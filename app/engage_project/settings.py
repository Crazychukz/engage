

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'z#d9l*z_ps+ko2te8uj-%@!3y=oyw3-j*($c*-$dielboj-=p!'
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'engage',
    'engage_project',
    'multiselectfield'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'engage_project.urls'
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
WSGI_APPLICATION = 'engage_project.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
INTERNAL_IPS = [
    '127.0.0.1'
]

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'host'
)

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


IMPORT_EXPORT_USE_TRANSACTIONS = True


IPWARE_META_PRECEDENCE_ORDER = (
     'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',
     'HTTP_CLIENT_IP',
     'HTTP_X_REAL_IP',
     'HTTP_X_FORWARDED',
     'HTTP_X_CLUSTER_CLIENT_IP',
     'HTTP_FORWARDED_FOR',
     'HTTP_FORWARDED',
     'HTTP_VIA',
     'REMOTE_ADDR',
 )