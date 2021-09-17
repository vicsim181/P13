from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # we use the postgresql adaptator
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# STATIC_URL = '/static/static/'
# MEDIA_URL = 'static/media/'

# STATIC_ROOT = '/vol/web/static'
# MEDIA_ROOT = '/vol/web/media'


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
