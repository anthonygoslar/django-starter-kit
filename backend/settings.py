from pathlib import Path
import os
from decouple import config
from celery.schedules import crontab
from .defaults import *

os.environ['S3_USE_SIGV4'] = 'True'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CSRF_TRUSTED_ORIGINS = ["https://example.com"]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'apoloappauth',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Application definition

BANNED_DOMAINS = ['trash-mail.com', 'you-spam.com',
                  're-gister.com', 'fake-box.com', 'trash-me.com', 'opentrash.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    "apps.app_common",
    "apps.app_profiles",
    "apps.app_users",
    # 3rd party apps
    'django_celery_beat',
    'celery',
    'django_elasticsearch_dsl',
    'rest_framework',
    'drf_yasg',
    'whitenoise.runserver_nostatic',
    'corsheaders',
    'silk',
    'channels',
    "phonenumber_field",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'silk.middleware.SilkyMiddleware',  # SilkyMiddleware before CacheMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # make sure to add this line
]


ROOT_URLCONF = 'backend.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME':     config('DATABASE_NAME'),
#         'USER':     config('DATABASE_USER'),
#         'PASSWORD': config('DATABASE_PASSWORD'),
#         'HOST':     config('DATABASE_HOST'),
#         'PORT':     config('DATABASE_PORT'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = config('staticRootLocation')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": (config('REDIS_HOST'), config('REDIS_PORT')),
        },
    },
}

# https://medium.com/@ksarthak4ever/django-handling-periodic-tasks-with-celery-daaa2a146f14
BROKER_URL = config('BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TIME_LIMIT = 30 * 60


ELASTICSEARCH_DSL = {
    'default': {
        'hosts':  "elasticsearch:9200",
        'timeout': 50,  # Increase timeout to 30 seconds or more
      
    },
}



# Celery Beat

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "backend.celery_conf.sample_task",
        "schedule": crontab(minute="*/1"),
    },
}

CACHES = {
    "alternate": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@redis:6379/1",
        "OPTIONS": {
            "DB": 1,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@redis:6379/1",
        "OPTIONS": {
            "DB": 2,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
