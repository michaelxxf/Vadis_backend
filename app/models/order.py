from sqlalchemy import Column, Enum, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    drug_id = Column(Integer, ForeignKey("drugs.id"))
    quantity = Column(Integer, default=1)

    drug = relationship("Drug")

class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    completed = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatusEnum), default="pending")
    created_at = Column(DateTime, default=func.now())

    items = relationship("OrderItem", back_populates="order")
