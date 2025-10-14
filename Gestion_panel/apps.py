from django.apps import AppConfig


class GestionPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Gestion_panel'

    def ready(self):
        import Gestion_panel.siganls