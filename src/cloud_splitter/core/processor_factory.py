from typing import Optional
from cloud_splitter.processor import Processor
from cloud_splitter.config import Config
from cloud_splitter.utils.logging import get_logger

logger = get_logger()

class ProcessorFactory:
    """Factory for creating stem separation processors"""
    
    @staticmethod
    def create_processor(config: Config) -> Processor:
        """Create a processor based on configuration"""
        separator = config.processing.separator.lower()
        
        if separator == "demucs":
            from cloud_splitter.processor import DemucsProcessor
            logger.info("Creating Demucs processor")
            return DemucsProcessor(config)
        elif separator == "spleeter":
            from cloud_splitter.processor import SpleeterProcessor
            logger.info("Creating Spleeter processor")
            return SpleeterProcessor(config)
        else:
            raise ValueError(f"Unsupported separator: {separator}")
