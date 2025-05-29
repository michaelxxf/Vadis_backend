from transformers import pipeline
from sqlalchemy.orm import Session
from app.models.drugs import Drug
import requests
from bs4 import BeautifulSoup

qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad", local_files_only= True)

def recommend_related_drugs(db: Session, current_drug: Drug, limit=3):
    # Similar composition or category (assuming these fields exist)
    related = db.query(Drug).filter(
        Drug.id != current_drug.id,
        Drug.composition.like(f"%{current_drug.composition.split()[0]}%")
    ).limit(limit).all()

    # Trending (assume you have an 'orders' or 'sales_count' table)
    trending = db.query(Drug).order_by(Drug.sales_count.desc()).limit(limit).all()

    recs = []

    for d in related:
        recs.append({
            "name": d.name,
            "reason": f"Similar composition: {d.composition}"
        })

    for d in trending:
        recs.append({
            "name": d.name,
            "reason": f"Trending (high sales)"
        })

    return recs

def ask_drug_question(db: Session, drug_id: int, question: str):
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        return {"error": "Drug not found"}

    # Use DB content
    context = f"""
    Name: {drug.name}
    Description: {drug.description}
    Composition: {drug.composition}
    Usage: {drug.usage}
    Warnings: {drug.warnings}
    """

    result = qa_pipeline(question=question, context=context)
    
    recommendations = recommend_related_drugs(db, drug)

    return {
        "answer": result["answer"],
        "score": result["score"],
        "source": "internal_db",
        "recommendations": recommendations
    }
