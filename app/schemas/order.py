from pydantic import BaseModel
from typing import List

class CartItemBase(BaseModel):
    drug_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemOut(CartItemBase):
    id: int
    class Config:
        orm_mode = True

class OrderItemOut(BaseModel):
    drug_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    pass  # Nothing for now, will order all items in cart

class OrderOut(BaseModel):
    id: int
    status: str
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
