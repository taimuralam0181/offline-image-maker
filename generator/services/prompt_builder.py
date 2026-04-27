"""Prompt helpers used before sending text to the local image model."""


QUALITY_PHRASE = "high detail, sharp focus, professional composition"
NEGATIVE_PROMPT = (
    "low quality, blurry, distorted, bad anatomy, extra fingers, watermark, text, logo"
)


def build_type_prompt(user_prompt, style):
    """Create a clean final prompt from a short user prompt."""
    return f"{user_prompt.strip()}, {style}, {QUALITY_PHRASE}"


def build_script_prompt(parts):
    """Create a final optimized prompt from parsed script parts."""
    segments = [
        parts["subject"],
        parts["action"],
        f"background: {parts['background']}",
        f"{parts['mood']} mood",
        parts["lighting"],
        parts["style"],
        QUALITY_PHRASE,
    ]
    cleaned_segments = []
    for segment in segments:
        segment = str(segment).strip(" ,")
        if segment and segment not in cleaned_segments:
            cleaned_segments.append(segment)
    return ", ".join(cleaned_segments)
