from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .manager import WebSocketManager
import uuid

router = APIRouter(
    tags=["Websocket"],
    responses={404: {"description": "Not found"}},
)

manager = WebSocketManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client_id = str(uuid.uuid4())
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)