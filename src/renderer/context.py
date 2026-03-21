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
