"""Function-based views for Offline Image Maker."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from .forms import ScriptToImageForm, TypeToImageForm
from .models import ImageGeneration
from .services.history_service import (
    create_history_record,
    get_all_history,
    get_recent_type_history,
)
from .services.image_generator import ImageGenerationError, generate_image
from .services.prompt_builder import build_script_prompt, build_type_prompt
from .services.script_parser import parse_script


def home_view(request):
    """Show the two main workflows."""
    return render(request, "generator/home.html")


def type_to_image_view(request):
    """Generate an image directly from a short prompt."""
    form = TypeToImageForm(request.POST or None)
    generated_record = None
    image_url = ""

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        final_prompt = build_type_prompt(data["prompt"], data["style"])
        image_path = ""
        error_message = ""
        print("[DEBUG] Type to Image form is valid.")
        print(f"[DEBUG] Original prompt: {data['prompt']}")
        print(f"[DEBUG] Final prompt sent to generator: {final_prompt}")

        try:
            image_path = generate_image(
                prompt=final_prompt,
                width=data["width"],
                height=data["height"],
                steps=data["inference_steps"],
                guidance_scale=data["guidance_scale"],
            )
            print(f"[DEBUG] generate_image() returned image_path: {image_path}")
            messages.success(request, "Image generated locally and saved to history.")
        except ImageGenerationError as exc:
            error_message = str(exc)
            print(f"[DEBUG] Image generation failed: {error_message}")
            messages.error(request, error_message)

        generated_record = create_history_record(
            original_input=data["prompt"],
            final_prompt=final_prompt,
            mode=ImageGeneration.MODE_TYPE,
            style=data["style"],
            width=data["width"],
            height=data["height"],
            inference_steps=data["inference_steps"],
            guidance_scale=data["guidance_scale"],
            image_path=image_path,
            error_message=error_message,
        )
        if generated_record.was_successful:
            image_url = generated_record.image.url

    context = {
        "form": form,
        "generated_record": generated_record,
        "image_url": image_url,
        "recent_history": get_recent_type_history(),
    }
    return render(request, "generator/type_to_image.html", context)


def script_to_image_view(request):
    """Parse a script offline and generate an image in one step."""
    form = ScriptToImageForm(request.POST or None)
    extracted_parts = None
    final_prompt = ""
    generated_record = None
    image_url = ""

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        extracted_parts = parse_script(data["script"], data["style"])
        final_prompt = build_script_prompt(extracted_parts)
        print("[DEBUG] Script to Image form is valid.")
        print(f"[DEBUG] Extracted script parts: {extracted_parts}")
        print(f"[DEBUG] Final script prompt: {final_prompt}")

        image_path = ""
        error_message = ""
        try:
            image_path = generate_image(
                prompt=final_prompt,
                width=data["width"],
                height=data["height"],
                steps=data["inference_steps"],
                guidance_scale=data["guidance_scale"],
            )
            print(f"[DEBUG] generate_image() returned image_path: {image_path}")
            messages.success(request, "Script image generated locally and saved.")
        except ImageGenerationError as exc:
            error_message = str(exc)
            print(f"[DEBUG] Image generation failed: {error_message}")
            messages.error(request, error_message)

        generated_record = create_history_record(
            original_input=data["script"],
            final_prompt=final_prompt,
            mode=ImageGeneration.MODE_SCRIPT,
            style=data["style"],
            width=data["width"],
            height=data["height"],
            inference_steps=data["inference_steps"],
            guidance_scale=data["guidance_scale"],
            image_path=image_path,
            error_message=error_message,
        )
        if generated_record.was_successful:
            image_url = generated_record.image.url

    context = {
        "form": form,
        "extracted_parts": extracted_parts,
        "final_prompt": final_prompt,
        "generated_record": generated_record,
        "image_url": image_url,
    }
    return render(request, "generator/script_to_image.html", context)


def history_view(request):
    """Show all previously generated local images and failed attempts."""
    return render(request, "generator/history.html", {"records": get_all_history()})


def history_detail_view(request, pk):
    """Show one history item with full input and prompt text."""
    record = get_object_or_404(ImageGeneration, pk=pk)
    return render(request, "generator/history_detail.html", {"record": record})
