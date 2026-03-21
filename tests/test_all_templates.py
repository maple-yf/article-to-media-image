import pytest
from src.renderer.engine import RenderEngine


@pytest.mark.parametrize("template", [
    "minimal",
    "gradient",
    "card",
    "dark",
    "tech_modern",
])
def test_all_templates_render(template):
    """Test that all templates render successfully."""
    engine = RenderEngine()
    segments = [
        {"type": "title", "text": f"{template.title()} Template Test"},
        {"type": "content", "text": "This is test content for the template."},
        {"type": "quote", "text": "A test quote"},
        {"type": "highlight", "text": "Key highlight"},
        {"type": "code", "text": "print('test')"},
    ]

    html = engine.render(segments, template)

    assert "<!DOCTYPE html>" in html
    assert f"{template.title()} Template Test" in html
    assert "This is test content" in html
