from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List
import json
from app.core.database import get_async_db
from app.services.websocket_manager import WebSocketManager

router = APIRouter()
manager = WebSocketManager()

@router.websocket("/audio/{client_id}")
async def websocket_audio_endpoint(
    websocket: WebSocket,
    client_id: str,
    db = Depends(get_async_db)
):
    """
    WebSocket endpoint for real-time audio processing updates
    """
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Process the message based on its type
                if message["type"] == "processing_status":
                    # Handle processing status updates
                    await manager.broadcast_to_client(
                        client_id,
                        {
                            "type": "status_update",
                            "data": message["data"]
                        }
                    )
                elif message["type"] == "visualization_data":
                    # Handle audio visualization data
                    await manager.broadcast_to_client(
                        client_id,
                        {
                            "type": "visualization_update",
                            "data": message["data"]
                        }
                    )
            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps({"error": "Invalid JSON format"})
                )
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
        await manager.broadcast_to_client(
            client_id,
            {"type": "system", "data": "Client disconnected"}
        )

@router.websocket("/spectrum/{client_id}")
async def websocket_spectrum_endpoint(
    websocket: WebSocket,
    client_id: str,
    db = Depends(get_async_db)
):
    """
    WebSocket endpoint for real-time spectrum analyzer data
    """
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                spectrum_data = json.loads(data)
                # Process and broadcast spectrum analyzer data
                await manager.broadcast_to_client(
                    client_id,
                    {
                        "type": "spectrum_data",
                        "data": spectrum_data
                    }
                )
            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps({"error": "Invalid JSON format"})
                )
    except WebSocketDisconnect:
        await manager.disconnect(client_id)

@router.websocket("/background/{client_id}")
async def websocket_background_endpoint(
    websocket: WebSocket,
    client_id: str,
    db = Depends(get_async_db)
):
    """
    WebSocket endpoint for music-reactive background effects
    """
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                background_data = json.loads(data)
                # Process and broadcast background effect data
                await manager.broadcast_to_client(
                    client_id,
                    {
                        "type": "background_effect",
                        "data": background_data
                    }
                )
            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps({"error": "Invalid JSON format"})
                )
    except WebSocketDisconnect:
        await manager.disconnect(client_id)

@router.get("/clients")
async def get_connected_clients():
    """
    Get list of connected WebSocket clients
    """
    return {"clients": manager.get_clients()}

