import pytest
from pathlib import Path
from src.renderer.engine import RenderEngine

def test_render_minimal_template():
    """Test rendering minimal template."""
    engine = RenderEngine()
    segments = [
        {"type": "title", "text": "Test Title"},
        {"type": "content", "text": "Test content"},
    ]

    html = engine.render(segments, template="minimal")

    assert "<!DOCTYPE html>" in html
    assert "Test Title" in html
    assert "Test content" in html
    assert "minimal" in html

def test_render_with_invalid_template_fallback():
    """Test that invalid template falls back to default."""
    engine = RenderEngine()
    segments = [{"type": "title", "text": "Title"}]

    # Should fall back to tech_modern (default)
    html = engine.render(segments, template="nonexistent")

    assert "<!DOCTYPE html>" in html

def test_render_empty_segments_raises():
    """Test that empty segments raises error."""
    engine = RenderEngine()

    with pytest.raises(ValueError):
        engine.render([], template="minimal")
