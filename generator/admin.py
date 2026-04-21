"""Admin configuration for generation history."""
from django.contrib import admin

from .models import ImageGeneration


@admin.register(ImageGeneration)
class ImageGenerationAdmin(admin.ModelAdmin):
    list_display = ("id", "mode", "style", "width", "height", "created_at", "was_successful")
    list_filter = ("mode", "style", "created_at")
    search_fields = ("original_input", "final_prompt")
    readonly_fields = ("created_at",)
