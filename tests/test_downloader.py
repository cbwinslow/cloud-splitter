import pytest
from pathlib import Path
from cloud_splitter.downloader import Downloader, DownloadResult
from unittest.mock import patch, MagicMock

@pytest.fixture
def sample_config(temp_dir):
    class Config:
        class Download:
            format = "bestaudio/best"
            keep_original = True
            batch_enabled = True
        
        class Paths:
            download_dir = temp_dir / "downloads"
            output_dir = temp_dir / "output"
        
        download = Download()
        paths = Paths()
    
    return Config()

@pytest.fixture
def downloader(sample_config):
    return Downloader(sample_config)

def test_downloader_initialization(downloader):
    assert downloader.config is not None
    assert 'format' in downloader.ydl_opts
    assert downloader.ydl_opts['format'] == 'bestaudio/best'

@pytest.mark.asyncio
async def test_download_single_url(downloader, temp_dir):
    mock_info = {
        'title': 'Test Song',
        'artist': 'Test Artist',
        'requested_downloads': [{'filepath': str(temp_dir / 'test.mp3')}],
        'vcodec': 'none'
    }
    
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        instance = mock_ydl.return_value.__enter__.return_value
        instance.extract_info.return_value = mock_info
        
        result = await downloader.download('https://youtube.com/watch?v=test')
        
        assert isinstance(result, DownloadResult)
        assert result.title == 'Test Song'
        assert result.artist == 'Test Artist'
        assert not result.is_video

@pytest.mark.asyncio
async def test_batch_download(downloader):
    urls = [
        'https://youtube.com/watch?v=test1',
        'https://youtube.com/watch?v=test2'
    ]
    
    mock_info1 = {
        'title': 'Test Song 1',
        'artist': 'Artist 1',
        'requested_downloads': [{'filepath': 'test1.mp3'}],
        'vcodec': 'none'
    }
    
    mock_info2 = {
        'title': 'Test Song 2',
        'artist': 'Artist 2',
        'requested_downloads': [{'filepath': 'test2.mp3'}],
        'vcodec': 'none'
    }
    
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        instance = mock_ydl.return_value.__enter__.return_value
        instance.extract_info.side_effect = [mock_info1, mock_info2]
        
        results = await downloader.batch_download(urls)
        
        assert len(results) == 2
        assert all(isinstance(r, DownloadResult) for r in results)
        assert results[0].title == 'Test Song 1'
        assert results[1].title == 'Test Song 2'
