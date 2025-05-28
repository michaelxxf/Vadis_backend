from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.drug import DrugCreate, DrugOut
from app.services.drug_service import create_drug, get_drug_by_id
from app.db.session import get_db
from app.dependencies.auth import get_current_user, is_inventory_manager_or_admin
from app.models import drugs, users

router = APIRouter(prefix="/drugs", tags=["Drugs"])

@router.post("/", response_model=DrugOut, dependencies=[Depends(is_inventory_manager_or_admin)])
def add_drug(drug: DrugCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_drug(db, drug, user.id)

@router.get("/{drug_id}", response_model=DrugCreate)
def get_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = get_drug_by_id(db, drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug

@router.put("/{drug_id}", response_model=DrugOut, dependencies=[Depends(is_inventory_manager_or_admin)])
def update_drug(drug_id: int, drug: DrugCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing_drug = get_drug_by_id(db, drug_id)
    if not existing_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return update_drug(db, drug, user.id)

@router.put("/drugs/{drug_id}/price")
def update_drug_price(drug_id: int, price: float, db: Session = Depends(get_db), current_user= Depends(get_current_user)):
    if current_user.role not in ["admin", "staff"]:
        raise HTTPException(status_code=403, detail="Only staff can update prices.")

    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found.")

    drug.price = price
    db.commit()
    db.refresh(drug)
    return {"message": "Price updated", "drug": {"id": drug.id, "name": drug.name, "price": drug.price}}

@router.delete("/{drug_id}", dependencies=[Depends(is_inventory_manager_or_admin)])
def delete_drug(drug_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing_drug = get_drug_by_id(db, drug_id)
    if not existing_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    db.delete(existing_drug)
    db.commit()
    return {"message": "Drug deleted"}


@router.get("/orders/{order_id}")
def get_order_status(order_id: int, db: Session = Depends(get_db), current_user= Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or unauthorized")

    return {"order_id": order.id, "status": order.status, "total": order.total}
