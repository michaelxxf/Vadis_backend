from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    composition = Column(Text)
    usage = Column(Text)
    warnings = Column(Text)
    price = Column(Float, nullable=False, default=0.0)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    sales_count = Column(Integer, default=0)  # New line
