"""Small service layer around the ImageGeneration model."""
from generator.models import ImageGeneration


def create_history_record(
    *,
    original_input,
    final_prompt,
    mode,
    style,
    width,
    height,
    inference_steps,
    guidance_scale,
    image_path="",
    error_message="",
):
    """Save both successful and failed attempts for transparent history."""
    print("[DEBUG] create_history_record() called.")
    print(f"[DEBUG] History mode: {mode}")
    print(f"[DEBUG] Final prompt: {final_prompt}")
    print(f"[DEBUG] Image path stored in ImageField: {image_path}")
    print(f"[DEBUG] Error message: {error_message}")
    record = ImageGeneration.objects.create(
        original_input=original_input,
        final_prompt=final_prompt,
        mode=mode,
        style=style,
        width=width,
        height=height,
        inference_steps=inference_steps,
        guidance_scale=guidance_scale,
        image=image_path or None,
        error_message=error_message,
    )
    image_url = record.image.url if record.image else ""
    print(f"[DEBUG] Created history record id={record.pk}, image_url={image_url}")
    return record


def get_recent_type_history(limit=5):
    """Return recent successful Type to Image prompts for the prompt history box."""
    return ImageGeneration.objects.filter(
        mode=ImageGeneration.MODE_TYPE,
        error_message="",
    )[:limit]


def get_all_history():
    """Return all history records newest first."""
    return ImageGeneration.objects.all()
