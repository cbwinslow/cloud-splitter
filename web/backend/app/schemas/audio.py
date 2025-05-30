from pydantic import BaseModel, Field, validator, constr
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import os
from pathlib import Path

class SpectralFeatures(BaseModel):
    """Schema for spectral analysis features"""
    centroids: List[List[float]]
    rolloff: List[List[float]]
    bandwidth: Optional[List[List[float]]] = None
    contrast: Optional[List[List[float]]] = None
    flatness: Optional[List[List[float]]] = None

class AudioMetadata(BaseModel):
    """Schema for audio file metadata"""
    duration: float = Field(..., description="Duration in seconds")
    sample_rate: int = Field(..., description="Sample rate in Hz")
    tempo: float = Field(..., description="Tempo in BPM")
    key: List[List[float]] = Field(..., description="Key analysis data")
    spectral_features: SpectralFeatures = Field(..., description="Spectral analysis features")
    waveform: Optional[List[float]] = Field(None, description="Waveform data")
    spectrum: Optional[List[float]] = Field(None, description="Spectrum data")
    
    # Additional metadata
    channels: Optional[int] = Field(None, description="Number of audio channels")
    bit_rate: Optional[int] = Field(None, description="Bit rate in kbps")
    encoding: Optional[str] = Field(None, description="Audio encoding format")
    genre: Optional[str] = Field(None, description="Detected genre")
    artist: Optional[str] = Field(None, description="Artist name from metadata")
    title: Optional[str] = Field(None, description="Track title from metadata")
    album: Optional[str] = Field(None, description="Album name from metadata")
    year: Optional[int] = Field(None, description="Release year from metadata")

    class Config:
        schema_extra = {
            "example": {
                "duration": 180.5,
                "sample_rate": 44100,
                "tempo": 120.5,
                "key": [[0.8, 0.2, 0.1], [0.3, 0.7, 0.4]],
                "spectral_features": {
                    "centroids": [[100.0, 200.0], [150.0, 250.0]],
                    "rolloff": [[2000.0, 3000.0], [2500.0, 3500.0]]
                }
            }
        }

class ProcessingStatus(BaseModel):
    """Schema for audio processing status"""
    status: str = Field(..., description="Current processing status")
    error: Optional[str] = Field(None, description="Error message if processing failed")
    progress: Optional[float] = Field(None, description="Processing progress (0-100)")
    started_at: Optional[datetime] = Field(None, description="Processing start time")
    completed_at: Optional[datetime] = Field(None, description="Processing completion time")

    @validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["pending", "processing", "completed", "failed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return v

    class Config:
        schema_extra = {
            "example": {
                "status": "processing",
                "progress": 45.5,
                "started_at": "2025-05-30T09:30:00Z"
            }
        }

class AudioProcessingResponse(BaseModel):
    """Schema for audio processing response"""
    filename: str = Field(..., description="Original filename")
    status: str = Field(..., description="Initial processing status")
    task_id: str = Field(..., description="Processing task ID")
    metadata: Optional[AudioMetadata] = Field(None, description="Audio metadata if available")

    class Config:
        schema_extra = {
            "example": {
                "filename": "song.mp3",
                "status": "processing",
                "task_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }

class ProcessingConfig(BaseModel):
    """Schema for audio processing configuration"""
    sample_rate: int = Field(44100, description="Target sample rate in Hz")
    num_channels: int = Field(2, description="Number of output channels")
    bit_depth: int = Field(16, description="Output bit depth")
    format: str = Field("wav", description="Output file format")
    stem_separation: bool = Field(True, description="Enable stem separation")
    apply_effects: bool = Field(False, description="Apply audio effects")
    effects: Optional[Dict[str, Any]] = Field(None, description="Audio effects configuration")

    @validator("format")
    def validate_format(cls, v):
        allowed_formats = ["wav", "mp3", "flac", "ogg"]
        if v not in allowed_formats:
            raise ValueError(f"Format must be one of: {allowed_formats}")
        return v

    class Config:
        schema_extra = {
            "example": {
                "sample_rate": 44100,
                "num_channels": 2,
                "bit_depth": 16,
                "format": "wav",
                "stem_separation": True,
                "apply_effects": False
            }
        }

class FileValidation(BaseModel):
    """Schema for file validation"""
    max_size: int = Field(500 * 1024 * 1024, description="Maximum file size in bytes")
    allowed_types: List[str] = Field(
        ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp3"],
        description="Allowed MIME types"
    )
    allowed_extensions: List[str] = Field(
        [".mp3", ".wav", ".flac", ".ogg"],
        description="Allowed file extensions"
    )

    def validate_file(self, file_path: Path, mime_type: str) -> bool:
        """Validate file size and type"""
        if not file_path.exists():
            raise ValueError("File does not exist")
        
        if file_path.stat().st_size > self.max_size:
            raise ValueError(f"File size exceeds maximum allowed size of {self.max_size} bytes")
        
        if mime_type not in self.allowed_types:
            raise ValueError(f"File type {mime_type} not allowed")
        
        if file_path.suffix.lower() not in self.allowed_extensions:
            raise ValueError(f"File extension {file_path.suffix} not allowed")
        
        return True

class ProcessingResult(BaseModel):
    """Schema for processing result"""
    task_id: str = Field(..., description="Processing task ID")
    original_file: str = Field(..., description="Original file path")
    processed_files: List[str] = Field(..., description="List of processed file paths")
    metadata: AudioMetadata = Field(..., description="Audio metadata")
    status: ProcessingStatus = Field(..., description="Processing status")
    config: ProcessingConfig = Field(..., description="Processing configuration")

    class Config:
        schema_extra = {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "original_file": "/uploads/song.mp3",
                "processed_files": [
                    "/processed/550e8400-e29b-41d4-a716-446655440000/vocals.wav",
                    "/processed/550e8400-e29b-41d4-a716-446655440000/drums.wav"
                ]
            }
        }

class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages"""
    type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")

    @validator("type")
    def validate_message_type(cls, v):
        allowed_types = [
            "processing_status",
            "visualization_data",
            "spectrum_data",
            "background_effect"
        ]
        if v not in allowed_types:
            raise ValueError(f"Message type must be one of: {allowed_types}")
        return v

    class Config:
        schema_extra = {
            "example": {
                "type": "processing_status",
                "data": {
                    "status": "processing",
                    "progress": 45.5
                },
                "timestamp": "2025-05-30T09:30:00Z"
            }
        }

from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from datetime import datetime

class ProcessingStatus(BaseModel):
    """
    Schema for audio processing status
    """
    status: str
    error: Optional[str] = None
    progress: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class AudioMetadata(BaseModel):
    """
    Schema for audio file metadata
    """
    duration: float
    sample_rate: int
    tempo: float
    key: List[List[float]]
    spectral_features: Dict[str, List[List[float]]]
    waveform: Optional[List[float]] = None
    spectrum: Optional[List[float]] = None

class AudioProcessingResponse(BaseModel):
    """
    Schema for audio processing response
    """
    filename: str
    status: str
    task_id: str
    metadata: Optional[AudioMetadata] = None

class SpectrumData(BaseModel):
    """
    Schema for spectrum analyzer data
    """
    frequencies: List[float]
    magnitudes: List[float]
    timestamp: float

class BackgroundEffect(BaseModel):
    """
    Schema for background effect data
    """
    type: str
    intensity: float
    color: Optional[str] = None
    pattern: Optional[str] = None
    timestamp: float

class AudioProcessingConfig(BaseModel):
    """
    Schema for audio processing configuration
    """
    sample_rate: int = 44100
    num_channels: int = 2
    bit_depth: int = 16
    format: str = "wav"
    stem_separation: bool = True
    apply_effects: bool = False
    effects: Optional[Dict[str, Any]] = None

class AudioProcessingResult(BaseModel):
    """
    Schema for audio processing result
    """
    task_id: str
    original_file: str
    processed_files: List[str]
    metadata: AudioMetadata
    status: ProcessingStatus
    config: AudioProcessingConfig

