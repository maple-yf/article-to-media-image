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
