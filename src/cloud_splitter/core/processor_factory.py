from typing import Optional
from cloud_splitter.utils.logging import get_logger
from cloud_splitter.processor import Processor, SeparatorType
from cloud_splitter.config import Config

logger = get_logger()

class ProcessorFactory:
    """Factory for creating stem separation processors"""
    
    @staticmethod
    def create_processor(config: Config) -> Processor:
        """Create a processor based on configuration"""
        return Processor(config)
