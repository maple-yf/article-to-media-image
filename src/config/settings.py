import os
from pathlib import Path
from datetime import datetime
import yaml
from typing import Optional

DEFAULT_CONFIG_DIR = Path.home() / ".article-to-media-image"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"


def get_default_config_path() -> Path:
    """Get the default config file path."""
    return DEFAULT_CONFIG_FILE


def expand_path(path: str) -> Path:
    """Expand ~ and environment variables in path."""
    return Path(os.path.expandvars(os.path.expanduser(path)))


class Settings:
    """Configuration management for article-to-media-image."""

    def __init__(self, config_path: Optional[Path] = None):
        """Load settings from config file or use defaults."""
        self.config_path = config_path or DEFAULT_CONFIG_FILE
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """Load config from file or return defaults."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f) or {}
        return self._get_defaults()

    def _get_defaults(self) -> dict:
        """Get default configuration."""
        default_config_file = Path(__file__).parent / "default_config.yaml"
        if default_config_file.exists():
            with open(default_config_file, "r") as f:
                return yaml.safe_load(f)
        return {
            "defaults": {"template": "tech_modern"},
            "output": {"base_dir": "~/article-cards", "filename_template": "{timestamp}-{template}.html"},
            "templates": {"available": ["minimal", "gradient", "card", "dark", "tech_modern"]},
        }

    @property
    def default_template(self) -> str:
        return self._config.get("defaults", {}).get("template", "tech_modern")

    @property
    def output_base_dir(self) -> Path:
        path_str = self._config.get("output", {}).get("base_dir", "~/article-cards")
        return expand_path(path_str)

    @property
    def available_templates(self) -> list[str]:
        return self._config.get("templates", {}).get("available", ["tech_modern"])

    def get_output_path(self, template: str, output_path: Optional[str] = None) -> Path:
        """Generate output path for HTML file."""
        if output_path:
            return expand_path(output_path)

        # Ensure output directory exists
        self.output_base_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime(self._config.get("defaults", {}).get("timestamp_format", "%Y%m%d-%H%M%S"))
        filename_template = self._config.get("output", {}).get("filename_template", "{timestamp}-{template}.html")
        filename = filename_template.format(timestamp=timestamp, template=template)

        return self.output_base_dir / filename
