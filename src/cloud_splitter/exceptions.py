class CloudSplitterError(Exception):
    """Base exception for cloud-splitter."""
    pass

class DownloadError(CloudSplitterError):
    """Raised when a download operation fails."""
    pass

class ProcessingError(CloudSplitterError):
    """Raised when an audio processing operation fails."""
    pass

class ConfigurationError(CloudSplitterError):
    """Raised when there's a configuration error."""
    pass

class ValidationError(CloudSplitterError):
    """Raised when validation fails."""
    pass

class StemSeparationError(ProcessingError):
    """Raised when stem separation fails."""
    pass
