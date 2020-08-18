from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'bastian',
        'PASSWORD': 'balthazar',
        'HOST': os.getenv('TEST_DATABASE_SERVICE_HOST'),
        'PORT': os.getenv('TEST_DATABASE_SERVICE_PORT'),
    }
}
