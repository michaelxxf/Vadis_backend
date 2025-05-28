from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    inventory_manager = "inventory_manager"
    support_staff = "support_staff"
    pharmacist = "pharmacist"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    is_verified = Column(Boolean, default=False)
    license_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())
    tickets = relationship("SupportTicket", back_populates="user", cascade="all, delete-orphan")

