#!/usr/bin/env python
"""Django command-line utility for Offline Image Maker."""
import os
import sys


def main():
    """Run administrative tasks such as migrations and the development server."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "offline_image_maker.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is not installed. Activate your virtual environment and run "
            "`pip install -r requirements.txt`."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
