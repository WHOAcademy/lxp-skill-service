import os

from django.core.exceptions import ImproperlyConfigured
from django.core import management
from django.core.management.commands import loaddata

environment = os.getenv("APP_ENV")

if environment is None:
    raise ImproperlyConfigured("The APP_ENV environment must not be empty.")


def set_default_env():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lxp_skill_service.settings.{env}'.format(env=environment))


def load_sample_data():
    management.call_command(loaddata.Command(), 'sample_data.json', verbosity=0)
