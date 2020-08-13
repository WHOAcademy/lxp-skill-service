"""
ASGI config for lxp_skill_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""


from django.core.asgi import get_asgi_application
from lxp_skill_service.preps import set_default_env, load_sample_data

set_default_env()
load_sample_data()

application = get_asgi_application()
