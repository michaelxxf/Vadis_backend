from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, ticket_id: int, websocket: WebSocket):
        await websocket.accept()
        if ticket_id not in self.active_connections:
            self.active_connections[ticket_id] = []
        self.active_connections[ticket_id].append(websocket)

    def disconnect(self, ticket_id: int, websocket: WebSocket):
        if ticket_id in self.active_connections:
            self.active_connections[ticket_id].remove(websocket)

    async def broadcast(self, ticket_id: int, message: str):
        if ticket_id in self.active_connections:
            for conn in self.active_connections[ticket_id]:
                await conn.send_text(message)

manager = ConnectionManager()
