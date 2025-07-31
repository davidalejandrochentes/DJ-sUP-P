from .base import *

SECRET_KEY = 'django-insecure-zhh5)-7-g572%$8)i6m%tbpbt4ua7*6lqy*rdin3uh&24^%u-2'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TELEGRAM_BOT_TOKEN = '7745404825:AAFDs9Jn7-I814WakBspVSgF8QXkef9GmwE'
TELEGRAM_CHAT_ID = '5992843153'