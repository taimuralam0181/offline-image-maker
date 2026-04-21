"""ASGI config for Offline Image Maker."""
import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "offline_image_maker.settings")

application = get_asgi_application()
