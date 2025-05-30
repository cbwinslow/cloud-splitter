from fastapi import APIRouter
from app.api.api_v1.endpoints import audio, health, websocket

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])

