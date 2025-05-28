#inventory.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    drug_id = Column(Integer, ForeignKey("drugs.id"))
    quantity = Column(Integer, default=0)
    batch_no = Column(String(255))
    expiry_date = Column(Date)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    drug = relationship("Drug", backref="inventory")
