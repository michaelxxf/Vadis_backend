from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ai_assistant import ask_drug_question

router = APIRouter(prefix="/ai", tags=["AI Assistant"])

@router.get("/ask")
def ai_answer(drug_id: int, question: str, db: Session = Depends(get_db)):
    result = ask_drug_question(db, drug_id, question)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
