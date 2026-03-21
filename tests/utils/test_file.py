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
