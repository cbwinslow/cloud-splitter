from fastapi import WebSocket
from typing import Dict, List, Any
import asyncio
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self, websocket: WebSocket, client_id: str):
        """
        Connect a new client and store their WebSocket connection
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        """
        Disconnect a client and remove their WebSocket connection
        """
        if client_id in self.active_connections:
            await self.active_connections[client_id].close()
            del self.active_connections[client_id]

    async def broadcast_to_client(self, client_id: str, message: Dict[str, Any]):
        """
        Send a message to a specific client
        """
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients
        """
        for connection in self.active_connections.values():
            await connection.send_json(message)

    async def broadcast_spectrum(self, client_id: str, spectrum_data: List[float]):
        """
        Send spectrum analyzer data to a specific client
        """
        message = {
            "type": "spectrum_data",
            "data": spectrum_data
        }
        await self.broadcast_to_client(client_id, message)

    async def broadcast_background_effect(self, client_id: str, effect_data: Dict[str, Any]):
        """
        Send background effect data to a specific client
        """
        message = {
            "type": "background_effect",
            "data": effect_data
        }
        await self.broadcast_to_client(client_id, message)

    async def handle_message(self, client_id: str, message: Dict[str, Any]):
        """
        Process incoming WebSocket messages
        """
        message_type = message.get("type")
        if message_type == "spectrum_data":
            await self.broadcast_spectrum(client_id, message["data"])
        elif message_type == "background_effect":
            await self.broadcast_background_effect(client_id, message["data"])
        elif message_type == "processing_status":
            await self.broadcast_to_client(client_id, {
                "type": "status_update",
                "data": message["data"]
            })

    def get_clients(self) -> List[str]:
        """
        Get list of connected client IDs
        """
        return list(self.active_connections.keys())

    async def start_background_tasks(self):
        """
        Start background tasks for message processing
        """
        asyncio.create_task(self._process_message_queue())

    async def _process_message_queue(self):
        """
        Process messages from the queue
        """
        while True:
            message = await self.message_queue.get()
            try:
                await self.handle_message(message["client_id"], message["data"])
            except Exception as e:
                print(f"Error processing message: {e}")
            finally:
                self.message_queue.task_done()

