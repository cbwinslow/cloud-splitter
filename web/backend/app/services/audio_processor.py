    async def _create_audio_file(self) -> None:
        """
        Create AudioFile record in database
        """
        try:
            file_stats = self.file_path.stat()
            self.audio_file = AudioFile(
                id=self.task_id,
                filename=self.file_path.name,
                original_path=str(self.file_path),
                file_size=file_stats.st_size,
                mime_type="audio/wav"  # TODO: Detect actual mime type
            )
            self.db.add(self.audio_file)
            await self.db.commit()
            await self.db.refresh(self.audio_file)
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Failed to create audio file record: {str(e)}")

    async def _create_processing_task(self) -> None:
        """
        Create ProcessingTask record in database
        """
        try:
            self.processing_task = ProcessingTask(
                id=self.task_id,
                audio_file_id=self.audio_file.id,
                status="pending",
                sample_rate=44100,  # Default values
                num_channels=2,
                bit_depth=16,
                format="wav",
                stem_separation=True
            )
            self.db.add(self.processing_task)
            await self.db.commit()
            await self.db.refresh(self.processing_task)
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Failed to create processing task record: {str(e)}")

    async def _save_processing_result(self, stems: Dict[str, Path]) -> None:
        """
        Save processing results to database
        """
        try:
            result = ProcessingResult(
                id=str(uuid.uuid4()),
                audio_file_id=self.audio_file.id,
                task_id=self.task_id,
                output_directory=str(self.output_dir),
                stems={name: str(path) for name, path in stems.items()},
                output_format="wav",
                output_sample_rate=44100,
                output_bit_depth=16,
                output_channels=2,
                processing_time=float(
                    (datetime.utcnow() - self.processing_task.started_at).total_seconds()
                )
            )
            self.db.add(result)
            await self.db.commit()
            await self.db.refresh(result)
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Failed to save processing result: {str(e)}")

import uuid
from pathlib import Path
import librosa
import numpy as np
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import asyncio
from pydub import AudioSegment
import soundfile as sf
from datetime import datetime

from app.core.config import settings
from app.schemas.audio import AudioMetadata, ProcessingStatus
from app.models.audio import AudioFile, ProcessingTask, AudioMetadata as AudioMetadataModel, ProcessingResult

class AudioProcessor:
    def __init__(self, file_path: Path, db: Session):
        self.file_path = file_path
        self.db = db
        self.task_id = str(uuid.uuid4())
        self.output_dir = settings.UPLOAD_DIR / "processed" / self.task_id
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.audio_file = None
        self.processing_task = None

    async def process_audio(self) -> None:
        """
        Process audio file: load, analyze, and split into stems
        """
        try:
            # Create database records
            await self._create_audio_file()
            await self._create_processing_task()
            
            # Update task status
            await self._update_status("processing")
        try:
            # Load audio file
            y, sr = librosa.load(str(self.file_path))
            
            # Extract metadata
            metadata = self._extract_metadata(y, sr)
            await self._save_metadata(metadata)

            # Process audio in stems
            stems = self._split_audio_stems(y, sr)
            
            # Save processed stems
            for stem_name, stem_data in stems.items():
                output_path = self.output_dir / f"{stem_name}.wav"
                sf.write(str(output_path), stem_data, sr)

            # Update processing status
            await self._update_status("completed")

        except Exception as e:
            await self._update_status("failed", str(e))
            raise

    def _extract_metadata(self, y: np.ndarray, sr: int) -> AudioMetadata:
        """
        Extract audio metadata including tempo, key, and spectral features
        """
        # Get tempo and beat frames
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        
        # Estimate key
        chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)
        key = librosa.feature.tonnetz(y=y, sr=sr)

        # Get spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

        return AudioMetadata(
            duration=float(len(y) / sr),
            sample_rate=sr,
            tempo=float(tempo),
            key=key.tolist(),
            spectral_features={
                "centroids": spectral_centroids.tolist(),
                "rolloff": spectral_rolloff.tolist()
            }
        )

    def _split_audio_stems(self, y: np.ndarray, sr: int) -> Dict[str, np.ndarray]:
        """
        Split audio into stems (vocals, drums, bass, other)
        """
        # TODO: Implement stem separation using Spleeter or similar library
        # This is a placeholder implementation
        stems = {
            "vocals": y.copy(),
            "drums": y.copy(),
            "bass": y.copy(),
            "other": y.copy()
        }
        return stems

    async def _save_metadata(self, metadata: AudioMetadata) -> None:
        """
        Save audio metadata to database
        """
        try:
            db_metadata = AudioMetadataModel(
                audio_file_id=self.audio_file.id,
                duration=metadata.duration,
                sample_rate=metadata.sample_rate,
                tempo=metadata.tempo,
                key=metadata.key,
                spectral_features=metadata.spectral_features,
                waveform=metadata.waveform,
                spectrum=metadata.spectrum
            )
            self.db.add(db_metadata)
            await self.db.commit()
            await self.db.refresh(db_metadata)
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Failed to save metadata: {str(e)}")

    async def _update_status(self, status: str, error: Optional[str] = None) -> None:
        """
        Update processing status in database
        """
        try:
            self.processing_task.status = status
            self.processing_task.error = error
            
            if status == "processing":
                self.processing_task.started_at = datetime.utcnow()
            elif status in ["completed", "failed"]:
                self.processing_task.completed_at = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(self.processing_task)
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Failed to update status: {str(e)}")

    @staticmethod
    async def get_task_status(task_id: str, db: Session) -> ProcessingStatus:
        """
        Get the current status of a processing task
        """
        try:
            task = await db.query(ProcessingTask).filter(ProcessingTask.id == task_id).first()
            if not task:
                raise Exception("Task not found")
            
            return ProcessingStatus(
                status=task.status,
                error=task.error,
                progress=task.progress,
                started_at=task.started_at,
                completed_at=task.completed_at
            )
        except Exception as e:
            raise Exception(f"Failed to get task status: {str(e)}")

    @staticmethod
    async def get_processed_file_path(task_id: str, db: Session) -> Path:
        """
        Get the path to a processed audio file
        """
        # TODO: Implement database path retrieval
        return settings.UPLOAD_DIR / "processed" / task_id / "output.wav"

    @staticmethod
    async def get_audio_metadata(task_id: str, db: Session) -> AudioMetadata:
        """
        Get stored metadata for an audio file
        """
        try:
            task = await db.query(ProcessingTask).filter(ProcessingTask.id == task_id).first()
            if not task:
                raise Exception("Task not found")
            
            metadata = await db.query(AudioMetadataModel).filter(
                AudioMetadataModel.audio_file_id == task.audio_file_id
            ).first()
            
            if not metadata:
                raise Exception("Metadata not found")
            
            return AudioMetadata(
                duration=metadata.duration,
                sample_rate=metadata.sample_rate,
                tempo=metadata.tempo,
                key=metadata.key,
                spectral_features=metadata.spectral_features,
                waveform=metadata.waveform,
                spectrum=metadata.spectrum
            )
        except Exception as e:
            raise Exception(f"Failed to get audio metadata: {str(e)}")

    @staticmethod
    async def delete_audio_files(task_id: str, db: Session) -> None:
        """
        Delete all files associated with a task
        """
        try:
            task = await db.query(ProcessingTask).filter(ProcessingTask.id == task_id).first()
            if not task:
                raise Exception("Task not found")
            
            # Delete files
            audio_file = await db.query(AudioFile).filter(AudioFile.id == task.audio_file_id).first()
            if audio_file:
                # Delete original file
                original_path = Path(audio_file.original_path)
                if original_path.exists():
                    original_path.unlink()
                
                # Delete processed files
                output_dir = settings.UPLOAD_DIR / "processed" / task_id
                if output_dir.exists():
                    for file in output_dir.glob("*"):
                        file.unlink()
                    output_dir.rmdir()
            
            # Delete database records
            await db.delete(task)
            if audio_file:
                await db.delete(audio_file)
            await db.commit()
            
        except Exception as e:
            await db.rollback()
            raise Exception(f"Failed to delete audio files: {str(e)}")

