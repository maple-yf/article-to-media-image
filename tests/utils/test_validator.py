import pytest
from src.utils.validator import validate_segments, ValidationError

def test_validate_segments_with_valid_data():
    """Test validation passes with valid segments."""
    segments = [
        {"type": "title", "text": "Test Title"},
        {"type": "content", "text": "Test content"},
    ]
    assert validate_segments(segments) == segments

def test_validate_segments_empty():
    """Test validation fails with empty segments."""
    with pytest.raises(ValidationError, match="Segments cannot be empty"):
        validate_segments([])

def test_validate_segments_missing_type():
    """Test validation fails when segment missing type."""
    with pytest.raises(ValidationError, match="Missing required field"):
        validate_segments([{"text": "No type"}])

def test_validate_segments_missing_text():
    """Test validation fails when segment missing text."""
    with pytest.raises(ValidationError, match="Missing required field"):
        validate_segments([{"type": "title"}])

def test_validate_segments_invalid_type():
    """Test validation fails with invalid segment type."""
    with pytest.raises(ValidationError, match="Invalid segment type"):
        validate_segments([{"type": "invalid", "text": "Test"}])

def test_validate_segments_text_too_long():
    """Test validation fails when text exceeds max length."""
    long_text = "a" * 1001
    with pytest.raises(ValidationError, match="Text too long"):
        validate_segments([{"type": "content", "text": long_text}])
