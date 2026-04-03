from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class TicketType(str, enum.Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    FEATURE_REQUEST = "feature_request"
    OTHER = "other"

class TicketSentiment(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class TicketStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    ESCALATED = "escalated"
    FAILED = "failed"

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True)
    ticket_id = Column(String(100), unique=True, index=True)
    customer_email = Column(String(255))
    subject = Column(String(500))
    description = Column(Text)
    ticket_type = Column(SQLEnum(TicketType), nullable=True)
    sentiment = Column(SQLEnum(TicketSentiment), nullable=True)
    suggested_resolution = Column(Text, nullable=True)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.PENDING)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.ticket_id,
            "customer_email": self.customer_email,
            "subject": self.subject,
            "description": self.description,
            "ticket_type": self.ticket_type.value if self.ticket_type else None,
            "sentiment": self.sentiment.value if self.sentiment else None,
            "suggested_resolution": self.suggested_resolution,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
