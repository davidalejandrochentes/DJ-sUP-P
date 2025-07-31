from .base import *
import os
from dotenv import load_dotenv

load_dotenv(Path.joinpath(BASE_DIR, '.env'))

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('DB_NAME'),
        "USER": os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DB_PASSWORD'),
        "HOST": os.environ.get('DB_HOST'),
        "PORT": os.environ.get('DB_PORT'),
    }
}

STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles')

# Configuración de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 604800  # 7 días en segundos
WHITENOISE_COMPRESSION_ENABLED = True

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF', '').split()

TELEGRAM_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TG_CHAT_ID')

#----------------------------------------------------------------------
# Configuración de Redis para caché
REDIS_HOST = os.environ.get('REDISHOST')
REDIS_PORT = os.environ.get('REDISPORT')
REDIS_DB = os.environ.get('REDISDB')
REDIS_PASSWORD = os.environ.get('REDISPASSWORD')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': REDIS_PASSWORD,
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
            }
        }
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 604800  # 7 días (604800 segundos)
CACHE_MIDDLEWARE_KEY_PREFIX = 'sUP'

#----------------------------------------------------------------------

# Configuración de logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}