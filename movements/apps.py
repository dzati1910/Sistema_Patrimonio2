from django.apps import AppConfig


class MovementsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movements'


    def ready(self):
        # Importe os sinais para garantir que eles sejam carregados
        import movements.signals