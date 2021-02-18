from django.apps import AppConfig


class FrontendConfig(AppConfig):
    name = 'apps.frontend'

    def ready(self):
        import apps.frontend.signals
        import apps.frontend.tests
