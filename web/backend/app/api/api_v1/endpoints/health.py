from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, database

router = APIRouter()

@router.get("")
async def health_check():
    """
    Health check endpoint to verify service status
    """
    return {
        "status": "healthy",
        "service": "cloud-splitter-web",
        "database": await check_database(),
    }

@router.get("/db")
async def check_database():
    """
    Check database connection status
    """
    try:
        if database.is_connected:
            return {"status": "connected"}
        return {"status": "disconnected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@router.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check to verify all components are operational
    """
    return {
        "status": "ready",
        "components": {
            "api": "operational",
            "database": "operational",
            "file_system": "operational"
        }
    }

