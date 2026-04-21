from django.apps import AppConfig


class GeneratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "generator"

    def ready(self):
        """Print a small startup message about the configured local model path.

        This does not load the Stable Diffusion model. It only checks local files
        so students can quickly explain that the app stays offline at startup.
        """
        try:
            from .services.image_generator import get_model_validation_status

            status = get_model_validation_status()
            print("[MODEL CHECK] Offline Image Maker local model setup")
            print(f"[MODEL CHECK] Path: {status['path']}")
            if status["is_valid"]:
                print("[MODEL CHECK] Status: valid Diffusers model folder found.")
            else:
                print(f"[MODEL CHECK] Status: {status['message']}")
        except Exception as exc:
            print(f"[MODEL CHECK] Startup validation skipped: {exc}")
