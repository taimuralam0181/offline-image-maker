"""Simple offline parser for converting script text into visual prompt parts.

This intentionally avoids online LLMs. It uses small keyword rules and sentence
selection so the project remains understandable for beginners and runs offline.
"""
import re


MOOD_KEYWORDS = [
    "calm",
    "dramatic",
    "mysterious",
    "peaceful",
    "tense",
    "joyful",
    "sad",
    "epic",
    "romantic",
    "dark",
]

LIGHTING_KEYWORDS = [
    "sunrise",
    "sunset",
    "morning",
    "noon",
    "night",
    "moonlight",
    "golden light",
    "neon",
    "soft light",
    "studio light",
    "rainy",
]

LOCATION_PATTERNS = [
    r"\bin the ([^,.]+)",
    r"\bat the ([^,.]+)",
    r"\bon the ([^,.]+)",
    r"\binside the ([^,.]+)",
    r"\bnear the ([^,.]+)",
]

ACTION_WORDS = [
    "walking",
    "running",
    "standing",
    "flying",
    "holding",
    "looking",
    "fighting",
    "dancing",
    "sitting",
    "exploring",
    "driving",
    "riding",
]


def _first_sentence(text):
    """Return a short sentence that can become the visual subject."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return sentences[0].strip(" .!?") if sentences else text.strip()


def _find_keyword(text, keywords, default_value):
    """Find the first keyword that appears in the script."""
    lowered_text = text.lower()
    for keyword in keywords:
        if keyword in lowered_text:
            return keyword
    return default_value


def _find_location(text):
    """Extract a likely background or location phrase."""
    lowered_text = text.lower()
    for pattern in LOCATION_PATTERNS:
        match = re.search(pattern, lowered_text)
        if match:
            return match.group(1).strip()
    return "detailed environment"


def _find_action(text):
    """Extract the first obvious visual action."""
    lowered_text = text.lower()
    for word in ACTION_WORDS:
        if word in lowered_text:
            return word
    return "posing in a visually clear scene"


def parse_script(script_text, selected_style):
    """Return structured visual parts from a longer script.

    The result is a dictionary so the template can display each extracted part.
    """
    cleaned_script = " ".join(script_text.split())
    first_sentence = _first_sentence(cleaned_script)

    return {
        "subject": first_sentence[:180],
        "action": _find_action(cleaned_script),
        "background": _find_location(cleaned_script),
        "mood": _find_keyword(cleaned_script, MOOD_KEYWORDS, "cinematic"),
        "lighting": _find_keyword(cleaned_script, LIGHTING_KEYWORDS, "soft light"),
        "style": selected_style,
    }
