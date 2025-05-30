from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from datetime import datetime

from app.core.database import Base

class AudioFile(Base):
    """
    Model for storing audio file information
    """
    __tablename__ = "audio_files"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    filename = Column(String(255), nullable=False)
    original_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    processing_task = relationship("ProcessingTask", back_populates="audio_file", uselist=False)
    metadata = relationship("AudioMetadata", back_populates="audio_file", uselist=False)
    processing_results = relationship("ProcessingResult", back_populates="audio_file")

class ProcessingTask(Base):
    """
    Model for tracking audio processing tasks
    """
    __tablename__ = "processing_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    audio_file_id = Column(String(36), ForeignKey("audio_files.id"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    error = Column(Text, nullable=True)
    progress = Column(Float, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Configuration
    sample_rate = Column(Integer, nullable=False, default=44100)
    num_channels = Column(Integer, nullable=False, default=2)
    bit_depth = Column(Integer, nullable=False, default=16)
    format = Column(String(10), nullable=False, default="wav")
    stem_separation = Column(Boolean, nullable=False, default=True)
    apply_effects = Column(Boolean, nullable=False, default=False)
    effects_config = Column(JSON, nullable=True)

    # Relationships
    audio_file = relationship("AudioFile", back_populates="processing_task")
    processing_result = relationship("ProcessingResult", back_populates="processing_task", uselist=False)

class AudioMetadata(Base):
    """
    Model for storing audio metadata
    """
    __tablename__ = "audio_metadata"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    audio_file_id = Column(String(36), ForeignKey("audio_files.id"), nullable=False)
    duration = Column(Float, nullable=False)
    sample_rate = Column(Integer, nullable=False)
    tempo = Column(Float, nullable=True)
    key = Column(JSON, nullable=True)  # Stores the key analysis as JSON
    spectral_features = Column(JSON, nullable=True)  # Stores spectral features as JSON
    waveform = Column(JSON, nullable=True)  # Stores waveform data as JSON
    spectrum = Column(JSON, nullable=True)  # Stores spectrum data as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Additional metadata
    channels = Column(Integer, nullable=True)
    bit_rate = Column(Integer, nullable=True)
    encoding = Column(String(50), nullable=True)
    genre = Column(String(100), nullable=True)
    artist = Column(String(255), nullable=True)
    title = Column(String(255), nullable=True)
    album = Column(String(255), nullable=True)
    year = Column(Integer, nullable=True)

    # Relationships
    audio_file = relationship("AudioFile", back_populates="metadata")

class ProcessingResult(Base):
    """
    Model for storing audio processing results
    """
    __tablename__ = "processing_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    audio_file_id = Column(String(36), ForeignKey("audio_files.id"), nullable=False)
    task_id = Column(String(36), ForeignKey("processing_tasks.id"), nullable=False)
    output_directory = Column(String(512), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Processing results
    stems = Column(JSON, nullable=True)  # Paths to separated stems
    effects = Column(JSON, nullable=True)  # Applied effects and their parameters
    output_format = Column(String(10), nullable=False)
    output_sample_rate = Column(Integer, nullable=False)
    output_bit_depth = Column(Integer, nullable=False)
    output_channels = Column(Integer, nullable=False)

    # Quality metrics
    quality_score = Column(Float, nullable=True)
    processing_time = Column(Float, nullable=True)  # Processing time in seconds
    file_size_reduction = Column(Float, nullable=True)  # Size reduction percentage

    # Relationships
    audio_file = relationship("AudioFile", back_populates="processing_results")
    processing_task = relationship("ProcessingTask", back_populates="processing_result")

# Helper function to create all tables
def init_db(engine):
    """
    Create all database tables
    """
    Base.metadata.create_all(bind=engine)

