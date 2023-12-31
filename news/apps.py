from time import sleep

from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from jobs import updater
        sleep(2)
        updater.start()
