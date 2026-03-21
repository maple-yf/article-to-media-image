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
