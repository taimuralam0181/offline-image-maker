"""One-time Stable Diffusion model download for Offline Image Maker.

Run this script once with internet access:
    python scripts/download_model.py

After the model is saved locally, the Django app can run fully offline because
image generation loads files only from local_models/stable-diffusion.
"""
from pathlib import Path
import sys


# Stable Diffusion v1.5 gives noticeably better and more realistic results than
# tiny demo models. It is larger, so the one-time download takes longer.
MODEL_ID = "runwayml/stable-diffusion-v1-5"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = PROJECT_ROOT / "local_models" / "stable-diffusion"
REQUIRED_ENTRIES = [
    "model_index.json",
    "unet",
    "vae",
    "tokenizer",
    "text_encoder",
    "scheduler",
]


def verify_model_folder(model_dir):
    """Return a list of required Diffusers files or folders that are missing."""
    return [entry for entry in REQUIRED_ENTRIES if not (model_dir / entry).exists()]


def main():
    """Download and save the Diffusers model in the local project folder."""
    print("Offline Image Maker - One-time model download")
    print("---------------------------------------------")
    print("This step needs internet only once.")
    print("No API is used for image generation at runtime.")
    print(f"Model source: {MODEL_ID}")
    print(f"Target folder: {TARGET_DIR}")
    print("")

    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        print("ERROR: Required packages are missing.")
        print("Run: pip install -r requirements.txt")
        raise SystemExit(1) from exc

    TARGET_DIR.parent.mkdir(parents=True, exist_ok=True)

    try:
        print("Downloading model files. This can take a long time...")
        snapshot_download(
            repo_id=MODEL_ID,
            local_dir=TARGET_DIR,
            local_dir_use_symlinks=False,
            resume_download=True,
        )
        print("Model files downloaded locally.")
    except Exception as exc:
        print("")
        print("ERROR: Model download failed.")
        print("Possible reasons:")
        print("- No internet connection during this one-time setup step")
        print("- The model requires Hugging Face access/login on this machine")
        print("- Not enough disk space")
        print(f"Details: {exc}")
        raise SystemExit(1) from exc

    missing_entries = verify_model_folder(TARGET_DIR)
    if missing_entries:
        print("")
        print("ERROR: Download finished, but the model folder is incomplete.")
        print(f"Missing entries: {', '.join(missing_entries)}")
        raise SystemExit(1)

    print("")
    print("Model folder verified.")
    print("You can now run the Django project fully offline:")
    print("  python manage.py check_local_model")
    print("  python manage.py runserver")
    return 0


if __name__ == "__main__":
    sys.exit(main())
