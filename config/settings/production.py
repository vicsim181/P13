from .base import *
import os
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.environ.get('DJANGO_KEY')
DEBUG = False
ALLOWED_HOSTS = ['.herokuapps']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # we use the postgresql adaptator
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PWD'),
        'HOST': '',
        'PORT': 5432,
    }
}


CORS_ALLOWED_ORIGINS = [
    os.environ.get('CORS_FRONTEND')
]


sentry_sdk.init(
    dsn="https://1d4c9e58518f4fc18b84065cd6b4fe31@o622128.ingest.sentry.io/5953587",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


django_heroku.settings(locals())
