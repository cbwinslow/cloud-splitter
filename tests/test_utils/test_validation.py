import pytest
from pathlib import Path
from cloud_splitter.utils.validation import Validator, ValidationError

def test_url_validation():
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://soundcloud.com/artist/track",
    ]
    invalid_urls = [
        "not_a_url",
        "http://invalid.domain/video",
        "ftp://youtube.com/video",
    ]
    
    for url in valid_urls:
        assert Validator.validate_url(url)
    
    for url in invalid_urls:
        assert not Validator.validate_url(url)

def test_path_validation(tmp_path):
    valid_path = tmp_path / "test"
    valid_path.mkdir()
    
    assert Validator.validate_path(valid_path) == valid_path
    
    with pytest.raises(ValidationError):
        Validator.validate_path("/nonexistent/path")

def test_stem_name_validation():
    valid_names = ["vocals", "drums_1", "lead-guitar", "bass"]
    invalid_names = ["vocals!", "drums/cymbals", "guitar*2"]
    
    for name in valid_names:
        assert Validator.validate_stem_name(name)
    
    for name in invalid_names:
        assert not Validator.validate_stem_name(name)

def test_validate_urls():
    urls = [
        "https://www.youtube.com/watch?v=valid1",
        "not_a_url",
        "https://youtu.be/valid2",
        "invalid_url_2"
    ]
    
    valid, invalid = Validator.validate_urls(urls)
    assert len(valid) == 2
    assert len(invalid) == 2
    assert "not_a_url" in invalid
    assert "https://youtu.be/valid2" in valid
