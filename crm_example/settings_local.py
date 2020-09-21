from .settings import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(#_kb*5jcq!b#7g@j%bd3ookn0g()574u5^v+8^83atu4g--2i'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Settings to use Google as Oauth Provider
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
