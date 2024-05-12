from django.apps import AppConfig


class UserauthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauthentication'

    def ready(self):
        from userauthentication import signals