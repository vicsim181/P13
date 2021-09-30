from config.settings import *


SECRET_KEY = 'supers€cretKey'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # we use the postgresql adaptator
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
