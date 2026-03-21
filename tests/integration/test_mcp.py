import pytest
from pathlib import Path
from src.renderer.engine import RenderEngine
from src.config import Settings

def test_full_render_flow(tmp_path):
    """Test full rendering flow from segments to file."""
    settings = Settings()
    engine = RenderEngine(settings)

    segments = [
        {"type": "title", "text": "Integration Test"},
        {"type": "content", "text": "This is a test content."},
        {"type": "highlight", "text": "Key point here"},
    ]

    output_path = tmp_path / "test-output.html"
    result = engine.render_to_file(segments, "minimal", output_path)

    assert result == output_path
    assert result.exists()
    content = result.read_text()
    assert "Integration Test" in content
    assert "This is a test content" in content
