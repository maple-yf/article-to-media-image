from pathlib import Path
from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from ..config import Settings
from .context import build_template_context
from ..utils.validator import validate_segments


class RenderEngine:
    """HTML template rendering engine."""

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the render engine.

        Args:
            settings: Optional settings instance
        """
        self.settings = settings or Settings()
        self._jinja_env = self._create_jinja_environment()

    def _create_jinja_environment(self) -> Environment:
        """Create Jinja2 environment with template directory."""
        template_dir = Path(__file__).parent / "templates"

        return Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=False,
        )

    def _get_template_path(self, template_name: str) -> str:
        """
        Get Jinja2 template path.

        Args:
            template_name: Name of the template

        Returns:
            Template path for Jinja2 (e.g., "minimal/template.html")
        """
        # Check if template exists
        if template_name not in self.settings.available_templates:
            # Fall back to default
            template_name = self.settings.default_template

        return f"{template_name}/template.html"

    def render(self, segments: List[Dict[str, Any]], template: str) -> str:
        """
        Render segments to HTML.

        Args:
            segments: List of segment dictionaries
            template: Template name to use

        Returns:
            Rendered HTML string

        Raises:
            ValueError: If segments is empty or invalid
        """
        # Validate input
        if not segments:
            raise ValueError("Cannot render empty segments")

        segments = validate_segments(segments)

        # Build context
        context = build_template_context(segments, template)

        # Get template path
        template_path = self._get_template_path(template)

        # Render
        jinja_template = self._jinja_env.get_template(template_path)
        return jinja_template.render(**context)
