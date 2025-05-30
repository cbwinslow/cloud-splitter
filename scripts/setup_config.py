#!/usr/bin/env python3
import tomli_w
from pathlib import Path

def setup_config():
    config = {
        "apis": {
            "spotify_client_id": "edaa7260b853412dbaf2886eaae6b3dd",
            "spotify_client_secret": "d606f3bc1b5049939285d658c8d553af",
            "youtube_api_key": "YOUR_YOUTUBE_API_KEY"  # This needs to be filled in
        },
        "metadata": {
            "enhance": True,
            "save_artwork": True,
            "apply_to_stems": True
        }
    }
    
    config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)
    
    print("Configuration file created at:", config_path)

if __name__ == "__main__":
    setup_config()

