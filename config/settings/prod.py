from .common import *


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = bool(os.environ.get('DJANGO_DEBUG', default=0))

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": os.environ.get('POSTGRES_ENGINE'),
        "NAME": os.environ.get('POSTGRES_DB'),
        "USER": os.environ.get('POSTGRES_USER'),
        "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
        "HOST": os.environ.get('POSTGRES_HOST'),
        "PORT": os.environ.get('POSTGRES_PORT'),
    }
}

REDIS_URL = os.environ.get('DJANGO_REDIS_URL')

# Redis settings
CELERY_BROKER_URL = REDIS_URL
