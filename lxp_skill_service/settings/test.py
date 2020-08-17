from .base import *

DATABASES['default']['HOST'] = os.getenv('TEST_DATABASE_SERVICE_HOST')
DATABASES['default']['PORT'] = os.getenv('TEST_DATABASE_SERVICE_PORT')
