# Setting Up API Access for Cloud Splitter

Cloud Splitter can enhance your audio files with metadata from Spotify and YouTube. Here's how to set up API access:

## Spotify API Setup

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in or create an account
3. Create a new application
4. Get your Client ID and Client Secret
5. Set environment variables:
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id"
   export SPOTIFY_CLIENT_SECRET="your_client_secret"
   ```
   Or add to your config file:
   ```toml
   [apis]
   spotify_client_id = "your_client_id"
   spotify_client_secret = "your_client_secret"
   ```

## YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Set environment variable:
   ```bash
   export YOUTUBE_API_KEY="your_api_key"
   ```
   Or add to your config file:
   ```toml
   [apis]
   youtube_api_key = "your_api_key"
   ```

## Configuration Options

In your config file (`~/.config/cloud-splitter/config.toml`):

```toml
[metadata]
enhance = true            # Enable metadata enhancement
save_artwork = true       # Save album artwork
apply_to_stems = true    # Apply metadata to stem files

[apis]
spotify_client_id = ""    # Your Spotify Client ID
spotify_client_secret = "" # Your Spotify Client Secret
youtube_api_key = ""      # Your YouTube API Key
```

## Testing Your Setup

Run the verification script:
```bash
./scripts/verify_install.py
```

Or test API access directly:
```python
from cloud_splitter.api.spotify import SpotifyClient
from cloud_splitter.api.youtube import YouTubeClient

# Test Spotify
spotify = SpotifyClient()
track_info = spotify.search_track("Your Song Title")

# Test YouTube
youtube = YouTubeClient()
video_info = youtube.get_video_metadata("video_id")
```

## Troubleshooting

1. API Credentials Not Found:
   - Check environment variables
   - Verify config file settings
   - Ensure proper permissions

2. Rate Limiting:
   - Monitor API usage
   - Implement appropriate delays
   - Consider quota increases

3. Metadata Not Found:
   - Check search terms
   - Verify API responses
   - Check log files
