from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SupportMessageBase(BaseModel):
    message: str

class SupportMessageCreate(SupportMessageBase):
    ticket_id: int

class SupportMessageResponse(SupportMessageBase):
    id: int
    sender_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SupportTicketCreate(BaseModel):
    subject: str

class SupportTicketResponse(BaseModel):
    id: int
    subject: str
    status: str
    created_at: datetime
    messages: List[SupportMessageResponse] = []

    class Config:
        orm_mode = True
