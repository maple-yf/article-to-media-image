import pytest
from src.config.settings import Settings, get_default_config_path

def test_get_default_config_path():
    """Test that default config path is correctly constructed."""
    path = get_default_config_path()
    assert str(path).endswith(".article-to-media-image/config.yaml")

def test_settings_with_defaults():
    """Test Settings loads with default values when no config file exists."""
    settings = Settings()
    assert settings.default_template == "tech_modern"
    assert str(settings.output_base_dir).endswith("article-cards")

def test_settings_output_path_generation():
    """Test output path is generated with timestamp and template."""
    settings = Settings()
    output_path = settings.get_output_path(template="minimal")
    assert "minimal" in str(output_path)
    assert str(output_path).endswith(".html")
