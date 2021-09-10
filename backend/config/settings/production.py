from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('DJANGO_KEY')
DEBUG = False
ALLOWED_HOSTS = ['localhost']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # we use the postgresql adaptator
        'NAME': os.getenv('POSTGRESQL_DBNAME'),
        'USER': os.getenv('POSTGRESQL_USER'),
        'PASSWORD': os.getenv('POSTGRESQL'),
        'HOST': '',
        'PORT': '5432',
    }
}