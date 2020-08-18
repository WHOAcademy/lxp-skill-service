from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test',
        'USER': 'bastian',
        'PASSWORD': 'balthazar',
        'HOST': 'localhost',
        'PORT': 5432
    }
}
