from textual.widgets import Static, Input, Button, ListView, TextArea, ListItem, Label
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from textual.message import Message
from typing import List
from cloud_splitter.utils.validation import Validator
from cloud_splitter.utils.queue import ProcessingQueue, QueueItem
import asyncio

class DownloadView(Container):
    """Main view for URL input and processing control"""
    
    display = reactive(True)  # Add display control
    
    class URLAdded(Message):
        def __init__(self, url: str):
            self.url = url
            super().__init__()

    class ProcessingRequested(Message):
        def __init__(self, urls: List[str]):
            self.urls = urls
            super().__init__()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = ProcessingQueue()
        self.url_list: List[str] = []

    def compose(self):
        with Vertical():
            yield Static("Enter URLs (one per line):", id="url-label")
            yield TextArea(id="url-input")
            with Horizontal():
                yield Button("Add URLs", id="add-urls-btn", variant="primary")
                yield Button("Clear", id="clear-btn", variant="error")
            yield Static("Processing Queue:", id="queue-label")
            yield ListView(id="url-list")
            with Horizontal():
                yield Button("Start Processing", id="process-btn", variant="success")
                yield Button("Remove Selected", id="remove-btn", variant="warning")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-urls-btn":
            self._add_urls()
        elif event.button.id == "clear-btn":
            self._clear_urls()
        elif event.button.id == "process-btn":
            self._start_processing()
        elif event.button.id == "remove-btn":
            self._remove_selected()

    def _add_urls(self) -> None:
        url_input = self.query_one("#url-input", TextArea)
        urls = url_input.text.strip().split('\n')
        valid_urls, invalid_urls = Validator.validate_urls(urls)
        
        if invalid_urls:
            self.notify(f"Invalid URLs detected: {', '.join(invalid_urls)}", severity="error")
        
        for url in valid_urls:
            if url not in self.url_list:
                self.url_list.append(url)
                self.post_message(self.URLAdded(url))
        
        self._refresh_url_list()
        url_input.clear()

    def _clear_urls(self) -> None:
        self.url_list.clear()
        self._refresh_url_list()

    def _start_processing(self) -> None:
        if not self.url_list:
            self.notify("No URLs to process", severity="warning")
            return
        
        self.post_message(self.ProcessingRequested(self.url_list.copy()))
        self._clear_urls()

    def _remove_selected(self) -> None:
        url_list = self.query_one("#url-list", ListView)
        if url_list.highlighted is not None:
            url = self.url_list[url_list.highlighted]
            self.url_list.pop(url_list.highlighted)
            self._refresh_url_list()
            
    def watch_display(self, value: bool) -> None:
        """React to display changes"""
        self.styles.display = "block" if value else "none"

    def _refresh_url_list(self) -> None:
        """Refresh the URL list widget"""
        url_list = self.query_one("#url-list", ListView)
        url_list.clear()
        for url in self.url_list:
            # Create a ListItem with an ID that matches the URL for easier retrieval
            list_item = ListItem(Label(url), id=f"url-{url}")
            url_list.append(list_item)

    def get_url_from_item(self, item: ListItem) -> str:
        """Extract URL from a ListItem widget"""
        return item.query_one(Label).render()
