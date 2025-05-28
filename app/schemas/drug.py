from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DrugCreate(BaseModel):
    name: str
    description: Optional[str]
    composition: Optional[str]
    usage: Optional[str]
    warnings: Optional[str]
    price: float

class DrugOut(DrugCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
