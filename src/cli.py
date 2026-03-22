"""CLI entry point for article-to-media-image."""

import argparse
import json
import sys
from pathlib import Path
from .renderer.engine import RenderEngine
from .config import Settings


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="将文章转换为精美的 HTML 卡片"
    )
    parser.add_argument(
        "--template", "-t",
        choices=["minimal", "gradient", "card", "dark", "tech_modern"],
        default="tech_modern",
        help="模板风格 (默认: tech_modern)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="输出文件路径 (默认: ~/article-cards/{timestamp}-{template}.html)"
    )
    parser.add_argument(
        "--segments", "-s",
        help="JSON 格式的 segments 数据"
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="列出所有可用模板"
    )

    args = parser.parse_args()

    # List templates mode
    if args.list_templates:
        print("可用模板:")
        for template in ["minimal", "gradient", "card", "dark", "tech_modern"]:
            print(f"  - {template}")
        return 0

    # Parse segments
    if args.segments:
        try:
            segments = json.loads(args.segments)
        except json.JSONDecodeError as e:
            print(f"错误: JSON 解析失败 - {e}", file=sys.stderr)
            return 1
    else:
        # Read from stdin
        try:
            data = json.load(sys.stdin)
            segments = data.get("segments", [])
        except json.JSONDecodeError:
            print("错误: 请提供 --segments 参数或通过 stdin 传入 JSON", file=sys.stderr)
            return 1
        except Exception:
            print("错误: 无法读取 stdin", file=sys.stderr)
            return 1

    # Validate segments
    if not segments:
        print("错误: segments 不能为空", file=sys.stderr)
        return 1

    # Render
    try:
        engine = RenderEngine()
        output_path = engine.render_to_file(
            segments=segments,
            template=args.template,
            output_path=args.output
        )
        print(f"✅ Generated: {output_path}")
        print(f"🎨 Template: {args.template}")
        print(f"📦 Segments: {len(segments)}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
