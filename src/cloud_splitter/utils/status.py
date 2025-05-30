from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from cloud_splitter.utils.logging import get_logger

logger = get_logger()

@dataclass
class ProcessStatus:
    stage: str
    status: str
    progress: float
    details: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.start_time is None:
            self.start_time = datetime.now()

    @property
    def duration(self) -> Optional[float]:
        """Returns duration in seconds if process is complete"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

class StatusManager:
    def __init__(self):
        self.current_status: Optional[ProcessStatus] = None
        self._status_history: List[ProcessStatus] = []
        self.logger = get_logger()

    def update_status(self, stage: str, status: str, progress: float, details: Optional[str] = None):
        self.current_status = ProcessStatus(
            stage=stage,
            status=status,
            progress=progress,
            details=details
        )
        self.logger.info(f"{stage}: {status} ({progress:.1f}%) - {details or ''}")
        self._status_history.append(self.current_status)

    def mark_complete(self, stage: str, metadata: Optional[Dict[str, Any]] = None):
        if self.current_status and self.current_status.stage == stage:
            self.current_status.status = "complete"
            self.current_status.progress = 100.0
            self.current_status.end_time = datetime.now()
            if metadata:
                self.current_status.metadata = metadata
            self.logger.info(f"{stage}: Complete")

    def mark_failed(self, stage: str, error: str):
        if self.current_status and self.current_status.stage == stage:
            self.current_status.status = "failed"
            self.current_status.details = error
            self.current_status.end_time = datetime.now()
            self.logger.error(f"{stage}: Failed - {error}")

    @property
    def status_summary(self) -> Dict[str, Any]:
        if not self.current_status:
            return {"status": "idle"}
        
        return {
            "stage": self.current_status.stage,
            "status": self.current_status.status,
            "progress": self.current_status.progress,
            "details": self.current_status.details,
            "duration": self.current_status.duration
        }

    @property
    def history(self) -> List[ProcessStatus]:
        return self._status_history.copy()
