import pytest
from src.renderer.context import build_template_context

def test_build_context_basic():
    """Test basic context building."""
    segments = [
        {"type": "title", "text": "My Article"},
        {"type": "content", "text": "Some content"},
    ]
    context = build_template_context(segments, template_name="minimal")

    assert context["template_name"] == "minimal"
    assert context["total_cards"] == 2
    assert len(context["segments"]) == 2
    assert context["segments"][0]["index"] == 1
    assert context["segments"][0]["is_first"] == True
    assert context["segments"][0]["is_last"] == False

def test_build_context_single_segment():
    """Test context with single segment."""
    segments = [{"type": "title", "text": "Title"}]
    context = build_template_context(segments, template_name="card")

    assert context["total_cards"] == 1
    assert context["segments"][0]["is_first"] == True
    assert context["segments"][0]["is_last"] == True

def test_build_context_includes_metadata():
    """Test context includes generated metadata."""
    segments = [{"type": "content", "text": "Test"}]
    context = build_template_context(segments, template_name="dark")

    assert "generated_at" in context
    assert "version" in context
