import re
from pathlib import Path
from typing import List, Tuple, Union
from urllib.parse import urlparse

class ValidationError(Exception):
    pass

class Validator:
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if the given string is a valid URL."""
        try:
            result = urlparse(url)
            # Check for supported domains (youtube, soundcloud, etc.)
            valid_domains = [
                'youtube.com', 'youtu.be',
                'soundcloud.com',
                'vimeo.com',
                'dailymotion.com'
            ]
            return all([
                result.scheme in ('http', 'https'),
                any(domain in result.netloc for domain in valid_domains)
            ])
        except:
            return False

    @staticmethod
    def validate_urls(urls: List[str]) -> Tuple[List[str], List[str]]:
        """Validate a list of URLs, returning valid and invalid URLs."""
        valid_urls = []
        invalid_urls = []
        for url in urls:
            if Validator.validate_url(url.strip()):
                valid_urls.append(url.strip())
            else:
                invalid_urls.append(url.strip())
        return valid_urls, invalid_urls

    @staticmethod
    def validate_path(path: Union[str, Path]) -> Path:
        """Validate if the given path is valid and accessible."""
        try:
            path = Path(path).expanduser().resolve()
            if not path.parent.exists():
                raise ValidationError(f"Parent directory does not exist: {path.parent}")
            return path
        except Exception as e:
            raise ValidationError(f"Invalid path: {str(e)}")

    @staticmethod
    def validate_stem_name(name: str) -> bool:
        """Validate if the given stem name is valid."""
        # Allow alphanumeric characters, spaces, and common punctuation
        pattern = r'^[\w\s\-_]+$'
        return bool(re.match(pattern, name))

    @staticmethod
    def validate_config(config: dict) -> List[str]:
        """Validate configuration values, returning a list of errors if any."""
        errors = []
        
        # Validate paths
        try:
            Validator.validate_path(config.get('paths', {}).get('download_dir', ''))
        except ValidationError as e:
            errors.append(f"Invalid download directory: {str(e)}")
            
        try:
            Validator.validate_path(config.get('paths', {}).get('output_dir', ''))
        except ValidationError as e:
            errors.append(f"Invalid output directory: {str(e)}")

        # Validate stem names
        stems = config.get('processing', {}).get('stems', [])
        for stem in stems:
            if not Validator.validate_stem_name(stem):
                errors.append(f"Invalid stem name: {stem}")

        # Validate separator choice
        separator = config.get('processing', {}).get('separator', '')
        if separator not in ['demucs', 'spleeter']:
            errors.append(f"Invalid separator: {separator}")

        return errors
