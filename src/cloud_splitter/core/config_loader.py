from pathlib import Path
from typing import Optional, Dict, Any
import tomli
import tomli_w
from cloud_splitter.config import Config
from cloud_splitter.exceptions import ConfigurationError
from cloud_splitter.utils.logging import get_logger

logger = get_logger()

class ConfigLoader:
    """Handles loading and validation of configuration"""
    
    @staticmethod
    def load_config(config_path: Optional[Path] = None) -> Config:
        """Load configuration from file or use defaults"""
        try:
            if config_path is None:
                config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"
            
            if config_path.exists():
                logger.info(f"Loading configuration from {config_path}")
                with open(config_path, "rb") as f:
                    config_data = tomli.load(f)
            else:
                logger.info("Using default configuration")
                default_config_path = Path(__file__).parent.parent / "config" / "default.toml"
                with open(default_config_path, "rb") as f:
                    config_data = tomli.load(f)
            
            return Config.model_validate(config_data)
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")

    @staticmethod
    def save_config(config: Config, config_path: Optional[Path] = None) -> None:
        """Save configuration to file"""
        try:
            if config_path is None:
                config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"
            
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, "wb") as f:
                config_dict = config.model_dump()
                # Convert Path objects to strings
                config_dict["paths"]["download_dir"] = str(config.paths.download_dir)
                config_dict["paths"]["output_dir"] = str(config.paths.output_dir)
                tomli_w.dump(config_dict, f)
            
            logger.info(f"Configuration saved to {config_path}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            raise ConfigurationError(f"Failed to save configuration: {str(e)}")
