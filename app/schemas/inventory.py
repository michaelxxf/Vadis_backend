from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class InventoryCreate(BaseModel):
    drug_id: int
    quantity: int
    batch_no: Optional[str]
    expiry_date: Optional[date]

class InventoryOut(InventoryCreate):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True
