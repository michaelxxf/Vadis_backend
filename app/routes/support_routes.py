from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.support import SupportTicketResponse, SupportMessageCreate, SupportMessageResponse, SupportTicketCreate
from app.models.support import SupportMessage, SupportTicket
from app.models.users import User
from typing import List
from app.dependencies.auth import get_current_user
from app.services.chat_manager import manager
import json

router = APIRouter(prefix="/support", tags=["Support"])

@router.post("/tickets", response_model=SupportTicketResponse)
def create_ticket(ticket_data: SupportTicketCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ticket = SupportTicket(subject=ticket_data.subject, user_id=user.id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/tickets", response_model=List[SupportTicketResponse])
def list_user_tickets(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(SupportTicket).filter_by(user_id=user.id).all()

@router.post("/messages", response_model=SupportMessageResponse)
def send_message(msg_data: SupportMessageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ticket = db.query(SupportTicket).filter_by(id=msg_data.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    msg = SupportMessage(ticket_id=msg_data.ticket_id, sender_id=user.id, message=msg_data.message)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

@router.get("/tickets/{ticket_id}/messages", response_model=List[SupportMessageResponse])
def get_ticket_messages(ticket_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ticket = db.query(SupportTicket).filter_by(id=ticket_id, user_id=user.id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket.messages


@router.websocket("/ws/support/{ticket_id}")
async def websocket_endpoint(websocket: WebSocket, ticket_id: int, db: Session = Depends(get_db)):
    await manager.connect(ticket_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            msg_data = json.loads(data)

            # Save to DB
            new_msg = models.SupportMessage(
                ticket_id=ticket_id,
                sender_id=msg_data["sender_id"],
                message=msg_data["message"]
            )
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)

            # Broadcast message to all clients
            response = {
                "ticket_id": ticket_id,
                "sender_id": msg_data["sender_id"],
                "message": msg_data["message"],
                "created_at": new_msg.timestamp.isoformat()
            }
            await manager.broadcast(ticket_id, json.dumps(response))

    except WebSocketDisconnect:
        manager.disconnect(ticket_id, websocket)
