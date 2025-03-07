from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        from django.conf import settings
        if settings.DEBUG:  # ✅ Prevents running the scheduler multiple times in development
            from .tasks import start_scheduler
            start_scheduler()
