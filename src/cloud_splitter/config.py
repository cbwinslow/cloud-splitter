from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PathConfig(BaseModel):
    download_dir: Path = Field(default=Path.home() / "Downloads" / "cloud-splitter")
    output_dir: Path = Field(default=Path.home() / "Music" / "stems")

class DownloadConfig(BaseModel):
    format: str = "bestaudio/best"
    keep_original: bool = True
    batch_enabled: bool = True

class ProcessingConfig(BaseModel):
    separator: str = "demucs"
    stems: List[str] = ["vocals", "drums", "bass", "other"]
    custom_labels: Dict[str, str] = {}

class DemucsConfig(BaseModel):
    model: str = "htdemucs"
    cpu_only: bool = False
    shifts: int = 2

class SpleeterConfig(BaseModel):
    stems: int = 4

class TUIConfig(BaseModel):
    theme: str = "dark"
    show_notifications: bool = True


class MetadataConfig(BaseModel):
    enhance: bool = True
    save_artwork: bool = True
    apply_to_stems: bool = True


class Config(BaseModel):
    paths: PathConfig = PathConfig()
    download: DownloadConfig = DownloadConfig()
    processing: ProcessingConfig = ProcessingConfig()
    demucs: DemucsConfig = DemucsConfig()
    spleeter: SpleeterConfig = SpleeterConfig()
    tui: TUIConfig = TUIConfig()
    metadata: MetadataConfig = MetadataConfig()

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> 'Config':
        """Load configuration from file or create default"""
        if config_path is None:
            config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"

        if config_path.exists():
            import tomli
            with open(config_path, "rb") as f:
                config_data = tomli.load(f)
                return cls.model_validate(config_data)
        
        return cls()
