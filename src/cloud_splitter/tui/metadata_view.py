"""
Metadata configuration and status view
"""
from textual.widgets import Static, Switch, DataTable, Button
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from typing import Dict, Any
from cloud_splitter.core.metadata_enhancer import MetadataEnhancer
from cloud_splitter.utils.logging import get_logger

logger = get_logger()

class MetadataView(Container):
    """View for configuring and monitoring metadata enhancement"""
    
    def compose(self):
        with Vertical():
            yield Static("Metadata Enhancement Settings", id="metadata-title")
            
            with Container(id="settings-container"):
                yield Switch("Enable Metadata Enhancement", id="enhance-switch", value=True)
                yield Switch("Save Album Artwork", id="artwork-switch", value=True)
                yield Switch("Apply to Stem Files", id="stems-switch", value=True)
            
            yield Static("API Status", id="api-status-title")
            yield DataTable(id="api-status-table")
            
            with Horizontal():
                yield Button("Test APIs", id="test-apis-btn", variant="primary")
                yield Button("Configure APIs", id="config-apis-btn", variant="default")

    def on_mount(self):
        """Initialize the view"""
        self.setup_table()
        self.load_settings()
        self.update_api_status()

    def setup_table(self):
        """Set up the API status table"""
        table = self.query_one("#api-status-table", DataTable)
        table.add_columns("API", "Status", "Details")
        self.refresh_table()

    def refresh_table(self):
        """Refresh the API status table"""
        table = self.query_one("#api-status-table", DataTable)
        table.clear()
        
        # Add API status rows
        spotify_status = self.check_spotify_status()
        youtube_status = self.check_youtube_status()
        
        table.add_row(
            "Spotify",
            "✓ Connected" if spotify_status['connected'] else "✗ Not Connected",
            spotify_status['details']
        )
        table.add_row(
            "YouTube",
            "✓ Connected" if youtube_status['connected'] else "✗ Not Connected",
            youtube_status['details']
        )

    def check_spotify_status(self) -> Dict[str, Any]:
        """Check Spotify API status"""
        try:
            from cloud_splitter.api.spotify import SpotifyClient
            spotify = SpotifyClient()
            test_result = spotify.search_track("Test")
            return {
                'connected': bool(test_result is not None),
                'details': "API working correctly" if test_result else "API configured but test failed"
            }
        except Exception as e:
            return {
                'connected': False,
                'details': str(e)
            }

    def check_youtube_status(self) -> Dict[str, Any]:
        """Check YouTube API status"""
        try:
            from cloud_splitter.api.youtube import YouTubeClient
            youtube = YouTubeClient()
            test_result = youtube.get_video_metadata("dQw4w9WgXcQ")
            return {
                'connected': bool(test_result is not None),
                'details': "API working correctly" if test_result else "API configured but test failed"
            }
        except Exception as e:
            return {
                'connected': False,
                'details': str(e)
            }

    def load_settings(self):
        """Load settings from configuration"""
        config = self.app.config
        metadata_config = config.get('metadata', {})
        
        self.query_one("#enhance-switch", Switch).value = metadata_config.get('enhance', True)
        self.query_one("#artwork-switch", Switch).value = metadata_config.get('save_artwork', True)
        self.query_one("#stems-switch", Switch).value = metadata_config.get('apply_to_stems', True)

    def save_settings(self):
        """Save settings to configuration"""
        config = self.app.config
        if 'metadata' not in config:
            config['metadata'] = {}
        
        config['metadata']['enhance'] = self.query_one("#enhance-switch", Switch).value
        config['metadata']['save_artwork'] = self.query_one("#artwork-switch", Switch).value
        config['metadata']['apply_to_stems'] = self.query_one("#stems-switch", Switch).value
        
        self.app.save_config()

    async def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses"""
        if event.button.id == "test-apis-btn":
            await self.test_apis()
        elif event.button.id == "config-apis-btn":
            self.configure_apis()

    async def test_apis(self):
        """Test API connections"""
        self.app.push_screen("loading", "Testing API connections...")
        self.refresh_table()
        self.app.pop_screen()
        
        if all([
            self.check_spotify_status()['connected'],
            self.check_youtube_status()['connected']
        ]):
            self.app.notify("API connections successful", severity="success")
        else:
            self.app.notify("Some API connections failed", severity="error")

    def configure_apis(self):
        """Launch API configuration"""
        import subprocess
        try:
            subprocess.run([sys.executable, "scripts/setup_apis.py"], check=True)
            self.app.notify("API configuration updated", severity="success")
            self.refresh_table()
        except subprocess.CalledProcessError:
            self.app.notify("API configuration failed", severity="error")
