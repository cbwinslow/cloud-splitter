from typing import List
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    BackgroundTasks,
    Query,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import aiofiles
import os
from pathlib import Path

from app.core.config import settings
from app.core.database import get_db
from app.services.audio_processor import AudioProcessor
from app.schemas.audio import AudioProcessingResponse, AudioMetadata

router = APIRouter()

@router.post("/upload", response_model=AudioProcessingResponse)
async def upload_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload an audio file for processing
    """
    if file.content_type not in settings.ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not supported. Supported types: {settings.ALLOWED_AUDIO_TYPES}"
        )

    # Generate unique filename
    file_path = settings.UPLOAD_DIR / f"{file.filename}"
    
    try:
        # Save uploaded file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Schedule processing in background
        processor = AudioProcessor(file_path, db)
        background_tasks.add_task(processor.process_audio)

        return AudioProcessingResponse(
            filename=file.filename,
            status="processing",
            task_id=processor.task_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{task_id}")
async def get_processing_status(task_id: str, db: Session = Depends(get_db)):
    """
    Get the status of an audio processing task
    """
    try:
        # Get status from database
        status = await AudioProcessor.get_task_status(task_id, db)
        return {"task_id": task_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/download/{task_id}")
async def download_processed_file(task_id: str, db: Session = Depends(get_db)):
    """
    Download a processed audio file
    """
    try:
        # Get file path from database
        file_path = await AudioProcessor.get_processed_file_path(task_id, db)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=Path(file_path).name
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/metadata/{task_id}", response_model=AudioMetadata)
async def get_audio_metadata(task_id: str, db: Session = Depends(get_db)):
    """
    Get metadata for a processed audio file
    """
    try:
        metadata = await AudioProcessor.get_audio_metadata(task_id, db)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{task_id}")
async def delete_audio_file(task_id: str, db: Session = Depends(get_db)):
    """
    Delete an audio file and its processed outputs
    """
    try:
        await AudioProcessor.delete_audio_files(task_id, db)
        return {"status": "success", "message": "Files deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

