# Update the imports section
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.binding import Binding
from textual.worker import Worker
from textual.reactive import reactive
from textual.css.query import NoMatches
import tomli_w

from cloud_splitter.core.config_loader import ConfigLoader
from cloud_splitter.config import Config
from .download_view import DownloadView
from .config_view import ConfigView
from .status_view import StatusView
from .metadata_view import MetadataView

class CloudSplitterApp(App):
    """Main application class for Cloud Splitter"""
    
    TITLE = "Cloud Splitter"
    CSS_PATH = "style.css"
    BINDINGS = [
        Binding("d", "switch_view('download')", "Download"),
        Binding("c", "switch_view('config')", "Config"),
        Binding("s", "switch_view('status')", "Status"),
        Binding("m", "switch_view('metadata')", "Metadata"),
        Binding("q", "quit", "Quit"),
    ]

    config: reactive[Config] = reactive(ConfigLoader.load_config())

    def compose(self) -> ComposeResult:
        yield Header()
        yield DownloadView()
        yield ConfigView()
        yield StatusView()
        yield MetadataView()  # Add this line
        yield Footer()

    def on_mount(self) -> None:
        """Handle application startup"""
        self.action_switch_view("download")
        self._update_status()

    def action_switch_view(self, view_name: str) -> None:
        """Switch between different views
        
        Args:
            view_name: Name of the view to switch to ('download', 'config', 'status', or 'metadata')
        """
        try:
            # Get references to all views
            download_view = self.query_one(DownloadView)
            config_view = self.query_one(ConfigView)
            status_view = self.query_one(StatusView)
            metadata_view = self.query_one(MetadataView)
            
            # Hide all views first
            download_view.display = False
            config_view.display = False
            status_view.display = False
            metadata_view.display = False
            
            # Show the selected view
            match view_name:
                case "download":
                    download_view.display = True
                case "config":
                    config_view.display = True
                case "status":
                    status_view.display = True
                case "metadata":
                    metadata_view.display = True
                case _:
                    self.notify("Invalid view name", severity="error")
                    return
            
            # Force a refresh to ensure display changes take effect
            self.refresh()
            
        except NoMatches:
            self.notify("View not found", severity="error")

    def _update_status(self) -> None:
        """Update status information"""
        # This method can be implemented later with actual status updates
        pass

    def save_config(self) -> None:
        """Save current configuration"""
        config_path = Path.home() / ".config" / "cloud-splitter" / "config.toml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, "wb") as f:
            tomli_w.dump(self.config, f)
