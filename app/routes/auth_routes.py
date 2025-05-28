from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import RegisterUser, LoginUser, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=dict)
def register(data: RegisterUser, db: Session = Depends(get_db)):
    user = auth_service.register_user(data, db)
    return {"message": "User registered. Await verification."}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginUser, db: Session = Depends(get_db)):
    return auth_service.login_user(data, db)
