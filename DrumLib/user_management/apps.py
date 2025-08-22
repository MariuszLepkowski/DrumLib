from django.apps import AppConfig


class UserManagementAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_management_app"

    def ready(self):
        import user_management_app.signals
