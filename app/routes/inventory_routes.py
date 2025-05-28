from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.inventory import InventoryCreate, InventoryOut
from app.services.inventory_service import create_inventory
from app.db.session import get_db
from app.dependencies.auth import is_inventory_manager_or_admin

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=InventoryOut, dependencies=[Depends(is_inventory_manager_or_admin)])
def add_inventory(item: InventoryCreate, db: Session = Depends(get_db)):
    return create_inventory(db, item)

