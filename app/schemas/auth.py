from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    super_admin = "super_admin"
    inventory_manager = "inventory_manager"
    customer_care = "customer_care"
    pharmacist = "pharmacist"

class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    license_id: str  # Only for pharmacists

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
