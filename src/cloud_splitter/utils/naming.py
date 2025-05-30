import re
from pathlib import Path
from typing import Tuple, Optional

class FileNaming:
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace multiple spaces with single space
        filename = re.sub(r'\s+', ' ', filename)
        return filename.strip()

    @staticmethod
    def extract_artist_title(video_title: str) -> Tuple[Optional[str], str]:
        # Common patterns for artist - title separation
        patterns = [
            r'^(.+?)\s*[-–]\s*(.+)$',  # Artist - Title
            r'^(.+?)\s*["'"]\s*(.+)\s*["'"]$',  # Artist "Title"
            r'^(.+?)\s*:\s*(.+)$',  # Artist: Title
        ]
        
        for pattern in patterns:
            match = re.match(pattern, video_title)
            if match:
                artist, title = match.groups()
                return artist.strip(), title.strip()
        
        return None, video_title.strip()

    @staticmethod
    def deduplicate_artist(artist: str, title: str) -> Tuple[str, str]:
        if artist and artist.lower() in title.lower():
            # Remove artist name from title if it appears at the start
            title_clean = re.sub(f'^{re.escape(artist)}\s*[-–:]\s*', '', title, flags=re.IGNORECASE)
            # Remove artist name from title if it appears in parentheses
            title_clean = re.sub(f'\s*[({\[]\s*{re.escape(artist)}\s*[)}\]]\s*', '', title_clean, flags=re.IGNORECASE)
            return artist, title_clean
        return artist, title

    @staticmethod
    def generate_output_filename(title: str, artist: Optional[str] = None, stem_type: Optional[str] = None) -> str:
        parts = []
        if artist:
            parts.append(artist)
        parts.append(title)
        if stem_type:
            parts.append(stem_type)
        
        filename = ' - '.join(parts)
        return FileNaming.sanitize_filename(filename)
