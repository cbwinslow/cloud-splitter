"""Common UI components for Cloud Splitter"""
from textual.widgets import Static
from textual.reactive import reactive
from typing import Optional

class StatusIndicator(Static):
    """Status indicator with icon and message"""
    
    status: reactive[str] = reactive("idle")
    message: reactive[Optional[str]] = reactive(None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._icons = {
            "idle": "○",
            "running": "◉",
            "success": "✓",
            "error": "✗",
            "warning": "⚠"
        }

    def render(self) -> str:
        icon = self._icons.get(self.status, "○")
        return f"{icon} {self.message or ''}"

    def update_status(self, status: str, message: Optional[str] = None) -> None:
        self.status = status
        self.message = message

class ProgressIndicator(Static):
    """Progress indicator with percentage and message"""
    
    progress: reactive[float] = reactive(0.0)
    message: reactive[Optional[str]] = reactive(None)
    
    def render(self) -> str:
        progress_bar = self._create_progress_bar()
        message = f" {self.message}" if self.message else ""
        return f"{progress_bar} {self.progress:.1f}%{message}"

    def _create_progress_bar(self) -> str:
        width = 20
        filled = int(self.progress / 100 * width)
        return f"[{'=' * filled}{'-' * (width - filled)}]"

    def update_progress(self, progress: float, message: Optional[str] = None) -> None:
        self.progress = max(0.0, min(100.0, progress))
        self.message = message
