# Offline Image Maker

A fully offline Django web app for generating images from short prompts or longer scene scripts using a local Stable Diffusion model.

## Offline Setup

1. Create and activate a virtual environment.
2. Install packages from `requirements.txt`.
3. Download the Stable Diffusion v1.5 model once:

```powershell
python scripts/download_model.py
```

4. Set the local model path:

```powershell
$env:OFFLINE_IMAGE_MODEL_PATH="C:\models\stable-diffusion"
```

5. Run migrations and start Django:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

6. Open `http://127.0.0.1:8000/`.

The app does not use OpenAI, Stability, Replicate, Hugging Face hosted inference, or any cloud API. `diffusers` is configured with `local_files_only=True`, so runtime Stable Diffusion generation expects all model files to already exist locally.

## Local Model Setup

This project needs a Stable Diffusion model that is already saved on your
computer in Diffusers format. The app does not download the model at runtime and
does not call any API.

The included download script uses:

```text
runwayml/stable-diffusion-v1-5
```

This model gives better and more realistic results than tiny demo models. It is
larger, so the first download can take time and needs enough disk space.

Place the model folder here:

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
  safety_checker/        optional depending on model
  feature_extractor/     optional depending on model
```

What the required files mean:

- `model_index.json` tells Diffusers which pipeline components are inside the folder.
- `unet/` is the main denoising network that creates the image structure.
- `vae/` converts the model's hidden latent result into a normal image.
- `tokenizer/` breaks your prompt text into tokens.
- `text_encoder/` converts those tokens into numbers the model can understand.

The validation helper in `generator/services/image_generator.py` checks these
entries before generation. If something is missing, the UI shows a clear setup
error instead of a confusing model loading failure.

## How To Test Model Setup

Run this command before using Type to Image or Script to Image:

```powershell
python manage.py check_local_model
```

This command is fully offline. It does not load the full model and does not
download anything. It only checks the folder path from Django settings and prints
which required entries are present or missing.

Expected success message:

```text
Model folder is valid.
You can run: python manage.py runserver
```

If the model is missing, the command shows the configured path and the missing
entries, such as `model_index.json`, `unet`, `vae`, `tokenizer`, or
`text_encoder`.

## Backend Modes

By default, `OFFLINE_IMAGE_BACKEND=stable_diffusion` so the app does not show a
placeholder/demo image when you expect real AI output.

For real Stable Diffusion output, set both variables before running the server:

```powershell
$env:OFFLINE_IMAGE_MODEL_PATH="C:\models\stable-diffusion"
$env:OFFLINE_IMAGE_BACKEND="stable_diffusion"
python manage.py runserver
```

For strict Stable Diffusion only:

```powershell
$env:OFFLINE_IMAGE_BACKEND="stable_diffusion"
```

## Viva-Friendly Explanation

Offline Image Maker is a Django web application that generates images from text.
The user can enter a short prompt in Type to Image or paste a longer scene in
Script to Image. Script to Image first extracts useful visual details and builds
a final prompt.

The project stays fully offline because it loads a Stable Diffusion Diffusers
model from a local folder using Django settings. The code uses
`local_files_only=True`, so Diffusers is not allowed to download missing files.
No OpenAI, Stability, Replicate, hosted Hugging Face inference, or cloud API is
used.

Before generation, the validation helper checks that the local model folder has
the important Diffusers components: `model_index.json`, `unet`, `vae`,
`tokenizer`, and `text_encoder`. The `check_local_model` management command lets
the student test this setup from the terminal before running image generation.

## GitHub Notes

Do not upload the local Stable Diffusion model, generated images, virtual
environment, or SQLite database to GitHub. They are ignored by `.gitignore`:

```text
local_models/
media/generated/
.venv/
db.sqlite3
```

After cloning the project on another computer, run:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python scripts/download_model.py
python manage.py check_local_model
python manage.py runserver
```
