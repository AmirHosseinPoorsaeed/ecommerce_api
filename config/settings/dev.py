from .common import *

SECRET_KEY = '32ul8v600bl5)i)+^=yz6z9e1&glc=1bl!ocn%3l!n0lio8xy)'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'store_dev',
        'USER': 'postgres',
        'PASSWORD': '1381amir',
        'PORT': '5432',
    }
}