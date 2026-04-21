"""Database models for storing local image generation history."""
from django.db import models


class ImageGeneration(models.Model):
    """One saved record for a generated image or a failed generation attempt."""

    MODE_TYPE = "type"
    MODE_SCRIPT = "script"
    MODE_CHOICES = [
        (MODE_TYPE, "Type to Image"),
        (MODE_SCRIPT, "Script to Image"),
    ]

    original_input = models.TextField(help_text="The exact text entered by the user.")
    final_prompt = models.TextField(help_text="The optimized prompt sent to the local model.")
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    style = models.CharField(max_length=80, blank=True)
    width = models.PositiveIntegerField(default=512)
    height = models.PositiveIntegerField(default=512)
    inference_steps = models.PositiveIntegerField(default=25)
    guidance_scale = models.FloatField(default=7.5)
    image = models.ImageField(upload_to="generated/", blank=True, null=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_mode_display()} #{self.pk}"

    @property
    def was_successful(self):
        """Used by templates and admin to show whether an image was created."""
        return bool(self.image and not self.error_message)
