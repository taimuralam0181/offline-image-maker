"""WSGI config for Offline Image Maker."""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "offline_image_maker.settings")

application = get_wsgi_application()
