#!/usr/bin/env python3
from googleapiclient.discovery import build
from pathlib import Path
import tomli

def load_config():
    config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"
    with open(config_path, "rb") as f:
        return tomli.load(f)

def test_youtube_api():
    config = load_config()
    api_key = config["apis"]["youtube_api_key"]
    
    print("Testing YouTube API connection...")
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        
        # Test search functionality
        resp = youtube.search().list(
            part="snippet",
            q="guitar tutorial",
            type="video",
            maxResults=2
        ).execute()
        
        print("\nSearch results:")
        for item in resp["items"]:
            print(f"Video ID: {item['id']['videoId']}")
            print(f"Title: {item['snippet']['title']}\n")
            
        # Test video details functionality
        if resp["items"]:
            video_id = resp["items"][0]["id"]["videoId"]
            video_response = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()
            
            if video_response["items"]:
                video = video_response["items"][0]
                print("Detailed video information:")
                print(f"Title: {video['snippet']['title']}")
                print(f"View count: {video['statistics']['viewCount']}")
                print(f"Like count: {video['statistics'].get('likeCount', 'N/A')}")
                
        print("\nYouTube API test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error testing YouTube API: {str(e)}")
        return False

if __name__ == "__main__":
    test_youtube_api()

