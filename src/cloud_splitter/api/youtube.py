"""
YouTube API integration for fetching video metadata
"""
import os
from typing import Optional, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from cloud_splitter.utils.logging import get_logger
from cloud_splitter.exceptions import APIError

logger = get_logger()

class YouTubeClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize YouTube API client"""
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        
        if not self.api_key:
            raise APIError("YouTube API key not found. Set YOUTUBE_API_KEY environment variable.")
        
        try:
            self.client = build('youtube', 'v3', developerKey=self.api_key)
            logger.info("YouTube client initialized")
        except Exception as e:
            raise APIError(f"Failed to initialize YouTube client: {str(e)}")

    def get_video_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed video metadata"""
        try:
            video_response = self.client.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                logger.warning(f"No YouTube video found for ID: {video_id}")
                return None
            
            video = video_response['items'][0]
            snippet = video['snippet']
            
            # Get channel details
            channel_response = self.client.channels().list(
                part='snippet,statistics',
                id=snippet['channelId']
            ).execute()
            
            channel = channel_response['items'][0] if channel_response['items'] else None
            
            return {
                'title': snippet['title'],
                'description': snippet['description'],
                'channel_title': snippet['channelTitle'],
                'channel_id': snippet['channelId'],
                'published_at': snippet['publishedAt'],
                'thumbnails': snippet['thumbnails'],
                'tags': snippet.get('tags', []),
                'category_id': snippet['categoryId'],
                'duration': video['contentDetails']['duration'],
                'view_count': video['statistics']['viewCount'],
                'like_count': video['statistics'].get('likeCount', 0),
                'channel_info': {
                    'title': channel['snippet']['title'],
                    'description': channel['snippet']['description'],
                    'subscriber_count': channel['statistics']['subscriberCount'],
                    'video_count': channel['statistics']['videoCount'],
                    'thumbnail_url': channel['snippet']['thumbnails']['high']['url']
                } if channel else None
            }
            
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching video metadata: {str(e)}")
            return None

    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        import re
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)',
            r'youtube\.com/embed/([^&\n?#]+)',
            r'youtube\.com/v/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Get recent videos from a channel"""
        try:
            response = self.client.search().list(
                part='snippet',
                channelId=channel_id,
                order='date',
                type='video',
                maxResults=max_results
            ).execute()
            
            return [
                {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url']
                }
                for item in response.get('items', [])
            ]
            
        except Exception as e:
            logger.error(f"Error fetching channel videos: {str(e)}")
            return []
