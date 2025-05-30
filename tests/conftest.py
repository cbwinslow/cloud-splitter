import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

@pytest.fixture
def sample_config(temp_dir):
    return {
        "paths": {
            "download_dir": str(temp_dir / "downloads"),
            "output_dir": str(temp_dir / "output")
        },
        "download": {
            "format": "bestaudio/best",
            "keep_original": True,
            "batch_enabled": True
        },
        "processing": {
            "separator": "demucs",
            "stems": ["vocals", "drums", "bass", "other"],
            "custom_labels": {}
        },
        "demucs": {
            "model": "htdemucs",
            "cpu_only": True,
            "shifts": 2
        }
    }
