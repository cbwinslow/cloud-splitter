"""
Metadata configuration and status view
"""
from typing import Dict, Any
import sys

from textual.app import ComposeResult
from textual.widgets import Static, Switch, DataTable, Button
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from textual.binding import Binding

from cloud_splitter.core.metadata_enhancer import MetadataEnhancer
from cloud_splitter.utils.logging import get_logger

logger = get_logger()

class MetadataView(Container):
    """View for configuring and monitoring metadata enhancement"""
    
    # Class variables
    BINDINGS = [
        Binding("s", "save", "Save Settings", show=True),
        Binding("t", "test_apis", "Test APIs", show=True),
    ]
    
    # Reactive properties
    display = reactive(False)
    is_loading = reactive(False)
    def compose(self) -> ComposeResult:
        """Create child widgets for the metadata view."""
        with Vertical(id="metadata-container"):
            yield Static("Metadata Enhancement Settings", id="metadata-title", classes="title")
            
            with Container(id="settings-container"):
                with Horizontal():
                    yield Static("Enable Metadata Enhancement", classes="setting-label")
                    yield Switch(id="enhance-switch", value=True)
                with Horizontal():
                    yield Static("Save Album Artwork", classes="setting-label")
                    yield Switch(id="artwork-switch", value=True)
                with Horizontal():
                    yield Static("Apply to Stem Files", classes="setting-label")
                    yield Switch(id="stems-switch", value=True)
            
            yield Static("API Status", id="api-status-title", classes="title")
            yield DataTable(id="api-status-table")
            
            with Horizontal(classes="button-container"):
                yield Button("Test APIs", id="test-apis-btn", variant="primary")
                yield Button("Configure APIs", id="config-apis-btn", variant="default")

    def on_mount(self) -> None:
        """Initialize the view"""
        # Set default values for switches
        self.query_one("#enhance-switch", Switch).value = True
        self.query_one("#artwork-switch", Switch).value = True
        self.query_one("#stems-switch", Switch).value = True
        
        # Initialize other components
        self.setup_table()
        self.load_settings()

    def setup_table(self) -> None:
        """Set up the API status table"""
        table = self.query_one("#api-status-table", DataTable)
        table.add_columns("API", "Status", "Details")
        self.refresh_table()

    def refresh_table(self) -> None:
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

    def load_settings(self) -> None:
        """Load settings from configuration"""
        try:
            # Default values for switches
            self.query_one("#enhance-switch", Switch).value = True
            self.query_one("#artwork-switch", Switch).value = True
            self.query_one("#stems-switch", Switch).value = True
            
            # If there's a config, override with its values
            if hasattr(self.app.config, 'metadata'):
                metadata = self.app.config.metadata
                if hasattr(metadata, 'enhance'):
                    self.query_one("#enhance-switch", Switch).value = metadata.enhance
                if hasattr(metadata, 'save_artwork'):
                    self.query_one("#artwork-switch", Switch).value = metadata.save_artwork
                if hasattr(metadata, 'apply_to_stems'):
                    self.query_one("#stems-switch", Switch).value = metadata.apply_to_stems
        except Exception as e:
            logger.error(f"Error loading metadata settings: {str(e)}")

    def save_settings(self) -> None:
        """Save settings to configuration"""
        try:
            # Create metadata config if it doesn't exist
            if not hasattr(self.app.config, 'metadata'):
                from pydantic import create_model
                MetadataConfig = create_model('MetadataConfig', 
                    enhance=(bool, True),
                    save_artwork=(bool, True),
                    apply_to_stems=(bool, True)
                )
                self.app.config.metadata = MetadataConfig()
            
            # Update values
            self.app.config.metadata.enhance = self.query_one("#enhance-switch", Switch).value
            self.app.config.metadata.save_artwork = self.query_one("#artwork-switch", Switch).value
            self.app.config.metadata.apply_to_stems = self.query_one("#stems-switch", Switch).value
            
            self.app.save_config()
        except Exception as e:
            logger.error(f"Error saving metadata settings: {str(e)}")
            self.app.notify("Failed to save settings", severity="error")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "test-apis-btn":
            await self.test_apis()
        elif event.button.id == "config-apis-btn":
            self.configure_apis()

    async def test_apis(self) -> None:
        """Test API connections"""
        self.is_loading = True
        try:
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
        except Exception as e:
            logger.error(f"Error during API testing: {str(e)}")
            self.app.notify("API testing failed", severity="error")
        finally:
            self.is_loading = False

    def configure_apis(self) -> None:
        """Launch API configuration"""
        import subprocess
        try:
            subprocess.run([sys.executable, "scripts/setup_apis.py"], check=True)
            self.app.notify("API configuration updated", severity="success")
            self.refresh_table()
        except subprocess.CalledProcessError:
            self.app.notify("API configuration failed", severity="error")

    def watch_display(self, value: bool) -> None:
        """React to display changes"""
        if value:
            self.styles.display = "block"
            self.load_settings()  # Refresh settings when view becomes visible
            self.refresh_table()  # Refresh API status when view becomes visible
        else:
            self.styles.display = "none"
            
    def watch_is_loading(self, value: bool) -> None:
        """React to loading state changes"""
        if value:
            self.query_one("#test-apis-btn").disabled = True
            self.query_one("#config-apis-btn").disabled = True
        else:
            self.query_one("#test-apis-btn").disabled = False
            self.query_one("#config-apis-btn").disabled = False
