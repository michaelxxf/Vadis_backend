from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.order_service import add_to_cart, place_order
from app.dependencies.auth import get_current_user, is_inventory_manager_or_admin

router = APIRouter(prefix="/orders", tags=["Orders, Carts"])

@router.post("/cart/add")
def add_item(drug_id: int, quantity: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return add_to_cart(current_user.id, drug_id, quantity, db)

@router.post("/order/place")
def place_user_order(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return place_order(current_user.id, db)

@router.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db), current_user= Depends(get_current_user)):
    if current_user.role not in ["admin", "inventory_manager"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated", "status": order.status}
