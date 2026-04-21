"""Validate the local Stable Diffusion model folder before generation.

Run:
    python manage.py check_local_model

This command is fully offline. It only checks files and folders on disk, so a
student can confirm the model setup before starting the heavier generation flow.
"""
from django.conf import settings
from django.core.management.base import BaseCommand

from generator.services.image_generator import get_model_validation_status


class Command(BaseCommand):
    """Django management command for local model setup checks."""

    help = "Validate the local Diffusers Stable Diffusion model folder."

    def handle(self, *args, **options):
        """Print a beginner-friendly report about the configured model folder."""
        status = get_model_validation_status()

        self.stdout.write("")
        self.stdout.write("Offline Image Maker - Local Model Check")
        self.stdout.write("---------------------------------------")
        self.stdout.write(f"Configured path: {status['path']}")
        self.stdout.write(f"Backend: {settings.OFFLINE_IMAGE_BACKEND}")
        self.stdout.write("Required entries:")

        for entry in settings.OFFLINE_REQUIRED_MODEL_FILES:
            marker = "OK" if entry not in status["missing_entries"] else "MISSING"
            self.stdout.write(f"  [{marker}] {entry}")

        self.stdout.write("")
        if status["is_valid"]:
            self.stdout.write(self.style.SUCCESS("Model folder is valid."))
            self.stdout.write(
                "You can run: python manage.py runserver"
            )
        else:
            self.stdout.write(self.style.ERROR("Model folder is not valid."))
            self.stdout.write(status["message"])
            self.stdout.write("")
            self.stdout.write("Expected folder example:")
            self.stdout.write(r"  C:\Users\HOTSPOT\OneDrive\Desktop\projectAI\local_models\stable-diffusion")
            self.stdout.write("    model_index.json")
            self.stdout.write("    unet\\")
            self.stdout.write("    vae\\")
            self.stdout.write("    tokenizer\\")
            self.stdout.write("    text_encoder\\")
            self.stdout.write("    scheduler\\")
