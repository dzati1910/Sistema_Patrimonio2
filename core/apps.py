# core/apps.py
from django.apps import AppConfig
from django.contrib import admin
from django.contrib.auth import get_user_model

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .dash_apps import create_dashboard_app
        create_dashboard_app()
