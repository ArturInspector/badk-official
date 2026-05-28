import os
import signal

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Прочее'

    def ready(self):
        from rosetta.signals import post_save as rosetta_post_save
        rosetta_post_save.connect(_reload_gunicorn)


def _reload_gunicorn(sender, **kwargs):
    try:
        with open('/tmp/gunicorn.pid') as f:
            os.kill(int(f.read().strip()), signal.SIGHUP)
    except Exception:
        pass
