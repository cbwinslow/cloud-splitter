"""
Metadata handling utilities for Cloud Splitter
"""
from typing import Dict, Any, Optional
import os
import json
from pathlib import Path
import requests
from PIL import Image
from mutagen import File
from mutagen.easyid3 import EasyID3
from cloud_splitter.utils.logging import get_logger
from cloud_splitter.exceptions import MetadataError

logger = get_logger()

class MetadataManager:
    def __init__(self, config):
        self.config = config
        self.metadata_dir = Path(self.config.paths.output_dir) / "metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    async def save_metadata(self, track_id: str, metadata: Dict[str, Any]) -> Path:
        """Save metadata to JSON file"""
        try:
            metadata_file = self.metadata_dir / f"{track_id}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            return metadata_file
        except Exception as e:
            raise MetadataError(f"Failed to save metadata: {str(e)}")

    async def download_artwork(self, url: str, track_id: str) -> Optional[Path]:
        """Download and save album artwork"""
        try:
            if not url:
                return None
            
            artwork_dir = self.metadata_dir / "artwork"
            artwork_dir.mkdir(exist_ok=True)
            
            artwork_path = artwork_dir / f"{track_id}.jpg"
            
            response = requests.get(url)
            response.raise_for_status()
            
            with open(artwork_path, 'wb') as f:
                f.write(response.content)
            
            # Optimize image
            with Image.open(artwork_path) as img:
                img.thumbnail((800, 800))  # Resize if too large
                img.save(artwork_path, "JPEG", quality=85, optimize=True)
            
            return artwork_path
            
        except Exception as e:
            logger.error(f"Failed to download artwork: {str(e)}")
            return None

    async def apply_metadata(self, audio_file: Path, metadata: Dict[str, Any], artwork_path: Optional[Path] = None):
        """Apply metadata to audio file"""
        try:
            audio = File(audio_file, easy=True)
            if audio is None:
                raise MetadataError(f"Unsupported audio format: {audio_file}")
            
            if not isinstance(audio, EasyID3):
                audio.add_tags()
            
            # Apply basic metadata
            audio['title'] = metadata.get('track_name', '')
            audio['artist'] = metadata.get('artist_name', '')
            audio['album'] = metadata.get('album_name', '')
            audio['date'] = metadata.get('album_release_date', '')
            audio['genre'] = metadata.get('artist_genres', [''])[0]
            
            # Save changes
            audio.save()
            
            # Apply artwork if available
            if artwork_path:
                self._apply_artwork(audio_file, artwork_path)
                
        except Exception as e:
            raise MetadataError(f"Failed to apply metadata: {str(e)}")

    def _apply_artwork(self, audio_file: Path, artwork_path: Path):
        """Apply artwork to audio file"""
        try:
            audio = File(audio_file)  # Reopen without easy=True
            
            with open(artwork_path, 'rb') as f:
                artwork_data = f.read()
            
            # Remove existing artwork
            if 'APIC:' in audio:
                del audio['APIC:']
            
            # Add new artwork
            audio['APIC:'] = APIC(
                encoding=3,  # UTF-8
                mime='image/jpeg',
                type=3,  # Cover (front)
                desc='Cover',
                data=artwork_data
            )
            
            audio.save()
            
        except Exception as e:
            logger.error(f"Failed to apply artwork: {str(e)}")
