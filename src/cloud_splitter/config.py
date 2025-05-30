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

class Config(BaseModel):
    paths: PathConfig = PathConfig()
    download: DownloadConfig = DownloadConfig()
    processing: ProcessingConfig = ProcessingConfig()
    demucs: DemucsConfig = DemucsConfig()
    spleeter: SpleeterConfig = SpleeterConfig()
    tui: TUIConfig = TUIConfig()

    @classmethod
    def load(cls, config_path: Optional[Path] = None):
        # TODO: Implement config loading from file
        return cls()
