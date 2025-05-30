from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
from cloud_splitter.utils.logging import get_logger

logger = get_logger()

@dataclass
class QueueItem:
    url: str
    status: str = "pending"
    progress: float = 0.0
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class ProcessingQueue:
    def __init__(self):
        self.items: List[QueueItem] = []
        self._lock = asyncio.Lock()
        self._current_item: Optional[QueueItem] = None

    async def add_item(self, url: str) -> QueueItem:
        async with self._lock:
            item = QueueItem(url=url)
            self.items.append(item)
            logger.info(f"Added URL to queue: {url}")
            return item

    async def add_items(self, urls: List[str]) -> List[QueueItem]:
        return [await self.add_item(url) for url in urls]

    async def get_next_item(self) -> Optional[QueueItem]:
        async with self._lock:
            pending_items = [item for item in self.items if item.status == "pending"]
            if pending_items:
                self._current_item = pending_items[0]
                self._current_item.status = "processing"
                self._current_item.start_time = datetime.now()
                logger.info(f"Processing URL: {self._current_item.url}")
                return self._current_item
            return None

    async def update_progress(self, url: str, progress: float, status: str = "processing"):
        async with self._lock:
            item = self._find_item(url)
            if item:
                item.progress = progress
                item.status = status
                logger.debug(f"Updated progress for {url}: {progress:.1f}%")

    async def mark_complete(self, url: str, metadata: Optional[Dict[str, Any]] = None):
        async with self._lock:
            item = self._find_item(url)
            if item:
                item.status = "complete"
                item.progress = 100.0
                item.end_time = datetime.now()
                if metadata:
                    item.metadata = metadata
                logger.info(f"Completed processing URL: {url}")

    async def mark_failed(self, url: str, error: str):
        async with self._lock:
            item = self._find_item(url)
            if item:
                item.status = "failed"
                item.error = error
                item.end_time = datetime.now()
                logger.error(f"Failed processing URL: {url} - {error}")

    def _find_item(self, url: str) -> Optional[QueueItem]:
        return next((item for item in self.items if item.url == url), None)

    @property
    def current_item(self) -> Optional[QueueItem]:
        return self._current_item

    @property
    def queue_status(self) -> Dict[str, int]:
        status_count = {
            "pending": 0,
            "processing": 0,
            "complete": 0,
            "failed": 0
        }
        for item in self.items:
            status_count[item.status] = status_count.get(item.status, 0) + 1
        return status_count

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0

    @property
    def has_pending(self) -> bool:
        return any(item.status == "pending" for item in self.items)
