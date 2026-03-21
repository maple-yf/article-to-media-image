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

> **Note:** The MCP server (`src/main.py`) will be implemented in Task 12. Until then, the package structure and templates can be used directly via Python API.
