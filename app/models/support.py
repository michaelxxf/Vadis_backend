from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class TicketStatusEnum(str, enum.Enum):
    open = "open"
    pending = "pending"
    closed = "closed"

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String(255), nullable=False)
    status = Column(Enum(TicketStatusEnum), default="open")
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="tickets")
    messages = relationship("SupportMessage", back_populates="ticket", cascade="all, delete-orphan")

class SupportMessage(Base):
    __tablename__ = "support_messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    ticket = relationship("SupportTicket", back_populates="messages")
    sender = relationship("User")
