import pytest
from cloud_splitter.utils.naming import FileNaming

def test_sanitize_filename():
    test_cases = [
        ("file/with\\invalid:chars", "filewithinvalidchars"),
        ("  spaces  everywhere  ", "spaces everywhere"),
        ('file"with"quotes', "filewithquotes"),
        ("normal_file_name", "normal_file_name"),
    ]
    
    for input_name, expected in test_cases:
        assert FileNaming.sanitize_filename(input_name) == expected

def test_extract_artist_title():
    test_cases = [
        ("Artist - Title", ("Artist", "Title")),
        ('Artist "Song Title"', ("Artist", "Song Title")),
        ("Artist: Song Name", ("Artist", "Song Name")),
        ("Just a Title", (None, "Just a Title")),
    ]
    
    for input_title, expected in test_cases:
        assert FileNaming.extract_artist_title(input_title) == expected

def test_deduplicate_artist():
    test_cases = [
        (
            "Artist Name",
            "Artist Name - Song Title",
            ("Artist Name", "Song Title")
        ),
        (
            "Band",
            "Song Title (Band)",
            ("Band", "Song Title")
        ),
        (
            "Artist",
            "Different Song",
            ("Artist", "Different Song")
        ),
    ]
    
    for artist, title, expected in test_cases:
        assert FileNaming.deduplicate_artist(artist, title) == expected

def test_generate_output_filename():
    test_cases = [
        (
            {"title": "Song", "artist": "Artist", "stem_type": "vocals"},
            "Artist - Song - vocals"
        ),
        (
            {"title": "Song", "artist": None, "stem_type": "drums"},
            "Song - drums"
        ),
        (
            {"title": "Song", "artist": "Artist"},
            "Artist - Song"
        ),
    ]
    
    for inputs, expected in test_cases:
        assert FileNaming.generate_output_filename(**inputs) == expected
