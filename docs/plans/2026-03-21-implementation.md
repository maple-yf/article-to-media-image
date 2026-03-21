# Article to Media Image Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个 MCP Skill，将 Agent 预处理的文章内容转换为可截图的竖版图卡 HTML 文件

**Architecture:**
- 使用 Python + MCP SDK 构建 Skill Server
- Jinja2 模板引擎渲染 5 种风格的 HTML 模板
- 配置文件管理默认输出路径和模板设置
- Agent 负责内容分析和分段，Skill 仅负责渲染

**Tech Stack:**
- Python 3.10+
- MCP Python SDK (`anthropic/mcp`)
- Jinja2 模板引擎
- PyYAML 配置管理

---

## Task 1: 项目初始化

**Files:**
- Create: `pyproject.toml`
- Create: `src/__init__.py`
- Create: `.gitignore` (update)
- Create: `README.md`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "article-to-media-image"
version = "0.1.0"
description = "MCP Skill to convert articles to shareable card images"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=0.1.0",
    "jinja2>=3.1.0",
    "pyyaml>=6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
article-to-media-image = "src.main:main"
```

**Step 2: Create src/__init__.py**

```python
"""Article to Media Image - MCP Skill."""

__version__ = "0.1.0"
```

**Step 3: Update .gitignore**

Add to existing `.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
ENV/

# Config
*.local.yaml

# Output
article-cards/
*.html
```

**Step 4: Create README.md**

```markdown
# Article to Media Image

MCP Skill to convert articles into shareable card images.

## Installation

```bash
pip install -e .
```

## Usage

Configure in your MCP client settings:

```json
{
  "mcpServers": {
    "article-to-media-image": {
      "command": "python",
      "args": ["-m", "src.main"]
    }
  }
}
```

## Templates

- `minimal` - Clean, minimalist design
- `gradient` - Warm gradient backgrounds
- `card` - Information card layout
- `dark` - Dark mode for developers
- `tech_modern` - Modern tech style

## Configuration

Default config: `~/.article-to-media-image/config.yaml`
```

**Step 5: Commit**

```bash
git add pyproject.toml src/__init__.py .gitignore README.md
git commit -m "feat: initialize project structure and configuration"
```

---

## Task 2: 配置管理模块

**Files:**
- Create: `src/config/__init__.py`
- Create: `src/config/settings.py`
- Create: `src/config/default_config.yaml`

**Step 1: Write failing test for config loading**

Create `tests/config/test_settings.py`:

```python
import pytest
from src.config.settings import Settings, get_default_config_path

def test_get_default_config_path():
    """Test that default config path is correctly constructed."""
    path = get_default_config_path()
    assert path.endswith(".article-to-media-image/config.yaml")

def test_settings_with_defaults():
    """Test Settings loads with default values when no config file exists."""
    settings = Settings()
    assert settings.default_template == "tech_modern"
    assert settings.output_base_dir.endswith("article-cards")

def test_settings_output_path_generation():
    """Test output path is generated with timestamp and template."""
    settings = Settings()
    output_path = settings.get_output_path(template="minimal")
    assert "minimal" in output_path
    assert output_path.endswith(".html")
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/config/test_settings.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'src.config'`

**Step 3: Create default config template**

Create `src/config/default_config.yaml`:

```yaml
defaults:
  template: tech_modern
  output_path: ~/article-cards/{timestamp}-{template}.html
  timestamp_format: "%Y%m%d-%H%M%S"

output:
  base_dir: ~/article-cards
  filename_template: "{timestamp}-{template}.html"

templates:
  available:
    - minimal
    - gradient
    - card
    - dark
    - tech_modern
```

**Step 4: Implement Settings class**

Create `src/config/settings.py`:

```python
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
```

**Step 5: Create config __init__.py**

Create `src/config/__init__.py`:

```python
"""Configuration management."""

from src.config.settings import Settings, get_default_config_path, expand_path

__all__ = ["Settings", "get_default_config_path", "expand_path"]
```

**Step 6: Run tests to verify they pass**

```bash
pytest tests/config/test_settings.py -v
```

Expected: PASS

**Step 7: Commit**

```bash
git add src/config/ tests/config/
git commit -m "feat: add configuration management module"
```

---

## Task 3: 输入验证模块

**Files:**
- Create: `src/utils/__init__.py`
- Create: `src/utils/validator.py`
- Create: `tests/utils/test_validator.py`

**Step 1: Write failing tests**

Create `tests/utils/test_validator.py`:

```python
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
    with pytest.raises(ValidationError, match="Segment text too long"):
        validate_segments([{"type": "content", "text": long_text}])
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/utils/test_validator.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Implement validator**

Create `src/utils/validator.py`:

```python
from typing import List, Dict, Any

# Valid segment types
VALID_SEGMENT_TYPES = {"title", "content", "quote", "code", "highlight"}

# Maximum text length per segment
MAX_TEXT_LENGTH = 1000


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


def validate_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validate input segments.

    Args:
        segments: List of segment dictionaries with 'type' and 'text' keys

    Returns:
        Validated segments

    Raises:
        ValidationError: If validation fails
    """
    if not segments:
        raise ValidationError("Segments cannot be empty")

    if not isinstance(segments, list):
        raise ValidationError("Segments must be a list")

    for i, segment in enumerate(segments):
        # Check required fields
        if "type" not in segment:
            raise ValidationError(f"Segment {i}: Missing required field 'type'")

        if "text" not in segment:
            raise ValidationError(f"Segment {i}: Missing required field 'text'")

        # Validate type
        if segment["type"] not in VALID_SEGMENT_TYPES:
            raise ValidationError(
                f"Segment {i}: Invalid segment type '{segment['type']}'. "
                f"Valid types: {', '.join(VALID_SEGMENT_TYPES)}"
            )

        # Validate text
        text = segment["text"]
        if not isinstance(text, str):
            raise ValidationError(f"Segment {i}: 'text' must be a string")

        if len(text) == 0:
            raise ValidationError(f"Segment {i}: 'text' cannot be empty")

        if len(text) > MAX_TEXT_LENGTH:
            raise ValidationError(
                f"Segment {i}: Text too long ({len(text)} chars). "
                f"Maximum: {MAX_TEXT_LENGTH} chars"
            )

    return segments
```

**Step 4: Create utils __init__.py**

Create `src/utils/__init__.py`:

```python
"""Utility modules."""

from src.utils.validator import validate_segments, ValidationError

__all__ = ["validate_segments", "ValidationError"]
```

**Step 5: Run tests to verify they pass**

```bash
pytest tests/utils/test_validator.py -v
```

Expected: PASS

**Step 6: Commit**

```bash
git add src/utils/ tests/utils/
git commit -m "feat: add input validation module"
```

---

## Task 4: 文件工具模块

**Files:**
- Create: `src/utils/file.py`
- Create: `tests/utils/test_file.py`

**Step 1: Write failing tests**

Create `tests/utils/test_file.py`:

```python
import pytest
from pathlib import Path
from src.utils.file import ensure_directory, write_html_file

def test_ensure_directory_creates_new_dir(tmp_path):
    """Test ensure_directory creates a new directory."""
    new_dir = tmp_path / "new" / "nested" / "dir"
    ensure_directory(new_dir)
    assert new_dir.exists()
    assert new_dir.is_dir()

def test_ensure_directory_handles_existing_dir(tmp_path):
    """Test ensure_directory doesn't fail on existing directory."""
    existing = tmp_path / "existing"
    existing.mkdir()
    ensure_directory(existing)  # Should not raise
    assert existing.exists()

def test_write_html_file(tmp_path):
    """Test writing HTML content to file."""
    output_path = tmp_path / "output.html"
    content = "<html><body>Test</body></html>"

    result_path = write_html_file(output_path, content)

    assert result_path == output_path
    assert result_path.exists()
    assert result_path.read_text() == content

def test_write_html_file_creates_parent_dirs(tmp_path):
    """Test write_html_file creates parent directories."""
    output_path = tmp_path / "nested" / "dir" / "output.html"
    content = "<html>Test</html>"

    result_path = write_html_file(output_path, content)

    assert result_path.exists()
    assert result_path.parent.exists()
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/utils/test_file.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Implement file utilities**

Create `src/utils/file.py`:

```python
from pathlib import Path


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists
    """
    path.mkdir(parents=True, exist_ok=True)


def write_html_file(output_path: Path, content: str) -> Path:
    """
    Write HTML content to a file.

    Args:
        output_path: Path to write the HTML file
        content: HTML content to write

    Returns:
        The path where the file was written
    """
    # Ensure parent directory exists
    ensure_directory(output_path.parent)

    # Write content
    output_path.write_text(content, encoding="utf-8")

    return output_path
```

**Step 4: Update utils __init__.py**

Update `src/utils/__init__.py`:

```python
"""Utility modules."""

from src.utils.validator import validate_segments, ValidationError
from src.utils.file import ensure_directory, write_html_file

__all__ = ["validate_segments", "ValidationError", "ensure_directory", "write_html_file"]
```

**Step 5: Run tests to verify they pass**

```bash
pytest tests/utils/test_file.py -v
```

Expected: PASS

**Step 6: Commit**

```bash
git add src/utils/file.py tests/utils/test_file.py src/utils/__init__.py
git commit -m "feat: add file utility module"
```

---

## Task 5: 模板上下文构建器

**Files:**
- Create: `src/renderer/context.py`
- Create: `tests/renderer/test_context.py`
- Create: `src/renderer/__init__.py`

**Step 1: Write failing tests**

Create `tests/renderer/test_context.py`:

```python
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
    from datetime import datetime
    segments = [{"type": "content", "text": "Test"}]
    context = build_template_context(segments, template_name="dark")

    assert "generated_at" in context
    assert "version" in context
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/renderer/test_context.py -v
```

Expected: FAIL with `ModuleNotFoundError`

**Step 3: Implement context builder**

Create `src/renderer/context.py`:

```python
from datetime import datetime
from typing import List, Dict, Any
from .. import __version__


def build_template_context(segments: List[Dict[str, Any]], template_name: str) -> Dict[str, Any]:
    """
    Build template context for rendering.

    Args:
        segments: Validated segment list
        template_name: Name of the template being used

    Returns:
        Template context dictionary
    """
    total_cards = len(segments)

    enriched_segments = []
    for i, segment in enumerate(segments):
        enriched_segments.append({
            **segment,
            "index": i + 1,
            "is_first": i == 0,
            "is_last": i == total_cards - 1,
        })

    return {
        "segments": enriched_segments,
        "total_cards": total_cards,
        "template_name": template_name,
        "generated_at": datetime.now().isoformat(),
        "version": __version__,
    }
```

**Step 4: Create renderer __init__.py**

Create `src/renderer/__init__.py`:

```python
"""Template rendering engine."""

from src.renderer.context import build_template_context
from src.renderer.engine import RenderEngine

__all__ = ["build_template_context", "RenderEngine"]
```

**Step 5: Run tests to verify they pass**

```bash
pytest tests/renderer/test_context.py -v
```

Expected: PASS

**Step 6: Commit**

```bash
git add src/renderer/ tests/renderer/
git commit -m "feat: add template context builder"
```

---

## Task 6: 渲染引擎核心

**Files:**
- Modify: `src/renderer/engine.py`
- Modify: `tests/renderer/test_engine.py`

**Step 1: Write failing tests**

Add to `tests/renderer/test_engine.py`:

```python
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
        engine.render([])
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/renderer/test_engine.py -v
```

Expected: FAIL with no engine module

**Step 3: Implement RenderEngine**

Create `src/renderer/engine.py`:

```python
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
```

**Step 4: Run tests to verify they fail (no templates yet)**

```bash
pytest tests/renderer/test_engine.py -v
```

Expected: FAIL with `TemplateNotFound` - we haven't created templates yet, which is expected. We'll create templates in next tasks.

**Step 5: Commit engine code**

```bash
git add src/renderer/engine.py tests/renderer/test_engine.py
git commit -m "feat: add render engine core"
```

---

## Task 7: Minimal 模板

**Files:**
- Create: `src/renderer/templates/minimal/template.html`
- Create: `src/renderer/templates/minimal/style.css`

**Step 1: Create minimal template HTML**

Create `src/renderer/templates/minimal/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Cards - {{ template_name }}</title>
    <style>
        {% include 'minimal/style.css' %}
    </style>
</head>
<body>
    <div class="container">
        {% for segment in segments %}
        <div class="card {% if segment.is_first %}card-first{% endif %} {% if segment.is_last %}card-last{% endif %}">
            {% if segment.type == 'title' %}
            <div class="card-title">
                <span class="card-index">0{{ segment.index }}</span>
                <h1>{{ segment.text }}</h1>
            </div>
            {% elif segment.type == 'content' %}
            <div class="card-content">
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'quote' %}
            <div class="card-quote">
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'highlight' %}
            <div class="card-highlight">
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'code' %}
            <div class="card-code">
                <pre><code>{{ segment.text }}</code></pre>
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
```

**Step 2: Create minimal template CSS**

Create `src/renderer/templates/minimal/style.css`:

```css
/* Minimal Template - Less is More */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --bg-primary: #FFFFFF;
    --bg-secondary: #F8FAFC;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-tertiary: #94A3B8;
    --border-light: #E2E8F0;
    --accent: #3B82F6;
    --accent-light: #DBEAFE;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
    background: var(--bg-secondary);
    color: var(--text-primary);
    line-height: 1.6;
    padding: 40px 20px;
}

.container {
    max-width: 420px;
    margin: 0 auto;
}

/* Card Base */
.card {
    background: var(--bg-primary);
    border: 1px solid var(--border-light);
    border-radius: 8px;
    padding: 60px 40px;
    margin-bottom: 24px;
    aspect-ratio: 3/4;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* Title Card */
.card-title {
    text-align: center;
}

.card-index {
    display: block;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-tertiary);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 24px;
}

.card-title h1 {
    font-size: 42px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

/* Content Card */
.card-content p {
    font-size: 18px;
    color: var(--text-secondary);
    line-height: 1.8;
}

/* Quote Card */
.card-quote {
    border-left: 4px solid var(--accent);
    background: var(--accent-light);
    padding: 32px;
}

.card-quote p {
    font-size: 17px;
    font-style: italic;
    color: var(--text-primary);
}

/* Highlight Card */
.card-highlight p {
    font-size: 20px;
    font-weight: 600;
    color: var(--accent);
}

/* Code Card */
.card-code {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 8px;
    padding: 24px;
}

.card-code pre {
    margin: 0;
    overflow-x: auto;
}

.card-code code {
    font-family: 'Courier New', monospace;
    font-size: 15px;
    color: var(--text-secondary);
}
```

**Step 3: Test minimal template rendering**

```bash
python -c "
from src.renderer.engine import RenderEngine
engine = RenderEngine()
segments = [{'type': 'title', 'text': 'Test'}, {'type': 'content', 'text': 'Content'}]
html = engine.render(segments, 'minimal')
print('Minimal template renders successfully')
"
```

Expected: Success message

**Step 4: Commit**

```bash
git add src/renderer/templates/minimal/
git commit -m "feat: add minimal template"
```

---

## Task 8: Gradient 模板

**Files:**
- Create: `src/renderer/templates/gradient/template.html`
- Create: `src/renderer/templates/gradient/style.css`

**Step 1: Create gradient template HTML**

Create `src/renderer/templates/gradient/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Cards - {{ template_name }}</title>
    <style>
        {% include 'gradient/style.css' %}
    </style>
</head>
<body>
    {% for segment in segments %}
    <div class="card-container gradient-{{ segment.index % 4 }}">
        <div class="card">
            <div class="card-badge">
                <span>{{ '{:02d}'.format(segment.index) }}</span>
            </div>
            {% if segment.type == 'title' %}
            <div class="card-title">
                <h1>{{ segment.text }}</h1>
                <div class="divider"></div>
            </div>
            {% elif segment.type == 'content' %}
            <div class="card-content">
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'quote' %}
            <div class="card-quote">
                <span class="quote-mark">"</span>
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'highlight' %}
            <div class="card-highlight">
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'code' %}
            <div class="card-code">
                <pre><code>{{ segment.text }}</code></pre>
            </div>
            {% endif %}
            <div class="card-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
    {% endfor %}
</body>
</html>
```

**Step 2: Create gradient template CSS**

Create `src/renderer/templates/gradient/style.css`:

```css
/* Gradient Template - Warm Flow */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --text-dark: #1E293B;
    --text-medium: #475569;
    --text-light: #64748B;
    --card-bg: rgba(255, 255, 255, 0.85);
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
    line-height: 1.6;
}

.card-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
}

/* Gradient backgrounds */
.gradient-0 {
    background: linear-gradient(135deg, #FFEDD5 0%, #FED7AA 50%, #FDBA74 100%);
}

.gradient-1 {
    background: linear-gradient(135deg, #FAE8FF 0%, #F0ABFC 50%, #E879F9 100%);
}

.gradient-2 {
    background: linear-gradient(135deg, #ECFDF5 0%, #A7F3D0 50%, #6EE7B7 100%);
}

.gradient-3 {
    background: linear-gradient(135deg, #E0F2FE 0%, #7DD3FC 50%, #38BDF8 100%);
}

.card {
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 24px;
    padding: 48px;
    max-width: 480px;
    width: 100%;
    aspect-ratio: 3/4;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04);
}

.card-badge {
    align-self: center;
    margin-bottom: 24px;
}

.card-badge span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    font-size: 18px;
    font-weight: 700;
    color: var(--text-dark);
}

/* Title Card */
.card-title {
    text-align: center;
}

.card-title h1 {
    font-size: 42px;
    font-weight: 700;
    color: var(--text-dark);
    line-height: 1.2;
    margin-bottom: 24px;
}

.divider {
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, rgba(0,0,0,0.2) 50%, transparent 100%);
    border-radius: 2px;
    margin: 0 auto;
    width: 120px;
}

/* Content Card */
.card-content {
    text-align: center;
}

.card-content p {
    font-size: 18px;
    color: var(--text-dark);
    line-height: 1.8;
}

/* Quote Card */
.card-quote {
    text-align: center;
    position: relative;
}

.quote-mark {
    display: block;
    font-size: 64px;
    color: rgba(0, 0, 0, 0.1);
    font-weight: 700;
    line-height: 1;
    margin-bottom: 16px;
}

.card-quote p {
    font-size: 20px;
    font-style: italic;
    color: var(--text-dark);
}

/* Highlight Card */
.card-highlight {
    text-align: center;
}

.card-highlight p {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-dark);
}

/* Code Card */
.card-code {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 12px;
    padding: 20px;
    overflow: hidden;
}

.card-code pre {
    margin: 0;
}

.card-code code {
    font-family: 'Courier New', monospace;
    font-size: 14px;
    color: var(--text-dark);
}

/* Card dots */
.card-dots {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 32px;
}

.card-dots span {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.1);
}
```

**Step 3: Test gradient template rendering**

```bash
python -c "
from src.renderer.engine import RenderEngine
engine = RenderEngine()
segments = [{'type': 'title', 'text': 'Gradient Test'}, {'type': 'content', 'text': 'Beautiful gradients!'}]
html = engine.render(segments, 'gradient')
print('Gradient template renders successfully')
"
```

**Step 4: Commit**

```bash
git add src/renderer/templates/gradient/
git commit -m "feat: add gradient template"
```

---

## Task 9: Card 模板

**Files:**
- Create: `src/renderer/templates/card/template.html`
- Create: `src/renderer/templates/card/style.css`

**Step 1: Create card template HTML**

Create `src/renderer/templates/card/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Cards - {{ template_name }}</title>
    <style>
        {% include 'card/style.css' %}
    </style>
</head>
<body>
    <div class="container">
        {% for segment in segments %}
        <div class="card {% if segment.is_first %}card-main{% else %}card-alt{% endif %}">
            <div class="card-indicator"></div>
            <div class="card-number">{{ segment.index }}</div>
            <div class="card-content">
                {% if segment.type == 'title' %}
                <div class="card-header-bar"></div>
                <h1 class="card-title">{{ segment.text }}</h1>
                <div class="card-meta">
                    <span>Article Cards</span>
                    <span>•</span>
                    <span>{{ total_cards }} cards</span>
                </div>
                {% elif segment.type == 'content' %}
                <p>{{ segment.text }}</p>
                {% elif segment.type == 'quote' %}
                <div class="card-quote">
                    <span class="quote-icon">"</span>
                    <p>{{ segment.text }}</p>
                </div>
                {% elif segment.type == 'highlight' %}
                <div class="card-highlight">
                    <span class="highlight-badge">Key Point</span>
                    <p>{{ segment.text }}</p>
                </div>
                {% elif segment.type == 'code' %}
                <div class="card-code">
                    <div class="code-header">
                        <span class="code-lang">code</span>
                    </div>
                    <pre><code>{{ segment.text }}</code></pre>
                </div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
```

**Step 2: Create card template CSS**

Create `src/renderer/templates/card/style.css`:

```css
/* Card Template - Information Block */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #059669;
    --primary-light: #D1FAE5;
    --primary-dark: #047857;
    --bg-page: #F1F5F9;
    --bg-card: #FFFFFF;
    --bg-card-alt: #F8FAFC;
    --text-primary: #1E293B;
    --text-secondary: #64748B;
    --border: #E2E8F0;
    --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
    background: var(--bg-page);
    color: var(--text-primary);
    line-height: 1.6;
    padding: 40px 20px;
}

.container {
    max-width: 460px;
    margin: 0 auto;
}

.card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 24px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    aspect-ratio: 3/4;
    display: flex;
    flex-direction: column;
    position: relative;
}

.card-alt {
    background: var(--bg-card-alt);
}

.card-indicator {
    position: absolute;
    left: 0;
    top: 40px;
    bottom: 40px;
    width: 4px;
    background: var(--primary);
    border-radius: 0 4px 4px 0;
}

.card-number {
    position: absolute;
    top: 40px;
    right: 40px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--bg-card-alt);
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 20px;
}

/* Title Card */
.card-header-bar {
    height: 4px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 2px;
    margin-bottom: 32px;
}

.card-title {
    font-size: 38px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
    margin-bottom: 24px;
}

.card-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: var(--text-secondary);
}

/* Content Card */
.card-content p {
    font-size: 17px;
    color: var(--text-secondary);
    line-height: 1.8;
}

/* Quote Card */
.card-quote {
    position: relative;
    padding-left: 48px;
}

.quote-icon {
    position: absolute;
    left: 0;
    top: 0;
    font-size: 48px;
    color: var(--primary);
    opacity: 0.3;
    line-height: 1;
}

.card-quote p {
    font-size: 18px;
    font-style: italic;
    color: var(--text-primary);
}

/* Highlight Card */
.card-highlight {
    background: var(--primary-light);
    border-radius: 12px;
    padding: 24px;
}

.highlight-badge {
    display: inline-block;
    padding: 4px 12px;
    background: var(--primary);
    color: white;
    font-size: 12px;
    font-weight: 600;
    border-radius: 12px;
    margin-bottom: 12px;
}

.card-highlight p {
    font-size: 18px;
    font-weight: 600;
    color: var(--primary-dark);
}

/* Code Card */
.card-code {
    background: var(--bg-card-alt);
    border-radius: 12px;
    overflow: hidden;
}

.code-header {
    padding: 12px 16px;
    background: var(--bg-page);
    border-bottom: 1px solid var(--border);
}

.code-lang {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
}

.card-code pre {
    padding: 16px;
    margin: 0;
}

.card-code code {
    font-family: 'Courier New', monospace;
    font-size: 14px;
    color: var(--text-primary);
}
```

**Step 3: Test card template rendering**

```bash
python -c "
from src.renderer.engine import RenderEngine
engine = RenderEngine()
segments = [{'type': 'title', 'text': 'Card Test'}, {'type': 'content', 'text': 'Structured content!'}]
html = engine.render(segments, 'card')
print('Card template renders successfully')
"
```

**Step 4: Commit**

```bash
git add src/renderer/templates/card/
git commit -m "feat: add card template"
```

---

## Task 10: Dark 模板

**Files:**
- Create: `src/renderer/templates/dark/template.html`
- Create: `src/renderer/templates/dark/style.css`

**Step 1: Create dark template HTML**

Create `src/renderer/templates/dark/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Cards - {{ template_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        {% include 'dark/style.css' %}
    </style>
</head>
<body>
    <div class="container">
        {% for segment in segments %}
        <div class="card {% if segment.is_first %}card-glow{% endif %}">
            <div class="card-index">// {{ '{:02d}'.format(segment.index) }}</div>
            {% if segment.type == 'title' %}
            <div class="card-header"></div>
            <div class="card-title">
                <span class="comment">/** Article Title */</span>
                <h1>{{ segment.text }}</h1>
            </div>
            {% elif segment.type == 'content' %}
            <div class="card-content">
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'quote' %}
            <div class="card-quote">
                <span class="quote-bracket">"</span>
                <p>{{ segment.text }}</p>
            </div>
            {% elif segment.type == 'highlight' %}
            <div class="card-highlight">
                <span class="highlight-keyword">const</span>
                <span class="highlight-var">highlight</span>
                <span class="highlight-operator">=</span>
                <span class="highlight-string">"{{ segment.text }}"</span>
                <span class="syntax-semicolon">;</span>
            </div>
            {% elif segment.type == 'code' %}
            <div class="card-code">
                <div class="terminal-header">
                    <span class="dot dot-red"></span>
                    <span class="dot dot-yellow"></span>
                    <span class="dot dot-green"></span>
                </div>
                <pre><code>{{ segment.text }}</code></pre>
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
```

**Step 2: Create dark template CSS**

Create `src/renderer/templates/dark/style.css`:

```css
/* Dark Template - Night Coding */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --bg-deep: #0D1117;
    --bg-card: #161B22;
    --bg-card-hover: #1C2128;
    --bg-elevated: #21262D;
    --text-primary: #F0F6FC;
    --text-secondary: #8B949E;
    --text-tertiary: #6E7681;
    --syntax-keyword: #FF7B72;
    --syntax-string: #A5D6FF;
    --syntax-function: #D2A8FF;
    --syntax-variable: #FFA657;
    --syntax-comment: #8B949E;
    --accent-blue: #58A6FF;
    --accent-green: #3FB950;
    --border: #30363D;
    --shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 20px rgba(88, 166, 255, 0.15);
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
    background: var(--bg-deep);
    color: var(--text-primary);
    line-height: 1.6;
    padding: 40px 20px;
}

.container {
    max-width: 460px;
    margin: 0 auto;
}

.card {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 36px;
    margin-bottom: 24px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    aspect-ratio: 3/4;
    display: flex;
    flex-direction: column;
    position: relative;
}

.card-glow {
    box-shadow: var(--shadow), var(--shadow-glow);
    border-color: var(--accent-blue);
}

.card:hover {
    background: var(--bg-card-hover);
}

.card-index {
    position: absolute;
    top: 20px;
    left: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--text-tertiary);
}

/* Title Card */
.card-header {
    height: 3px;
    background: linear-gradient(90deg,
        var(--syntax-keyword) 0%,
        var(--syntax-string) 50%,
        var(--syntax-function) 100%);
    border-radius: 2px;
    margin-bottom: 32px;
}

.card-title {
    text-align: center;
}

.comment {
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--syntax-comment);
    font-style: italic;
    margin-bottom: 16px;
}

.card-title h1 {
    font-size: 40px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

/* Content Card */
.card-content p {
    font-size: 17px;
    color: var(--text-secondary);
    line-height: 1.8;
}

/* Quote Card */
.card-quote {
    border-left: 3px solid var(--accent-blue);
    padding-left: 24px;
}

.quote-bracket {
    display: block;
    font-size: 48px;
    color: var(--accent-blue);
    opacity: 0.5;
    line-height: 1;
    margin-bottom: 8px;
}

.card-quote p {
    font-size: 18px;
    font-style: italic;
    color: var(--text-primary);
}

/* Highlight Card */
.card-highlight {
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg-elevated);
    border-radius: 8px;
    padding: 20px;
}

.highlight-keyword {
    color: var(--syntax-keyword);
}

.highlight-var {
    color: var(--syntax-variable);
}

.highlight-operator {
    color: var(--accent-blue);
}

.highlight-string {
    color: var(--syntax-string);
}

.syntax-semicolon {
    color: var(--text-secondary);
}

/* Code Card */
.card-code {
    background: var(--bg-deep);
    border-radius: 8px;
    overflow: hidden;
}

.terminal-header {
    display: flex;
    gap: 8px;
    padding: 12px;
    background: var(--bg-elevated);
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.dot-red { background: #FF5F56; }
.dot-yellow { background: #FFBD2E; }
.dot-green { background: #27C93F; }

.card-code pre {
    padding: 16px;
    margin: 0;
}

.card-code code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    color: var(--text-secondary);
}
```

**Step 3: Test dark template rendering**

```bash
python -c "
from src.renderer.engine import RenderEngine
engine = RenderEngine()
segments = [{'type': 'title', 'text': 'Dark Mode Test'}, {'type': 'content', 'text': 'Easy on the eyes!'}]
html = engine.render(segments, 'dark')
print('Dark template renders successfully')
"
```

**Step 4: Commit**

```bash
git add src/renderer/templates/dark/
git commit -m "feat: add dark template"
```

---

## Task 11: Tech Modern 模板

**Files:**
- Create: `src/renderer/templates/tech_modern/template.html`
- Create: `src/renderer/templates/tech_modern/style.css`

**Step 1: Create tech_modern template HTML**

Create `src/renderer/templates/tech_modern/template.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Cards - {{ template_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        {% include 'tech_modern/style.css' %}
    </style>
</head>
<body>
    <div class="container">
        {% for segment in segments %}
        <div class="card {% if segment.is_first %}card-hero{% endif %}">
            {% if segment.is_first %}
            <div class="hero-badge">
                <span class="badge-dot"></span>
                <span>ARTICLE</span>
            </div>
            {% endif %}
            <div class="card-content-inner">
                {% if segment.type == 'title' %}
                <h1 class="hero-title">{{ segment.text }}</h1>
                <div class="hero-meta">
                    <span class="meta-tag">{{ total_cards }} sections</span>
                    <span class="meta-separator">•</span>
                    <span class="meta-tag">Generated with AI</span>
                </div>
                {% elif segment.type == 'content' %}
                <p class="body-text">{{ segment.text }}</p>
                {% elif segment.type == 'quote' %}
                <div class="quote-block">
                    <span class="quote-line"></span>
                    <p>{{ segment.text }}</p>
                </div>
                {% elif segment.type == 'highlight' %}
                <div class="highlight-box">
                    <span class="highlight-icon">⚡</span>
                    <p>{{ segment.text }}</p>
                </div>
                {% elif segment.type == 'code' %}
                <div class="code-block">
                    <div class="code-window">
                        <span class="window-dot"></span>
                        <span class="window-dot"></span>
                    </div>
                    <pre><code>{{ segment.text }}</code></pre>
                </div>
                {% endif %}
            </div>
            {% if not segment.is_last %}
            <div class="card-connector">
                <span></span>
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
```

**Step 2: Create tech_modern template CSS**

Create `src/renderer/templates/tech_modern/style.css`:

```css
/* Tech Modern Template - Professional Tech Style */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #0EA5E9;
    --accent: #38BDF8;
    --deep-blue: #0284C7;
    --dark-blue: #0369A1;
    --dark: #0F172A;
    --dark-bg-light: #1E293B;
    --success: #22C55E;
    --warning-orange: #F59E0B;
    --text-primary: #1E293B;
    --text-secondary: #64748B;
    --bg-light-blue: #F0F9FF;
    --border-light: #BAE6FD;
}

body {
    font-family: 'Inter', 'Noto Sans SC', -apple-system, sans-serif;
    background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
    padding: 40px 20px;
}

.container {
    max-width: 480px;
    margin: 0 auto;
}

.card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 20px;
    padding: 48px;
    margin-bottom: 24px;
    aspect-ratio: 3/4;
    display: flex;
    flex-direction: column;
    box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
}

.card-hero {
    background: linear-gradient(135deg, var(--dark) 0%, var(--dark-bg-light) 100%);
    border: none;
}

.card-hero::before {
    background: linear-gradient(90deg, var(--success), var(--primary), var(--warning-orange));
}

/* Hero Badge */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    margin-bottom: 24px;
    align-self: flex-start;
}

.badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--success);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.1); }
}

.hero-badge span:last-child {
    color: rgba(255, 255, 255, 0.8);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
}

/* Card Content */
.card-content-inner {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* Hero Title */
.hero-title {
    font-size: 48px;
    font-weight: 900;
    color: white;
    line-height: 1.1;
    margin-bottom: 24px;
}

.hero-meta {
    display: flex;
    align-items: center;
    gap: 12px;
}

.meta-tag {
    padding: 6px 14px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    font-size: 13px;
    font-weight: 500;
    color: var(--accent);
}

.meta-separator {
    color: rgba(255, 255, 255, 0.3);
}

/* Body Text (for non-hero cards) */
.body-text {
    font-size: 18px;
    color: var(--text-primary);
    line-height: 1.8;
}

/* Quote Block */
.quote-block {
    position: relative;
    padding-left: 24px;
}

.quote-line {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--primary), var(--accent));
    border-radius: 2px;
}

.quote-block p {
    font-size: 20px;
    font-weight: 600;
    color: var(--dark-blue);
}

/* Highlight Box */
.highlight-box {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 24px;
    background: var(--bg-light-blue);
    border-radius: 16px;
    border: 1px solid var(--border-light);
}

.highlight-icon {
    font-size: 24px;
    flex-shrink: 0;
}

.highlight-box p {
    font-size: 17px;
    font-weight: 600;
    color: var(--deep-blue);
}

/* Code Block */
.code-block {
    background: var(--dark);
    border-radius: 12px;
    overflow: hidden;
}

.code-window {
    display: flex;
    gap: 6px;
    padding: 12px;
    background: var(--dark-bg-light);
}

.window-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.window-dot:nth-child(1) { background: #FF5F56; }
.window-dot:nth-child(2) { background: #FFBD2E; }

.code-block pre {
    padding: 16px;
    margin: 0;
}

.code-block code {
    font-family: 'Courier New', monospace;
    font-size: 14px;
    color: var(--accent);
}

/* Card Connector */
.card-connector {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.card-connector span {
    width: 2px;
    height: 16px;
    background: linear-gradient(180deg, var(--primary), transparent);
    border-radius: 1px;
}
```

**Step 3: Test tech_modern template rendering**

```bash
python -c "
from src.renderer.engine import RenderEngine
engine = RenderEngine()
segments = [{'type': 'title', 'text': 'Tech Modern Test'}, {'type': 'content', 'text': 'Modern tech style!'}]
html = engine.render(segments, 'tech_modern')
print('Tech Modern template renders successfully')
"
```

**Step 4: Commit**

```bash
git add src/renderer/templates/tech_modern/
git commit -m "feat: add tech_modern template"
```

---

## Task 12: MCP Server 入口

**Files:**
- Create: `src/main.py`
- Modify: `src/renderer/engine.py` (add write_to_file method)
- Create: `tests/integration/test_mcp.py`

**Step 1: Update RenderEngine with write method**

Add to `src/renderer/engine.py`:

```python
from ..utils.file import write_html_file

# Add this method to RenderEngine class
def render_to_file(
    self,
    segments: List[Dict[str, Any]],
    template: str,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Render segments to HTML file.

    Args:
        segments: List of segment dictionaries
        template: Template name to use
        output_path: Optional output path (uses default if not provided)

    Returns:
        Path to the written file
    """
    # Generate output path if not provided
    if output_path is None:
        output_path = self.settings.get_output_path(template)

    # Render HTML
    html = self.render(segments, template)

    # Write to file
    return write_html_file(output_path, html)
```

**Step 2: Create MCP server main file**

Create `src/main.py`:

```python
"""MCP Server for article-to-media-image."""

from pathlib import Path
from typing import Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .renderer.engine import RenderEngine
from .config import Settings
from .utils.validator import validate_segments, ValidationError

# Create MCP server
app = Server("article-to-media-image")

# Initialize render engine
settings = Settings()
engine = RenderEngine(settings)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="article_to_card",
            description="Convert article segments into shareable HTML card images. "
            "Input should be pre-processed segments with type and text fields. "
            "Output is an HTML file that can be opened in a browser for screenshot.",
            inputSchema={
                "type": "object",
                "properties": {
                    "segments": {
                        "type": "array",
                        "description": "List of content segments processed by Agent",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": ["title", "content", "quote", "code", "highlight"],
                                    "description": "Segment type",
                                },
                                "text": {
                                    "type": "string",
                                    "description": "Segment text content (max 1000 chars)",
                                },
                            },
                            "required": ["type", "text"],
                        },
                    },
                    "template": {
                        "type": "string",
                        "enum": ["minimal", "gradient", "card", "dark", "tech_modern"],
                        "description": "Template style to use",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Optional output file path (default: ~/article-cards/{timestamp}-{template}.html)",
                    },
                },
                "required": ["segments", "template"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "article_to_card":
        try:
            # Extract arguments
            segments = arguments.get("segments", [])
            template = arguments.get("template", settings.default_template)
            output_path_str = arguments.get("output_path")

            # Validate and convert output path
            output_path: Optional[Path] = None
            if output_path_str:
                output_path = Path(output_path_str).expanduser()

            # Validate segments
            try:
                segments = validate_segments(segments)
            except ValidationError as e:
                return [TextContent(
                    type="text",
                    text=f"Validation Error: {str(e)}\n"
                    f"Please ensure segments have 'type' and 'text' fields, "
                    f"and type is one of: title, content, quote, code, highlight."
                )]

            # Render to file
            result_path = engine.render_to_file(
                segments=segments,
                template=template,
                output_path=output_path,
            )

            # Format response
            response = (
                f"✅ Successfully generated {len(segments)} card(s)\n"
                f"📁 Output: {result_path}\n"
                f"🎨 Template: {template}\n\n"
                f"Open the HTML file in your browser and take screenshots."
            )

            return [TextContent(type="text", text=response)]

        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error: {str(e)}\n"
                f"Please check your input and try again."
            )]

    return [TextContent(type="text", text="Unknown tool")]


def main():
    """Main entry point."""
    import asyncio
    asyncio.run(stdio_server(app))


if __name__ == "__main__":
    main()
```

**Step 3: Write integration test**

Create `tests/integration/test_mcp.py`:

```python
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
```

**Step 4: Run integration test**

```bash
pytest tests/integration/test_mcp.py -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/main.py src/renderer/engine.py tests/integration/
git commit -m "feat: add MCP server entry point and integration test"
```

---

## Task 13: 最终测试和文档

**Files:**
- Update: `README.md`
- Create: `tests/test_all_templates.py`

**Step 1: Create comprehensive template test**

Create `tests/test_all_templates.py`:

```python
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
```

**Step 2: Run all tests**

```bash
pytest tests/ -v
```

Expected: All PASS

**Step 3: Update README with usage example**

Update `README.md`:

```markdown
# Article to Media Image

MCP Skill to convert articles into shareable card images.

## Features

- **5 Beautiful Templates**: Minimal, Gradient, Card, Dark, Tech Modern
- **Smart Segmentation**: Agent processes content, Skill renders
- **One-Click Output**: HTML file ready for browser screenshots
- **Flexible Config**: Customizable output paths and defaults

## Installation

```bash
# Clone repository
git clone <repo-url>
cd article-to-media-image

# Install dependencies
pip install -e .

# Or install with pip
pip install article-to-media-image
```

## MCP Configuration

Add to your MCP client config (e.g., Claude Code settings):

```json
{
  "mcpServers": {
    "article-to-media-image": {
      "command": "python",
      "args": ["-m", "src.main"]
    }
  }
}
```

## Usage

### From Claude Code / Agent

```
User: Convert this article to cards

Agent: I'll process the article and generate cards...

[Agent calls article_to_card tool with processed segments]

✅ Successfully generated 5 card(s)
📁 Output: ~/article-cards/20260321-143022-tech_modern.html
🎨 Template: tech_modern

Open the HTML file in your browser and take screenshots.
```

### Direct Python Usage

```python
from src.renderer.engine import RenderEngine

engine = RenderEngine()

segments = [
    {"type": "title", "text": "My Article Title"},
    {"type": "content", "text": "First paragraph..."},
    {"type": "highlight", "text": "Key insight"},
]

# Render to file
output_path = engine.render_to_file(segments, template="tech_modern")
print(f"Generated: {output_path}")
```

## Templates

| Template | Style | Best For |
|----------|-------|----------|
| `minimal` | Clean, minimalist | Technical docs, serious content |
| `gradient` | Warm gradients | Lifestyle, emotional stories |
| `card` | Information cards | Knowledge sharing, tutorials |
| `dark` | Dark mode | Developers, night reading |
| `tech_modern` | Modern tech | Tech, AI, developer content |

## Segment Types

Agents should use these segment types:

- `title`: Article/section title
- `content`: Regular paragraph content
- `quote`: Quotations or references
- `highlight`: Key points or emphasis
- `code`: Code snippets or commands

## Configuration

Default config: `~/.article-to-media-image/config.yaml`

```yaml
defaults:
  template: tech_modern
  output_path: ~/article-cards/{timestamp}-{template}.html

output:
  base_dir: ~/article-cards
  filename_template: "{timestamp}-{template}.html"
```

## License

MIT License - see LICENSE file for details.
```

**Step 4: Manual smoke test**

```bash
python -c "
from src.renderer.engine import RenderEngine
from src.config import Settings
from pathlib import Path

# Test all templates
segments = [
    {'type': 'title', 'text': '🚀 Article to Media Image'},
    {'type': 'content', 'text': 'This is a test of the article to card conversion system.'},
    {'type': 'highlight', 'text': '5 beautiful templates included!'},
]

engine = RenderEngine()
for template in ['minimal', 'gradient', 'card', 'dark', 'tech_modern']:
    output = engine.render_to_file(segments, template)
    print(f'✅ {template}: {output}')
"
```

**Step 5: Commit final changes**

```bash
git add README.md tests/test_all_templates.py
git commit -m "docs: update README with comprehensive usage guide"
```

---

## Summary

This implementation plan builds the article-to-media-image MCP Skill in 13 tasks:

1. ✅ Project initialization and configuration
2. ✅ Configuration management module
3. ✅ Input validation module
4. ✅ File utilities module
5. ✅ Template context builder
6. ✅ Render engine core
7. ✅ Minimal template
8. ✅ Gradient template
9. ✅ Card template
10. ✅ Dark template
11. ✅ Tech Modern template
12. ✅ MCP server entry point
13. ✅ Final testing and documentation

**Total estimated time:** ~2-3 hours

**Tech stack:** Python 3.10+, MCP SDK, Jinja2, PyYAML
