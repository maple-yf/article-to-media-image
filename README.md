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

## Development

```bash
# Install development dependencies
pip install -e ".[test]"

# Run tests
pytest tests/ -v

# Run specific test file
pytest tests/test_all_templates.py -v
```

## License

MIT License - see LICENSE file for details.

---

> **Note:** The MCP server (`src/main.py`) is now fully implemented. Use the `article_to_card` tool to generate card images from article segments.
