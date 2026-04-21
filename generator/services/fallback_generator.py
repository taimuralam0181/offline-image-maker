"""Small offline image renderer used when no Stable Diffusion model is present.

This is not a real text-to-image AI model. It creates a simple visual scene with
Pillow so the app can be demonstrated fully offline until local SD files are
added. Real AI generation still happens through image_generator.py.
"""
from hashlib import sha256
from pathlib import Path
from textwrap import wrap
from uuid import uuid4

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont


def _colors_from_prompt(prompt):
    """Create repeatable colors from prompt text."""
    digest = sha256(prompt.encode("utf-8")).hexdigest()
    first = tuple(int(digest[i : i + 2], 16) for i in (0, 2, 4))
    second = tuple(int(digest[i : i + 2], 16) for i in (6, 8, 10))
    accent = tuple(int(digest[i : i + 2], 16) for i in (12, 14, 16))
    return first, second, accent


def _load_font(size, bold=False):
    """Use common Windows fonts when available, otherwise Pillow default."""
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(font_name, size)
    except OSError:
        return ImageFont.load_default()


def _draw_gradient(draw, width, height, first, second):
    """Draw a vertical gradient background."""
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(
            int(first[index] * (1 - ratio) + second[index] * ratio)
            for index in range(3)
        )
        draw.line([(0, y), (width, y)], fill=color)


def _draw_city_scene(draw, width, height, accent):
    """Draw a basic city skyline for urban/cyberpunk prompts."""
    ground_y = int(height * 0.72)
    draw.rectangle([0, ground_y, width, height], fill=(18, 24, 35))
    building_width = max(34, width // 10)
    for index, x in enumerate(range(0, width + building_width, building_width)):
        top = ground_y - ((index * 47) % max(90, height // 3)) - 40
        draw.rectangle([x, top, x + building_width - 8, ground_y], fill=(28, 36, 52))
        for wx in range(x + 8, x + building_width - 14, 18):
            for wy in range(top + 18, ground_y - 18, 28):
                color = accent if (wx + wy) % 3 == 0 else (244, 193, 101)
                draw.rectangle([wx, wy, wx + 7, wy + 10], fill=color)
    draw.line([0, ground_y, width, ground_y], fill=accent, width=4)


def _draw_forest_scene(draw, width, height, accent):
    """Draw a basic forest for nature prompts."""
    ground_y = int(height * 0.74)
    draw.rectangle([0, ground_y, width, height], fill=(34, 78, 55))
    for index, x in enumerate(range(-30, width + 40, max(38, width // 12))):
        trunk_top = int(height * 0.36) + (index * 17) % 70
        draw.rectangle([x + 18, trunk_top, x + 30, ground_y], fill=(89, 59, 38))
        draw.polygon(
            [(x, trunk_top + 20), (x + 24, trunk_top - 70), (x + 58, trunk_top + 20)],
            fill=(28, 102, 69),
        )
        draw.polygon(
            [(x + 4, trunk_top - 20), (x + 24, trunk_top - 95), (x + 54, trunk_top - 20)],
            fill=(45, 134, 88),
        )
    draw.ellipse([width * 0.68, height * 0.12, width * 0.86, height * 0.30], fill=accent)


def _draw_object_scene(draw, width, height, accent):
    """Draw a generic focused object for prompts that do not match a scene."""
    center_x = width // 2
    center_y = height // 2
    radius = min(width, height) // 4
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=(255, 255, 255),
        outline=accent,
        width=6,
    )
    draw.rounded_rectangle(
        [center_x - radius // 2, center_y - 20, center_x + radius // 2, center_y + 20],
        radius=10,
        fill=accent,
    )
    draw.line([center_x, center_y - radius, center_x, center_y + radius], fill=(255, 255, 255), width=3)


def _draw_prompt_caption(draw, prompt, width, height):
    """Add a small caption without covering the generated preview."""
    caption_font = _load_font(max(13, width // 42))
    caption = "Local preview mode - add Stable Diffusion model for real AI output"
    prompt_line = wrap(prompt, width=max(32, width // 16))[0]
    panel_height = max(62, height // 8)
    y = height - panel_height
    draw.rectangle([0, y, width, height], fill=(8, 13, 22))
    draw.text((20, y + 12), prompt_line, fill=(245, 248, 252), font=caption_font)
    draw.text((20, y + 36), caption, fill=(164, 174, 191), font=caption_font)


def generate_fallback_image(final_prompt, width, height):
    """Create and save a local illustrative image based on the prompt text."""
    print("[DEBUG] generate_fallback_image() called.")
    output_dir = Path(settings.OFFLINE_GENERATED_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[DEBUG] Fallback output directory: {output_dir}")

    first, second, accent = _colors_from_prompt(final_prompt)
    image = Image.new("RGB", (width, height), first)
    draw = ImageDraw.Draw(image)
    _draw_gradient(draw, width, height, first, second)

    prompt_lower = final_prompt.lower()
    if any(word in prompt_lower for word in ["city", "cyberpunk", "street", "building", "neon"]):
        _draw_city_scene(draw, width, height, accent)
    elif any(word in prompt_lower for word in ["forest", "tree", "jungle", "garden", "nature"]):
        _draw_forest_scene(draw, width, height, accent)
    else:
        _draw_object_scene(draw, width, height, accent)

    _draw_prompt_caption(draw, final_prompt, width, height)

    filename = f"{uuid4().hex}.png"
    output_path = output_dir / filename
    image.save(output_path)
    print(f"[DEBUG] Fallback image saved to: {output_path}")
    return f"generated/{filename}"
