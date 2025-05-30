from pathlib import Path
from typing import Optional, List, Dict, Any
import asyncio
from cloud_splitter.config import Config
from cloud_splitter.downloader import Downloader
from cloud_splitter.core.processor_factory import ProcessorFactory
from cloud_splitter.utils.queue import ProcessingQueue, QueueItem
from cloud_splitter.utils.status import StatusManager
from cloud_splitter.utils.logging import get_logger
from cloud_splitter.exceptions import DownloadError, ProcessingError

logger = get_logger()

class ProcessingWorkflow:
    """Coordinates the download and processing workflow"""
    
    def __init__(self, config: Config):
        self.config = config
        self.downloader = Downloader(config)
        self.processor = ProcessorFactory.create_processor(config)
        self.queue = ProcessingQueue()
        self.status = StatusManager()

    async def process_url(self, url: str) -> Dict[str, Any]:
        """Process a single URL through the workflow"""
        try:
            # Download stage
            self.status.update_status("download", "starting", 0, f"Downloading {url}")
            download_result = await self.downloader.download(url)
            self.status.mark_complete("download", {"file_path": str(download_result.file_path)})
            
            # Processing stage
            self.status.update_status("processing", "starting", 0, "Separating stems")
            processing_result = await self.processor.process_file(download_result.file_path)
            self.status.mark_complete("processing", {"stems": {k: str(v) for k, v in processing_result.stems.items()}})
            
            # Cleanup if needed
            if not self.config.download.keep_original:
                download_result.file_path.unlink()
                logger.info(f"Removed original file: {download_result.file_path}")
            
            return {
                "url": url,
                "title": download_result.title,
                "artist": download_result.artist,
                "stems": processing_result.stems,
                "output_dir": str(processing_result.output_dir)
            }
            
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            self.status.mark_failed("processing", str(e))
            raise ProcessingError(f"Failed to process {url}: {str(e)}")

    async def process_queue(self) -> List[Dict[str, Any]]:
        """Process all URLs in the queue"""
        results = []
        while True:
            item = await self.queue.get_next_item()
            if not item:
                break
                
            try:
                result = await self.process_url(item.url)
                await self.queue.mark_complete(item.url, result)
                results.append(result)
            except Exception as e:
                await self.queue.mark_failed(item.url, str(e))
                logger.error(f"Failed to process {item.url}: {str(e)}")
        
        return results

    async def add_urls(self, urls: List[str]) -> List[QueueItem]:
        """Add URLs to the processing queue"""
        return await self.queue.add_items(urls)

    @property
    def queue_status(self) -> Dict[str, int]:
        """Get current queue status"""
        return self.queue.queue_status

    @property
    def current_status(self) -> Dict[str, Any]:
        """Get current processing status"""
        return self.status.status_summary
