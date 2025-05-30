import pytest
from pathlib import Path
from textual.app import App
from cloud_splitter.tui.app import CloudSplitterApp
from cloud_splitter.core.config_loader import ConfigLoader

@pytest.mark.asyncio
async def test_app_startup():
    """Test application startup"""
    app = CloudSplitterApp()
    async with app.run_test() as pilot:
        # Check that main components are present
        download_view = pilot.app.query_one("DownloadView")
        config_view = pilot.app.query_one("ConfigView")
        status_view = pilot.app.query_one("StatusView")
        
        assert download_view is not None
        assert config_view is not None
        assert status_view is not None
        
        # Check initial view state
        assert download_view.display
        assert not config_view.display
        assert not status_view.display

@pytest.mark.asyncio
async def test_view_switching():
    """Test view switching functionality"""
    app = CloudSplitterApp()
    async with app.run_test() as pilot:
        # Switch to config view
        await pilot.press("c")
        assert not pilot.app.query_one("DownloadView").display
        assert pilot.app.query_one("ConfigView").display
        assert not pilot.app.query_one("StatusView").display
        
        # Switch to status view
        await pilot.press("s")
        assert not pilot.app.query_one("DownloadView").display
        assert not pilot.app.query_one("ConfigView").display
        assert pilot.app.query_one("StatusView").display
        
        # Switch back to download view
        await pilot.press("d")
        assert pilot.app.query_one("DownloadView").display
        assert not pilot.app.query_one("ConfigView").display
        assert not pilot.app.query_one("StatusView").display

@pytest.mark.asyncio
async def test_url_input():
    """Test URL input functionality"""
    app = CloudSplitterApp()
    async with app.run_test() as pilot:
        download_view = pilot.app.query_one("DownloadView")
        url_input = download_view.query_one("#url-input")
        
        # Add test URL
        test_url = "https://www.youtube.com/watch?v=test123"
        url_input.text = test_url
        
        # Click add button
        add_button = download_view.query_one("#add-urls-btn")
        await pilot.click(add_button)
        
        # Verify URL was added to list
        url_list = download_view.query_one("#url-list")
        assert test_url in [item.text for item in url_list.children]
