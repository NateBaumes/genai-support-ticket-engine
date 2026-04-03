from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

from app.tickets.processor import TicketProcessor
from app.database import SessionLocal
from app.tickets.models import Ticket
from app.core.rate_limiter import RateLimiter

router = APIRouter()
processor = TicketProcessor()
rate_limiter = RateLimiter(rate=100, per_seconds=60)

class TicketCreate(BaseModel):
    customer_email: str
    subject: str
    description: str
    ticket_id: Optional[str] = None

@router.post("/create")
async def create_ticket(ticket: TicketCreate, background_tasks: BackgroundTasks):
    allowed, retry_after = await rate_limiter.is_allowed(ticket.customer_email)
    if not allowed:
        raise HTTPException(status_code=429, detail=f"Rate limited. Try again in {retry_after}s")
    
    ticket_id = ticket.ticket_id or f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    
    ticket_data = {
        "ticket_id": ticket_id,
        "customer_email": ticket.customer_email,
        "subject": ticket.subject,
        "description": ticket.description,
    }
    
    background_tasks.add_task(processor.process_ticket, ticket_data)
    
    return {
        "id": ticket_id,
        "status": "pending",
        "message": "Ticket created, processing in background",
        "created_at": datetime.utcnow().isoformat()
    }

@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str):
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket.to_dict()
    finally:
        db.close()

@router.get("/")
async def list_tickets(limit: int = 50):
    db = SessionLocal()
    try:
        tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).limit(limit).all()
        return [t.to_dict() for t in tickets]
    finally:
        db.close()
