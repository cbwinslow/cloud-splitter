from textual.widgets import Static, DataTable, ProgressBar
from textual.containers import Container, Vertical
from textual.reactive import reactive
from typing import List, Dict
from datetime import datetime
from cloud_splitter.utils.queue import QueueItem
from cloud_splitter.utils.status import ProcessStatus

class StatusView(Container):
    display = reactive(False)
    queue_items: reactive[List[QueueItem]] = reactive([])
    current_status: reactive[ProcessStatus] = reactive(None)
    
    def compose(self):
        with Vertical():
            yield Static("Processing Queue", id="queue-title")
            yield DataTable(id="queue-table")
            yield Static("Current Operation:", id="current-operation")
            yield ProgressBar(id="progress-bar")
            yield Static("", id="status-details")

    def on_mount(self) -> None:
        self.setup_table()

    def setup_table(self) -> None:
        table = self.query_one("#queue-table", DataTable)
        table.add_columns(
            "URL",
            "Status",
            "Progress",
            "Duration",
            "Error"
        )
        self.refresh_table()

    def refresh_table(self) -> None:
        table = self.query_one("#queue-table", DataTable)
        table.clear()
        for item in self.queue_items:
            duration = ""
            if item.start_time and item.end_time:
                duration = str(item.end_time - item.start_time).split('.')[0]
            elif item.start_time:
                duration = str(datetime.now() - item.start_time).split('.')[0]
            
            table.add_row(
                item.url,
                item.status,
                f"{item.progress:.1f}%",
                duration,
                item.error or ""
            )

    def watch_display(self, value: bool) -> None:
        """React to display changes"""
        self.styles.display = "block" if value else "none"

    def update_queue(self, items: List[QueueItem]) -> None:
        self.queue_items = items
        self.refresh_table()
        
    def update_status(self, status: ProcessStatus) -> None:
        self.current_status = status
        if status:
            self.query_one("#current-operation", Static).update(
                f"Current Operation: {status.stage}"
            )
            self.query_one("#progress-bar", ProgressBar).progress = status.progress / 100
            self.query_one("#status-details", Static).update(
                status.details or ""
            )
