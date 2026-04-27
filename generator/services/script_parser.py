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
    r"\bin (?:the|an|a) ([^,.]+)",
    r"\bat (?:the|an|a) ([^,.]+)",
    r"\bon (?:the|an|a) ([^,.]+)",
    r"\binside (?:the|an|a) ([^,.]+)",
    r"\bnear (?:the|an|a) ([^,.]+)",
    r"\bthrough (?:the|an|a) ([^,.]+)",
]

ACTION_WORDS = [
    "walking",
    "walks",
    "walk",
    "running",
    "runs",
    "run",
    "standing",
    "stands",
    "stand",
    "flying",
    "flies",
    "fly",
    "holding",
    "holds",
    "hold",
    "looking",
    "looks",
    "look",
    "fighting",
    "fights",
    "fight",
    "dancing",
    "dances",
    "dance",
    "sitting",
    "sits",
    "sit",
    "exploring",
    "explores",
    "explore",
    "driving",
    "drives",
    "drive",
    "riding",
    "rides",
    "ride",
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
    location_candidates = []
    for pattern in LOCATION_PATTERNS:
        for match in re.finditer(pattern, lowered_text):
            location = match.group(1).strip()
            location = re.split(
                r"\b(with|while|during|under|near|as|and)\b",
                location,
                maxsplit=1,
            )[0].strip(" ,.")
            if location:
                location_candidates.append((match.start(), location))
    if location_candidates:
        location_candidates.sort(key=lambda item: item[0])
        return location_candidates[0][1]
    return "detailed environment"


def _find_action(text):
    """Extract the first obvious visual action."""
    lowered_text = text.lower()
    for word in ACTION_WORDS:
        if word in lowered_text:
            return word
    return "posing in a visually clear scene"


def _build_subject(text, background, lighting):
    """Create a shorter subject line without repeating background or lighting.

    This keeps the final prompt cleaner and easier for a student to explain.
    """
    subject = _first_sentence(text)
    subject = re.sub(r"^\s*at\s+\w+\s*,?\s*", "", subject, flags=re.IGNORECASE)
    subject = re.sub(r"\bwith [^,.]+", "", subject, flags=re.IGNORECASE).strip(" ,.")
    if lighting != "soft light":
        subject = re.sub(rf"\bat {re.escape(lighting)}\b", "", subject, flags=re.IGNORECASE)
    subject = re.sub(r"\s+,", ",", subject)
    subject = re.sub(r"\s+", " ", subject).strip(" ,.")
    return subject[:180] if subject else _first_sentence(text)[:180]


def parse_script(script_text, selected_style):
    """Return structured visual parts from a longer script.

    The result is a dictionary so the template can display each extracted part.
    """
    cleaned_script = " ".join(script_text.split())
    background = _find_location(cleaned_script)
    lighting = _find_keyword(cleaned_script, LIGHTING_KEYWORDS, "soft light")
    subject = _build_subject(cleaned_script, background, lighting)

    return {
        "subject": subject,
        "action": _find_action(cleaned_script),
        "background": background,
        "mood": _find_keyword(cleaned_script, MOOD_KEYWORDS, "cinematic"),
        "lighting": lighting,
        "style": selected_style,
    }
