import pytest
from pathlib import Path
from textual.app import App
from cloud_splitter.tui.app import CloudSplitterApp
from cloud_splitter.core.config_loader import ConfigLoader
from cloud_splitter.tui.download_view import DownloadView
from cloud_splitter.tui.config_view import ConfigView
from cloud_splitter.tui.status_view import StatusView
from cloud_splitter.tui.metadata_view import MetadataView
from cloud_splitter.tui.download_view import DownloadView
from cloud_splitter.tui.config_view import ConfigView
from cloud_splitter.tui.status_view import StatusView
from cloud_splitter.tui.metadata_view import MetadataView

@pytest.mark.asyncio
async def test_app_startup():
    """Test application startup"""
    app = CloudSplitterApp()
    async with app.run_test() as pilot:
        # Check that main components are present
        download_view = pilot.app.query_one(DownloadView)
        config_view = pilot.app.query_one(ConfigView)
        status_view = pilot.app.query_one(StatusView)
        metadata_view = pilot.app.query_one(MetadataView)
        
        assert download_view is not None
        assert config_view is not None
        assert status_view is not None
        assert metadata_view is not None
        
        await pilot.app.wait_for_animation()  # Wait for initial mount
        
        # Check initial view state
        assert download_view.display, "Download view should be visible on startup"
        assert not config_view.display, "Config view should be hidden on startup"
        assert not status_view.display, "Status view should be hidden on startup"
        assert not metadata_view.display, "Metadata view should be hidden on startup"

@pytest.mark.asyncio
async def test_view_switching():
    """Test view switching functionality"""
    app = CloudSplitterApp()
    async with app.run_test() as pilot:
        # Get references to all views
        download_view = pilot.app.query_one(DownloadView)
        config_view = pilot.app.query_one(ConfigView)
        status_view = pilot.app.query_one(StatusView)
        metadata_view = pilot.app.query_one(MetadataView)
        
        await pilot.app.wait_for_animation()  # Wait for initial mount
        
        # Test view switching sequence
        view_switches = [
            ("c", "config", config_view),
            ("s", "status", status_view),
            ("m", "metadata", metadata_view),
            ("d", "download", download_view)
        ]
        
        for key, name, active_view in view_switches:
            # Switch view
            await pilot.press(key)
            await pilot.app.wait_for_animation()
            
            # Verify states
            assert active_view.display, f"{name} view should be visible after switching"
            other_views = [v for k, n, v in view_switches if v != active_view]
            for view in other_views:
                assert not view.display, f"Other views should be hidden when in {name} view"
        # Switch to status view
        await pilot.press("s")
        # Give the app more time to process the view switch
        for _ in range(5):
            await pilot.pause()
        assert not pilot.app.query_one("DownloadView").display, "Download view should be hidden in status view"
        assert not pilot.app.query_one("ConfigView").display, "Config view should be hidden in status view"
        assert pilot.app.query_one("StatusView").display, "Status view should be visible"
        assert not pilot.app.query_one("MetadataView").display, "Metadata view should be hidden in status view"
        
        # Switch to metadata view
        await pilot.press("m")
        # Give the app more time to process the view switch
        for _ in range(5):
            await pilot.pause()
        assert not pilot.app.query_one("DownloadView").display, "Download view should be hidden in metadata view"
        assert not pilot.app.query_one("ConfigView").display, "Config view should be hidden in metadata view"
        assert not pilot.app.query_one("StatusView").display, "Status view should be hidden in metadata view"
        assert pilot.app.query_one("MetadataView").display, "Metadata view should be visible"
        
        # Switch back to download view
        await pilot.press("d")
        # Give the app more time to process the view switch
        for _ in range(5):
            await pilot.pause()
        assert pilot.app.query_one("DownloadView").display, "Download view should be visible after switching back"
        assert not pilot.app.query_one("ConfigView").display, "Config view should be hidden after switching back"
        assert not pilot.app.query_one("StatusView").display, "Status view should be hidden after switching back"
        assert not pilot.app.query_one("MetadataView").display, "Metadata view should be hidden after switching back"

@pytest.mark.asyncio
async def test_url_input():
    """Test URL input functionality"""
    app = CloudSplitterApp()
    async with app.run_test() as pilot:
        await pilot.app.wait_for_animation()  # Wait for initial mount
        
        download_view = pilot.app.query_one(DownloadView)
        assert download_view.display, "Download view should be visible for URL input test"
        
        url_input = download_view.query_one("#url-input")
        add_button = download_view.query_one("#add-urls-btn")
        
        # Add test URL
        test_url = "https://www.youtube.com/watch?v=test123"
        url_input.text = test_url
        
        # Click add button and wait for UI update
        await pilot.click(add_button)
        await pilot.app.wait_for_animation()
        
        # Verify URL was added to list
        url_list = download_view.query_one("#url-list")
        list_urls = [download_view.get_url_from_item(item) for item in url_list.children]
        assert test_url in list_urls, "URL should be added to the list"
