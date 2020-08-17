from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neverendingblog',
        'USER': 'bastian',
        'PASSWORD': 'balthazar',
        'HOST': '172.30.105.228',
        'PORT': '5432',
    }
}
