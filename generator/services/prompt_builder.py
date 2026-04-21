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
    return (
        f"{parts['subject']}, {parts['action']}, background: {parts['background']}, "
        f"{parts['mood']} mood, {parts['lighting']}, {parts['style']}, {QUALITY_PHRASE}"
    )
