from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.users import User
from app.schemas.auth import RegisterUser, LoginUser
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token

def register_user(data: RegisterUser, db: Session):
    user = db.query(User).filter(User.email == data.email).first()
    userNo = db.query(User).filter(User.license_id == data.license_id).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if userNo:
        raise HTTPException(status_code=400, detail="License Number already registered")

    new_user = User(
        full_name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role="pharmacist",
        license_id=data.license_id,
        is_verified=False  # Will verify manually later
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(data: LoginUser, db: Session):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified")

    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
