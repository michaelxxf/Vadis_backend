from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate
from sqlalchemy.orm import Session

def create_inventory(db: Session, data: InventoryCreate):
    new_inventory = Inventory(**data.dict())
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)
    return new_inventory

def update_inventory_quantity(db: Session, drug_id: int, quantity: int):
    inventory = db.query(Inventory).filter(Inventory.drug_id == drug_id).first()
    if inventory:
        inventory.quantity = quantity
        db.commit()
        db.refresh(inventory)
    return inventory

def get_inventory_by_drug_id(db: Session, drug_id: int):
    return db.query(Inventory).filter(Inventory.drug_id == drug_id).first()

def get_all_inventories(db: Session):
    return db.query(Inventory).all()

def delete_inventory(db: Session, drug_id: int):
    inventory = db.query(Inventory).filter(Inventory.drug_id == drug_id).first()
    if inventory:
        db.delete(inventory)
        db.commit()
    return inventory

def update_inventory(db: Session, drug_id: int, data: InventoryCreate):
    inventory = db.query(Inventory).filter(Inventory.drug_id == drug_id).first()
    if inventory:
        for key, value in data.dict().items():
            setattr(inventory, key, value) if value is not None else None
        db.commit()
        db.refresh(inventory)
    return inventory

