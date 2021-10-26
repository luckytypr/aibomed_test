from os.path import dirname, abspath, join
from pathlib import Path
from datetime import timedelta
from environ import Env


BASE_DIR: str = dirname(dirname(abspath(__file__)))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
env: Env = Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%5ub0@vw8-3hqwxdb%c-*l!)thv=ug7i(9mh73kjytv-_7(wpk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SIDE_APPS = [
    'corsheaders',
    'rest_framework',
    'django_extensions',
    'django.contrib.sites',
    'django_filters',
    'rest_framework_simplejwt',
    'django_fsm',
    'drf_yasg',
    'rest_framework_simplejwt.token_blacklist',
]

PROJECT_APPS = [
    "apps.users.apps.UsersAppConfig",
    "apps.tasks.apps.TasksAppConfig",
]

INSTALLED_APPS += SIDE_APPS
INSTALLED_APPS += PROJECT_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = 60


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# File access
STATIC_URL: str = '/static/'
STATIC_ROOT: str = join(BASE_DIR, 'staticfiles')
MEDIA_URL: str = '/media/'
MEDIA_ROOT: str = join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SWAGGER settings
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "DEEP_LINKING": True,
}

# AUTH settings
AUTH_USER_MODEL = 'users.User'
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("JWT",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M",
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagisnation",
    "PAGE_SIZE": 100,
    'COERCE_DECIMAL_TO_STRING': False,
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


CELERY_BROKER_URL: str = env.str(var='CELERY_BROKER_URL')
CELERY_RESULT_BACKEND: str = env.str(var='CELERY_RESULT_BACKEND')
CELERY_TIMEZONE: str = env.str(var='CELERY_TIMEZONE')
CELERY_ENABLE_UTC: bool = True
CELERY_ACCEPT_CONTENT = ('application/json',)
CELERY_TASK_SERIALIZER: str = 'json'
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_TASK_ACKS_LATE: bool = True
