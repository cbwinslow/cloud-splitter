from pathlib import Path
from typing import List, Optional
import yt_dlp
from pydantic import BaseModel

class DownloadResult(BaseModel):
    file_path: Path
    title: str
    artist: Optional[str]
    is_video: bool

class Downloader:
    def __init__(self, config):
        self.config = config
        self._setup_options()

    def _setup_options(self):
        self.ydl_opts = {
            'format': self.config.download.format,
            'outtmpl': '%(title)s.%(ext)s',
            'paths': {'home': str(self.config.paths.download_dir)},
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'extract_audio': True,
            'writethumbnail': True,
            'writeinfojson': True,
        }

    async def download(self, url: str) -> DownloadResult:
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return self._process_download_info(info)
        except Exception as e:
            raise RuntimeError(f"Download failed: {str(e)}")

    async def batch_download(self, urls: List[str]) -> List[DownloadResult]:
        results = []
        for url in urls:
            try:
                result = await self.download(url)
                results.append(result)
            except Exception as e:
                # Log error but continue with remaining URLs
                print(f"Error downloading {url}: {str(e)}")
        return results

    def _process_download_info(self, info: dict) -> DownloadResult:
        title = info.get('title', '')
        artist = info.get('artist') or info.get('uploader')
        file_path = Path(info['requested_downloads'][0]['filepath'])
        
        return DownloadResult(
            file_path=file_path,
            title=title,
            artist=artist,
            is_video=info.get('vcodec', 'none') != 'none'
        )
