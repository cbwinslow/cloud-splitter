"""
Metadata enhancement module for Cloud Splitter
"""
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import asyncio
from cloud_splitter.api.spotify import SpotifyClient
from cloud_splitter.api.youtube import YouTubeClient
from cloud_splitter.utils.metadata import MetadataManager
from cloud_splitter.utils.logging import get_logger
from cloud_splitter.exceptions import MetadataError

logger = get_logger()

class MetadataEnhancer:
    def __init__(self, config):
        self.config = config
        self.spotify = SpotifyClient()
        self.youtube = YouTubeClient()
        self.metadata_manager = MetadataManager(config)

    async def enhance_metadata(self, url: str, initial_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance track metadata with information from Spotify and YouTube"""
        try:
            # Get YouTube metadata
            video_id = self.youtube.extract_video_id(url)
            if not video_id:
                raise MetadataError(f"Could not extract video ID from URL: {url}")
            
            youtube_metadata = await self._get_youtube_metadata(video_id)
            
            # Extract title and artist from YouTube
            title, artist = self._extract_title_artist(
                youtube_metadata.get('title', ''),
                initial_metadata.get('title', ''),
                initial_metadata.get('artist', '')
            )
            
            # Get Spotify metadata
            spotify_metadata = await self._get_spotify_metadata(title, artist)
            
            # Merge metadata
            enhanced_metadata = {
                'track_id': video_id,
                'source_url': url,
                'youtube': youtube_metadata,
                'spotify': spotify_metadata,
                'title': spotify_metadata.get('track_name', title) if spotify_metadata else title,
                'artist': spotify_metadata.get('artist_name', artist) if spotify_metadata else artist,
                'album': spotify_metadata.get('album_name', '') if spotify_metadata else '',
                'artwork_url': (
                    spotify_metadata.get('album_artwork_url')
                    if spotify_metadata and spotify_metadata.get('album_artwork_url')
                    else youtube_metadata.get('thumbnails', {}).get('maxres', {}).get('url', '')
                )
            }
            
            # Save metadata
            await self.metadata_manager.save_metadata(video_id, enhanced_metadata)
            
            # Download artwork
            if enhanced_metadata['artwork_url']:
                artwork_path = await self.metadata_manager.download_artwork(
                    enhanced_metadata['artwork_url'],
                    video_id
                )
                if artwork_path:
                    enhanced_metadata['artwork_path'] = str(artwork_path)
            
            return enhanced_metadata
            
        except Exception as e:
            logger.error(f"Error enhancing metadata: {str(e)}")
            return initial_metadata

    async def _get_youtube_metadata(self, video_id: str) -> Dict[str, Any]:
        """Fetch metadata from YouTube"""
        metadata = self.youtube.get_video_metadata(video_id)
        if not metadata:
            raise MetadataError(f"Could not fetch YouTube metadata for video ID: {video_id}")
        return metadata

    async def _get_spotify_metadata(self, title: str, artist: Optional[str]) -> Optional[Dict[str, Any]]:
        """Fetch metadata from Spotify"""
        try:
            metadata = self.spotify.search_track(title, artist)
            if metadata:
                # Get additional artist information
                artist_info = self.spotify.get_artist_info(metadata['artist_name'])
                if artist_info:
                    metadata['artist_info'] = artist_info
            return metadata
        except Exception as e:
            logger.error(f"Error fetching Spotify metadata: {str(e)}")
            return None

    def _extract_title_artist(self, youtube_title: str, default_title: str = '', default_artist: str = '') -> Tuple[str, str]:
        """Extract title and artist from YouTube title"""
        import re
        
        # Common patterns for title formats
        patterns = [
            r'^(.+?)\s*[-–]\s*(.+)$',  # Artist - Title
            r'^(.+?)\s*["'"]\s*(.+)\s*["'"]$',  # Artist "Title"
            r'^(.+?)\s*:\s*(.+)$',  # Artist: Title
        ]
        
        title = youtube_title
        artist = ''
        
        # Try to extract artist and title using patterns
        for pattern in patterns:
            match = re.match(pattern, youtube_title)
            if match:
                artist, title = match.groups()
                break
        
        # Clean up
        title = title.strip()
        artist = artist.strip()
        
        # Use defaults if extraction failed
        if not title:
            title = default_title
        if not artist:
            artist = default_artist
        
        return title, artist

    async def apply_metadata(self, audio_file: Path, metadata: Dict[str, Any]):
        """Apply metadata to audio file"""
        try:
            artwork_path = Path(metadata['artwork_path']) if 'artwork_path' in metadata else None
            await self.metadata_manager.apply_metadata(audio_file, metadata, artwork_path)
        except Exception as e:
            logger.error(f"Error applying metadata: {str(e)}")
