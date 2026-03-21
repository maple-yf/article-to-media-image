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
                f"Successfully generated {len(segments)} card(s)\n"
                f"Output: {result_path}\n"
                f"Template: {template}\n\n"
                f"Open the HTML file in your browser and take screenshots."
            )

            return [TextContent(type="text", text=response)]

        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error: {str(e)}\n"
                f"Please check your input and try again."
            )]

    return [TextContent(type="text", text="Unknown tool")]


def main():
    """Main entry point."""
    import asyncio
    asyncio.run(stdio_server(app))


if __name__ == "__main__":
    main()
