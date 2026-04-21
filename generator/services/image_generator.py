"""Offline image generation service.

This module is the bridge between Django and the local Stable Diffusion model.
It never calls an external API. The model must already exist on the user's
machine in Diffusers format, and `local_files_only=True` prevents runtime
downloads.
"""
from pathlib import Path
from uuid import uuid4

from django.conf import settings

from .fallback_generator import generate_fallback_image
from .prompt_builder import NEGATIVE_PROMPT


class ImageGenerationError(Exception):
    """User-facing error raised when local image generation cannot continue."""


_PIPELINE = None
_DEVICE = None


def get_model_validation_status(model_path=None):
    """Validate the Stable Diffusion folder configured in Django settings.

    A Diffusers Stable Diffusion model is split into several local components:
    `model_index.json` describes the pipeline, `unet` predicts image noise,
    `vae` converts latent data into pixels, `tokenizer` prepares prompt text,
    and `text_encoder` turns tokens into embeddings. If any required component
    is missing, the model cannot be loaded correctly.

    The helper only checks local files. It does not import the heavy model and
    does not contact the internet, so it is safe to use from views, startup
    checks, and management commands.
    """
    model_path = Path(model_path or settings.OFFLINE_IMAGE_MODEL_PATH)
    required_entries = getattr(settings, "OFFLINE_REQUIRED_MODEL_FILES", [])
    missing_entries = []

    print(f"[DEBUG] Validating local model path from settings: {model_path}")
    print(f"[DEBUG] Required Diffusers entries: {required_entries}")

    if not model_path.exists():
        return {
            "is_valid": False,
            "path": model_path,
            "missing_entries": required_entries,
            "message": (
                "Local Stable Diffusion model folder was not found. "
                f"Configured path: {model_path}. "
                "Create this folder or set OFFLINE_IMAGE_MODEL_PATH to your local "
                "Diffusers model directory."
            ),
        }

    if not model_path.is_dir():
        return {
            "is_valid": False,
            "path": model_path,
            "missing_entries": [],
            "message": (
                "The configured model path exists, but it is not a folder. "
                f"Configured path: {model_path}."
            ),
        }

    # Each entry can be a file or folder depending on the Diffusers component.
    for entry in required_entries:
        entry_path = model_path / entry
        if not entry_path.exists():
            missing_entries.append(entry)

    if missing_entries:
        return {
            "is_valid": False,
            "path": model_path,
            "missing_entries": missing_entries,
            "message": (
                "The local model folder is incomplete. "
                f"Configured path: {model_path}. "
                f"Missing required Diffusers entries: {', '.join(missing_entries)}."
            ),
        }

    return {
        "is_valid": True,
        "path": model_path,
        "missing_entries": [],
        "message": "Local Stable Diffusion model folder is valid.",
    }


def _choose_device(torch_module):
    """Choose CPU or CUDA for local inference."""
    configured_device = settings.OFFLINE_MODEL_DEVICE.lower()
    if configured_device != "auto":
        return configured_device
    return "cuda" if torch_module.cuda.is_available() else "cpu"


def _validate_model_path(model_path):
    """Return a valid model path or raise a clear setup error."""
    validation = get_model_validation_status(model_path)
    print(f"[DEBUG] Model validation result: {validation}")
    if not validation["is_valid"]:
        raise ImageGenerationError(validation["message"])
    print("Model validation passed")
    return validation["path"]


def _load_pipeline():
    """Load the local Stable Diffusion pipeline once and cache it in memory.

    Loading a Stable Diffusion model is slow and memory-heavy. The first request
    loads it from disk; later requests reuse the cached `_PIPELINE` object.
    """
    global _PIPELINE, _DEVICE

    if _PIPELINE is not None:
        print("[DEBUG] Reusing already loaded Stable Diffusion pipeline.")
        return _PIPELINE

    model_path = _validate_model_path(settings.OFFLINE_IMAGE_MODEL_PATH)
    print("Loading model...")
    print(f"[DEBUG] Loading Stable Diffusion pipeline from: {model_path}")

    try:
        import torch
        from diffusers import StableDiffusionPipeline
    except ImportError as exc:
        raise ImageGenerationError(
            "Missing local ML packages. Install requirements.txt in your virtual environment."
        ) from exc

    _DEVICE = _choose_device(torch)
    # CUDA GPUs are fastest with float16. CPU inference is more compatible with float32.
    dtype = torch.float16 if _DEVICE == "cuda" else torch.float32
    print(f"[DEBUG] Selected device: {_DEVICE}, dtype: {dtype}")

    try:
        pipeline = StableDiffusionPipeline.from_pretrained(
            str(model_path),
            torch_dtype=dtype,
            local_files_only=True,
            safety_checker=None,
        )
        pipeline = pipeline.to(_DEVICE)
        if _DEVICE == "cuda":
            pipeline.enable_attention_slicing()
    except Exception as exc:
        print(f"[DEBUG] Stable Diffusion load exception: {exc}")
        raise ImageGenerationError(
            "Could not load the local Stable Diffusion model. Check that the folder "
            "contains a valid Diffusers Stable Diffusion model and all files are "
            "available offline."
        ) from exc

    _PIPELINE = pipeline
    print("Model loaded")
    print("[DEBUG] Stable Diffusion pipeline loaded successfully.")
    return _PIPELINE


def generate_image(prompt, width, height, steps, guidance_scale):
    """Generate an image and return the path stored by Django's ImageField.

    The image is generated by the local Diffusers pipeline and saved under
    `media/generated/`. The returned value is the relative media path stored in
    Django's ImageField, for example `generated/example.png`.
    """
    backend = settings.OFFLINE_IMAGE_BACKEND.lower()
    model_path_exists = Path(settings.OFFLINE_IMAGE_MODEL_PATH).exists()
    print("[DEBUG] generate_image() called.")
    print(f"[DEBUG] Backend: {backend}")
    print(f"[DEBUG] Model path: {settings.OFFLINE_IMAGE_MODEL_PATH}")
    print(f"[DEBUG] Model path exists: {model_path_exists}")
    print(f"[DEBUG] Output directory: {settings.OFFLINE_GENERATED_DIR}")
    print(f"[DEBUG] Prompt: {prompt}")
    print(
        "[DEBUG] Settings: "
        f"width={width}, height={height}, steps={steps}, guidance={guidance_scale}"
    )

    if backend == "local_pillow":
        print("Generating image...")
        image_path = generate_fallback_image(prompt, width, height)
        print("Generation done")
        print(f"Returning URL: {settings.MEDIA_URL}{image_path}")
        return image_path

    if backend != "stable_diffusion":
        raise ImageGenerationError(
            f"Unsupported OFFLINE_IMAGE_BACKEND={backend}. Use local_pillow or stable_diffusion."
        )

    pipeline = _load_pipeline()
    output_dir = Path(settings.OFFLINE_GENERATED_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[DEBUG] Ensured output directory exists: {output_dir}")

    try:
        print("Generating image...")
        print("[DEBUG] Calling Stable Diffusion pipeline...")
        result = pipeline(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
        )
    except Exception as exc:
        print(f"[DEBUG] Stable Diffusion generation exception: {exc}")
        raise ImageGenerationError(
            "The local model failed during image generation. Try a smaller size or fewer steps."
        ) from exc

    if not result.images:
        raise ImageGenerationError("The local model did not return an image.")

    image = result.images[0]
    filename = f"{uuid4().hex}.png"
    output_path = output_dir / filename
    try:
        image.save(output_path)
    except Exception as exc:
        print(f"[DEBUG] Image save exception: {exc}")
        raise ImageGenerationError(
            "The image was generated but could not be saved to media/generated/."
        ) from exc

    relative_image_path = f"generated/{filename}"
    print("Generation done")
    print(f"Saved image at: {output_path}")
    print(f"Returning URL: {settings.MEDIA_URL}{relative_image_path}")
    print(f"[DEBUG] Stable Diffusion image saved to: {output_path}")

    return relative_image_path
