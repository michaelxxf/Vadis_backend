from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user, require_role
from app.models.users import User

router = APIRouter()

@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return {"name": current_user.name, "email": current_user.email}

@router.get("/admin-only")
def admin_only(current_user: User = Depends(require_role("super_admin"))):
    return {"msg": f"Hello {current_user.name}, you're an admin."}
