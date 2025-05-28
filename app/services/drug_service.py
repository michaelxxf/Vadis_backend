from app.models.drugs import Drug
from app.schemas.drug import DrugCreate
from sqlalchemy.orm import Session

def create_drug(db: Session, drug: DrugCreate, user_id: int):
    new_drug = Drug(**drug.dict(), created_by=user_id)
    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)
    return new_drug

def get_drug_by_id(db: Session, drug_id: int):
    return db.query(Drug).filter(Drug.id == drug_id).first()

def get_drug_by_name(db: Session, name: str):
    return db.query(Drug).filter(Drug.name == name).first()

def get_all_drugs(db: Session):
    return db.query(Drug).all()

def update_drug(db: Session, drug_id: int, drug: DrugCreate):
    db_drug = get_drug_by_id(db, drug_id)
    if db_drug:
        for key, value in drug.dict().items():
            setattr(db_drug, key, value) if value is not None else None
        db.commit()
        db.refresh(db_drug)
    return db_drug

def delete_drug(db: Session, drug_id: int):
    db_drug = get_drug_by_id(db, drug_id)
    if db_drug:
        db.delete(db_drug)
        db.commit()
    return db_drug


