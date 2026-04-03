from datetime import datetime
from typing import Dict, Any

from app.tickets.models import Ticket, TicketStatus, TicketType, TicketSentiment
from app.database import SessionLocal
from app.vendors.llm_provider import OpenAIProvider
from app.vendors.slack_client import SlackClient
from app.core.circuit_breaker import CircuitBreaker

class TicketProcessor:
    def __init__(self):
        self.llm = OpenAIProvider()
        self.slack = SlackClient()
        self.circuit = CircuitBreaker(failure_threshold=3, recovery_timeout=30)
    
    async def process_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        db = SessionLocal()
        
        try:
            existing = db.query(Ticket).filter(
                Ticket.ticket_id == ticket_data["ticket_id"]
            ).first()
            
            if existing:
                print(f"⚠️ Duplicate {ticket_data['ticket_id']} - skipping")
                return existing.to_dict()
            
            ticket = Ticket(
                ticket_id=ticket_data["ticket_id"],
                customer_email=ticket_data["customer_email"],
                subject=ticket_data["subject"],
                description=ticket_data["description"],
                status=TicketStatus.PENDING
            )
            db.add(ticket)
            db.commit()
            
            # Classify with LLM
            try:
                text = f"Subject: {ticket.subject}\nDescription: {ticket.description}"
                classification = await self.circuit.call(self.llm.classify_ticket, text)
                ticket.ticket_type = TicketType(classification["type"])
                ticket.sentiment = TicketSentiment(classification["sentiment"])
                print(f"📊 Classified as {ticket.ticket_type.value} ({ticket.sentiment.value})")
            except Exception as e:
                ticket.status = TicketStatus.FAILED
                ticket.error_message = f"LLM failed: {str(e)}"
                db.commit()
                return ticket.to_dict()
            
            # Generate resolution
            try:
                resolution = await self.circuit.call(self.llm.generate_resolution, ticket.description, [])
                ticket.suggested_resolution = resolution
                print(f"💡 Generated resolution")
            except Exception as e:
                print(f"⚠️ Resolution failed: {e}")
            
            # Escalate if negative
            if ticket.sentiment == TicketSentiment.NEGATIVE:
                ticket.status = TicketStatus.ESCALATED
                await self.slack.send_escalation({
                    "ticket_id": ticket.ticket_id,
                    "customer": ticket.customer_email,
                    "type": ticket.ticket_type.value,
                    "sentiment": ticket.sentiment.value,
                    "description": ticket.description[:300]
                })
                print(f"🚨 Escalated to Slack")
            else:
                ticket.status = TicketStatus.PROCESSED
            
            ticket.processed_at = datetime.utcnow()
            db.commit()
            
            return ticket.to_dict()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            if 'ticket' in locals():
                ticket.status = TicketStatus.FAILED
                ticket.error_message = str(e)
                db.commit()
            raise
        finally:
            db.close()
