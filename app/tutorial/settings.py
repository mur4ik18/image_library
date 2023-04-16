import os
from pathlib import Path
import mimetypes

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY", 'no')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = int(os.environ.get("DEBUG", default=0))
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS",'*').split(" ")
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
    'rest_framework',
    'advanced_search',
    'posts_collections',
    'posts',
    'auth_system',
    'approve',
    'writers',
    'django_cleanup',
    'apiapp',
    'debug_toolbar',
    'silk',
]
SILKY_META = True
SILKY_PYTHON_PROFILER = True
# SILKY_PYTHON_PROFILER_BINARY = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'tutorial.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]
WSGI_APPLICATION = 'tutorial.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.postgresql',
        'NAME': os.environ.get("SQL_DATABASE", 'name'),
        'USER': os.environ.get("SQL_USER", 'user'),
        'PASSWORD': os.environ.get("SQL_PASSWORD", 'password'),
        'HOST': os.environ.get("SQL_HOST", 'host'),
        'PORT': os.environ.get("SQL_PORT", 5432),
        'TEST': {
            'ENGINE': 'dj_db_conn_pool.backends.postgresql',
            'NAME': 'Test',
        },
        'POOL_OPTIONS': {
            'POOL_SIZE': 50,
            'MAX_OVERFLOW': 10,
            'RECYCLE': 24 * 60 * 60
         }
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s '
                        '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '*': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

mimetypes.add_type("text/css", ".css", True)
STATIC_URL = 'staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = 'images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
HOST = 'address'
