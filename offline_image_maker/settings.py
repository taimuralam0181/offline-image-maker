"""
Django settings for Offline Image Maker.

This project is designed to run fully offline. The Stable Diffusion model path is
read from an environment variable and must point to files already downloaded on
the user's machine.
"""
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "offline-image-maker-dev-secret-key-change-for-production",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost,testserver",
).split(",")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "generator",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "offline_image_maker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "offline_image_maker.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Offline image generation settings.
# Example Windows value:
# set OFFLINE_IMAGE_MODEL_PATH=C:\models\stable-diffusion-v1-5
OFFLINE_IMAGE_MODEL_PATH = os.environ.get(
    "OFFLINE_IMAGE_MODEL_PATH",
    r"C:\Users\HOTSPOT\OneDrive\Desktop\projectAI\local_models\stable-diffusion",
)
OFFLINE_GENERATED_DIR = MEDIA_ROOT / "generated"
OFFLINE_MODEL_DEVICE = os.environ.get("OFFLINE_MODEL_DEVICE", "auto")
# A valid Diffusers Stable Diffusion folder must contain these entries.
# Keeping this in settings makes the validation rule easy to explain and adjust.
OFFLINE_REQUIRED_MODEL_FILES = [
    "model_index.json",
    "unet",
    "vae",
    "tokenizer",
    "text_encoder",
    "scheduler",
]
# stable_diffusion uses the real local Diffusers model.
# local_pillow is only for classroom/demo mode when no model is available.
OFFLINE_IMAGE_BACKEND = os.environ.get("OFFLINE_IMAGE_BACKEND", "stable_diffusion")
