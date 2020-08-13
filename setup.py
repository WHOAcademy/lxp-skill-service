from setuptools import setup, find_packages

setup(name='lxp-skill-service',
      version='1.1.1',
      packages=find_packages(),
      install_requires=[
          'Django~=3.0.8',
          'psycopg2-binary~=2.8.5',
          'djangorestframework~=3.11.0',
          'nose==1.3.7',
          'coverage==5.2',
          'django-nose==1.4.6',
          'drf-yasg==1.17.1',
          'django-cors-headers==3.4.0',
          'django-filter==2.3.0'
      ],
      scripts=['manage.py'])