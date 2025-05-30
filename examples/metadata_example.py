#!/usr/bin/env python3
"""
Example script demonstrating metadata enhancement features
"""
import asyncio
from pathlib import Path
from cloud_splitter.core.config_loader import ConfigLoader
from cloud_splitter.core.metadata_enhancer import MetadataEnhancer
from cloud_splitter.utils.logging import setup_logging

async def enhance_track_metadata(url: str):
    # Set up logging
    logger = setup_logging()
    
    # Load configuration
    config = ConfigLoader.load_config()
    
    # Create metadata enhancer
    enhancer = MetadataEnhancer(config)
    
    try:
        # Initial metadata (normally from download)
        initial_metadata = {
            'title': '',
            'artist': ''
        }
        
        # Enhance metadata
        metadata = await enhancer.enhance_metadata(url, initial_metadata)
        
        # Print results
        print("\nEnhanced Metadata:")
        print("================")
        print(f"Title: {metadata['title']}")
        print(f"Artist: {metadata['artist']}")
        
        if metadata.get('spotify'):
            print("\nSpotify Information:")
            print(f"Album: {metadata['spotify'].get('album_name', 'N/A')}")
            print(f"Release Date: {metadata['spotify'].get('album_release_date', 'N/A')}")
            print(f"Genres: {', '.join(metadata['spotify'].get('artist_genres', ['N/A']))}")
            
            if 'artist_info' in metadata['spotify']:
                print("\nArtist Information:")
                print(f"Followers: {metadata['spotify']['artist_info']['followers']:,}")
                print(f"Popularity: {metadata['spotify']['artist_info']['popularity']}/100")
                print("\nTop Tracks:")
                for track in metadata['spotify']['artist_info']['top_tracks']:
                    print(f"- {track['name']} ({track['album']})")
        
        if metadata.get('youtube'):
            print("\nYouTube Information:")
            print(f"Channel: {metadata['youtube'].get('channel_title', 'N/A')}")
            print(f"Views: {int(metadata['youtube'].get('view_count', 0)):,}")
            print(f"Likes: {int(metadata['youtube'].get('like_count', 0)):,}")
            
            if metadata['youtube'].get('channel_info'):
                print("\nChannel Information:")
                print(f"Subscribers: {int(metadata['youtube']['channel_info']['subscriber_count']):,}")
                print(f"Total Videos: {int(metadata['youtube']['channel_info']['video_count']):,}")
        
        if 'artwork_path' in metadata:
            print(f"\nArtwork saved to: {metadata['artwork_path']}")
        
    except Exception as e:
        logger.error(f"Error processing metadata: {str(e)}")
        raise

if __name__ == "__main__":
    # Example YouTube URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Never Gonna Give You Up
    
    print("Cloud Splitter Metadata Enhancement Example")
    print("=========================================")
    print(f"Processing URL: {url}")
    
    asyncio.run(enhance_track_metadata(url))
