# Offline Image Maker

A Django web app that generates images from text. It has two modes:

- **Type to Image**: write a short prompt and generate an image.
- **Script to Image**: paste a longer scene/script, convert it into a final prompt, then generate an image.

The project is designed for **fully offline runtime generation**. No OpenAI API,
Stability API, Replicate API, hosted Hugging Face inference API, or cloud service
is used for image generation.

## Quick Start After Cloning

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

If the page opens, the Django app is working.

## Important: Two Ways To Run

### Option A: Demo Mode Without Stable Diffusion Model

Use this if you only want to test the UI quickly and avoid downloading a large
model.

```powershell
$env:OFFLINE_IMAGE_BACKEND="local_pillow"
python manage.py runserver
```

This saves and displays images, but they are **not real AI Stable Diffusion
images**. It is only a local offline preview/demo renderer.

### Option B: Real Offline Stable Diffusion Mode

Use this for real AI image generation.

Step 1: Download the model once. This step needs internet only once:

```powershell
python scripts/download_model.py
```

Step 2: Check that the model folder is valid:

```powershell
python manage.py check_local_model
```

Expected success:

```text
Model folder is valid.
```

Step 3: Run real offline generation:

```powershell
$env:OFFLINE_IMAGE_BACKEND="stable_diffusion"
python manage.py runserver
```

After the model is downloaded, generation runs from local files only.

## Local Model Folder

The model should be stored here:

```text
C:\Users\HOTSPOT\OneDrive\Desktop\projectAI\local_models\stable-diffusion
```

Expected structure:

```text
stable-diffusion/
  model_index.json
  unet/
  vae/
  tokenizer/
  text_encoder/
  scheduler/
```

The included script downloads:

```text
runwayml/stable-diffusion-v1-5
```

This gives better results than tiny demo models, but it is large and can take
time to download.

## Useful Test Prompt

Try this in **Type to Image**:

```text
A realistic photo of a small modern house beside a river, golden hour sunlight, natural colors, DSLR photography, high detail, sharp focus
```

Recommended settings:

```text
Style: Photorealistic
Width: 512
Height: 512
Inference steps: 30
Guidance scale: 7.5
```

## Common Problems

### Problem: Local model folder not found

Run:

```powershell
python scripts/download_model.py
python manage.py check_local_model
```

### Problem: Model folder is incomplete

Run the download script again. It supports resume:

```powershell
python scripts/download_model.py
```

### Problem: App opens but image looks like a placeholder

You are probably using demo mode:

```powershell
$env:OFFLINE_IMAGE_BACKEND="local_pillow"
```

For real AI output, use:

```powershell
$env:OFFLINE_IMAGE_BACKEND="stable_diffusion"
```

### Problem: Generation is very slow

CPU generation is slow. A GPU with CUDA is much faster. The app automatically
uses CUDA if `torch.cuda.is_available()` returns true.

## How The Offline System Works

The app loads a Diffusers Stable Diffusion model from the local folder set in
Django settings:

```python
OFFLINE_IMAGE_MODEL_PATH
```

The generator uses:

```python
local_files_only=True
```

That means Diffusers cannot download missing files during generation. Everything
must already exist on your computer.

## Model Check Command

Run:

```powershell
python manage.py check_local_model
```

It checks whether these required files/folders exist:

```text
model_index.json
unet/
vae/
tokenizer/
text_encoder/
scheduler/
```

This command is fully offline and helps confirm setup before image generation.

## GitHub Notes

These files/folders should not be uploaded to GitHub:

```text
local_models/
media/generated/
.venv/
db.sqlite3
```

They are already ignored in `.gitignore`.

## Viva-Friendly Explanation

Offline Image Maker is a Django project that converts user text into images.
The frontend is made with Django templates, CSS, and JavaScript. The backend uses
Django views, forms, services, SQLite, and local file storage.

Type to Image sends a short prompt to the image generator. Script to Image first
extracts scene details from a longer script, builds a final prompt, and sends it
to the same generator.

For real image generation, the app uses a local Diffusers Stable Diffusion model.
No online API is used during generation. The model is downloaded once during
setup, then the app runs offline.

If CUDA GPU is available, the app uses GPU with `float16`. If not, it uses CPU
with `float32`. CPU works but is slower.
