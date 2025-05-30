import pytest
from pathlib import Path
from cloud_splitter.core.workflow import ProcessingWorkflow
from cloud_splitter.core.config_loader import ConfigLoader
from cloud_splitter.exceptions import ProcessingError

@pytest.fixture
def workflow(tmp_path):
    """Create a test workflow with temporary directories"""
    config = ConfigLoader.load_config()
    config.paths.download_dir = tmp_path / "downloads"
    config.paths.output_dir = tmp_path / "output"
    config.download.keep_original = True
    config.processing.separator = "demucs"
    return ProcessingWorkflow(config)

@pytest.mark.asyncio
async def test_add_urls(workflow):
    """Test adding URLs to the workflow queue"""
    urls = [
        "https://www.youtube.com/watch?v=test1",
        "https://www.youtube.com/watch?v=test2"
    ]
    
    items = await workflow.add_urls(urls)
    assert len(items) == 2
    assert all(item.status == "pending" for item in items)
    assert workflow.queue_status["pending"] == 2

@pytest.mark.asyncio
async def test_invalid_url(workflow):
    """Test handling of invalid URLs"""
    urls = ["not_a_valid_url"]
    
    with pytest.raises(ProcessingError):
        await workflow.process_url(urls[0])

@pytest.mark.asyncio
async def test_queue_processing(workflow):
    """Test queue processing workflow"""
    urls = [
        "https://www.youtube.com/watch?v=test1",
        "https://www.youtube.com/watch?v=test2"
    ]
    
    # Add URLs to queue
    await workflow.add_urls(urls)
    
    # Mock processing to avoid actual downloads
    workflow.downloader.download = lambda url: {"file_path": Path("test.wav")}
    workflow.processor.process_file = lambda path: {"stems": {"vocals": Path("vocals.wav")}}
    
    # Process queue
    results = await workflow.process_queue()
    
    assert len(results) == 2
    assert workflow.queue_status["complete"] == 2
    assert workflow.queue_status["pending"] == 0
