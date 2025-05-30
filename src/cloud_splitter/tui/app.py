# Update the imports section
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.binding import Binding
from textual.worker import Worker

from .download_view import DownloadView
from .config_view import ConfigView
from .status_view import StatusView
from .metadata_view import MetadataView  # Add this line

class CloudSplitterApp(App):
    """Main application class for Cloud Splitter"""
    
    TITLE = "Cloud Splitter"
    CSS_PATH = "style.css"
    BINDINGS = [
        Binding("d", "switch_to_download", "Download"),
        Binding("c", "switch_to_config", "Config"),
        Binding("s", "switch_to_status", "Status"),
        Binding("m", "switch_to_metadata", "Metadata"),  # Add this line
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DownloadView()
        yield ConfigView()
        yield StatusView()
        yield MetadataView()  # Add this line
        yield Footer()

    def on_mount(self) -> None:
        """Handle application startup"""
        self.switch_to_download()
        self._update_status()

    def action_switch_to_metadata(self) -> None:
        """Switch to metadata view"""
        self.query_one(DownloadView).display = False
        self.query_one(ConfigView).display = False
        self.query_one(StatusView).display = False
        self.query_one(MetadataView).display = True
