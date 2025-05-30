"""
Spotify API integration for fetching artist and album metadata
"""
import os
from typing import Optional, Dict, Any
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from cloud_splitter.utils.logging import get_logger
from cloud_splitter.exceptions import APIError

logger = get_logger()

class SpotifyClient:
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """Initialize Spotify client with credentials"""
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not (self.client_id and self.client_secret):
            raise APIError("Spotify credentials not found. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")
        
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.client = spotipy.Spotify(auth_manager=auth_manager)
            logger.info("Spotify client initialized")
        except Exception as e:
            raise APIError(f"Failed to initialize Spotify client: {str(e)}")

    def search_track(self, title: str, artist: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Search for a track and return its metadata"""
        try:
            query = title
            if artist:
                query = f"track:{title} artist:{artist}"
            
            results = self.client.search(query, type='track', limit=1)
            
            if not results['tracks']['items']:
                logger.warning(f"No Spotify results found for: {query}")
                return None
            
            track = results['tracks']['items'][0]
            artist_id = track['artists'][0]['id']
            artist_info = self.client.artist(artist_id)
            
            return {
                'track_name': track['name'],
                'artist_name': track['artists'][0]['name'],
                'artist_id': artist_id,
                'album_name': track['album']['name'],
                'album_artwork_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'album_release_date': track['album']['release_date'],
                'artist_genres': artist_info['genres'],
                'artist_popularity': artist_info['popularity'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            }
            
        except Exception as e:
            logger.error(f"Error fetching Spotify metadata: {str(e)}")
            return None

    def get_artist_info(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed artist information"""
        try:
            results = self.client.search(artist_name, type='artist', limit=1)
            
            if not results['artists']['items']:
                logger.warning(f"No Spotify artist found for: {artist_name}")
                return None
            
            artist = results['artists']['items'][0]
            top_tracks = self.client.artist_top_tracks(artist['id'])
            
            return {
                'name': artist['name'],
                'genres': artist['genres'],
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'image_url': artist['images'][0]['url'] if artist['images'] else None,
                'external_url': artist['external_urls']['spotify'],
                'top_tracks': [
                    {
                        'name': track['name'],
                        'album': track['album']['name'],
                        'preview_url': track['preview_url']
                    }
                    for track in top_tracks['tracks'][:5]
                ]
            }
            
        except Exception as e:
            logger.error(f"Error fetching artist info: {str(e)}")
            return None

    def get_album_artwork(self, album_name: str, artist_name: str) -> Optional[str]:
        """Get album artwork URL"""
        try:
            query = f"album:{album_name} artist:{artist_name}"
            results = self.client.search(query, type='album', limit=1)
            
            if not results['albums']['items']:
                return None
            
            album = results['albums']['items'][0]
            return album['images'][0]['url'] if album['images'] else None
            
        except Exception as e:
            logger.error(f"Error fetching album artwork: {str(e)}")
            return None
