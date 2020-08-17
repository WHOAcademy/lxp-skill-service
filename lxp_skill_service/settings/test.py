from .base import *
import importlib

settings = importlib.import_module('lxp_skills_service.settings.' + os.getenv('APP_ENV'))

settings.DATABASES['default']['HOST'] = os.getenv('TEST_DATABASE_SERVICE_HOST')
settings.DATABASES['default']['PORT'] = os.getenv('TEST_DATABASE_SERVICE_PORT')

DATABASES = settings.DATABASES