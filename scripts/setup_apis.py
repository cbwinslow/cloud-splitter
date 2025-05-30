#!/usr/bin/env python3
"""
Interactive setup script for Cloud Splitter APIs
"""
import os
import sys
import webbrowser
from pathlib import Path
import tomli
import tomli_w

def get_config_path():
    """Get the path to the configuration file"""
    return Path.home() / ".config" / "cloud-splitter" / "config.toml"

def load_config():
    """Load existing configuration"""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, "rb") as f:
            return tomli.load(f)
    return {}

def save_config(config):
    """Save configuration to file"""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)

def setup_spotify():
    """Guide user through Spotify API setup"""
    print("\nSpotify API Setup")
    print("================")
    print("1. Visit the Spotify Developer Dashboard")
    print("2. Create a new application")
    print("3. Get your Client ID and Client Secret\n")
    
    open_dashboard = input("Open Spotify Developer Dashboard in browser? (y/n): ")
    if open_dashboard.lower() == 'y':
        webbrowser.open("https://developer.spotify.com/dashboard/")
    
    client_id = input("\nEnter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    
    return client_id, client_secret

def setup_youtube():
    """Guide user through YouTube API setup"""
    print("\nYouTube API Setup")
    print("================")
    print("1. Go to Google Cloud Console")
    print("2. Create a project or select existing project")
    print("3. Enable YouTube Data API v3")
    print("4. Create API credentials\n")
    
    open_console = input("Open Google Cloud Console in browser? (y/n): ")
    if open_console.lower() == 'y':
        webbrowser.open("https://console.cloud.google.com/apis/library/youtube.googleapis.com")
    
    api_key = input("\nEnter your YouTube API Key: ").strip()
    
    return api_key

def test_apis(config):
    """Test API connections"""
    print("\nTesting API Connections...")
    
    try:
        from cloud_splitter.api.spotify import SpotifyClient
        spotify = SpotifyClient(
            client_id=config['apis']['spotify_client_id'],
            client_secret=config['apis']['spotify_client_secret']
        )
        test_result = spotify.search_track("Never Gonna Give You Up", "Rick Astley")
        if test_result:
            print("✓ Spotify API connection successful")
        else:
            print("✗ Spotify API test failed")
    except Exception as e:
        print(f"✗ Spotify API error: {str(e)}")
    
    try:
        from cloud_splitter.api.youtube import YouTubeClient
        youtube = YouTubeClient(api_key=config['apis']['youtube_api_key'])
        test_result = youtube.get_video_metadata("dQw4w9WgXcQ")  # Rick Astley video ID
        if test_result:
            print("✓ YouTube API connection successful")
        else:
            print("✗ YouTube API test failed")
    except Exception as e:
        print(f"✗ YouTube API error: {str(e)}")

def main():
    print("Cloud Splitter API Setup Wizard")
    print("===============================")
    
    # Load existing config
    config = load_config()
    if 'apis' not in config:
        config['apis'] = {}
    
    # Setup Spotify
    print("\nSetup Spotify API access:")
    client_id, client_secret = setup_spotify()
    config['apis']['spotify_client_id'] = client_id
    config['apis']['spotify_client_secret'] = client_secret
    
    # Setup YouTube
    print("\nSetup YouTube API access:")
    api_key = setup_youtube()
    config['apis']['youtube_api_key'] = api_key
    
    # Enable metadata enhancement
    if 'metadata' not in config:
        config['metadata'] = {}
    config['metadata']['enhance'] = True
    config['metadata']['save_artwork'] = True
    config['metadata']['apply_to_stems'] = True
    
    # Save configuration
    save_config(config)
    print("\nConfiguration saved successfully!")
    
    # Test APIs
    test_apis(config)
    
    print("\nSetup complete! You can now use metadata enhancement features.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {str(e)}")
        sys.exit(1)
