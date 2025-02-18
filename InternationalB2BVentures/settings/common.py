# Python imports
import os
from os.path import abspath, basename, dirname, join, normpath
import sys

# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
BASE_DIR = DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(BASE_DIR)
RUN_DIR = join(PROJECT_ROOT, 'run')

# the name of the whole site
SITE_NAME = basename(BASE_DIR)

# collect static files here
STATIC_ROOT = join(RUN_DIR, 'static')

# collect media files here
MEDIA_ROOT = join(RUN_DIR, 'media')

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# For white noise static files serving.
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# WHITENOISE_MANIFEST_STRICT = False

# Use our custom user model instead of django's default user model 
# AUTH_USER_MODEL = 'accounts.User'

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))

# ##### APPLICATION CONFIGURATION #########################

# these are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cities_light',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
]

AUTHENTICATION_BACKENDS = [
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },

]

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Internationalization
USE_I18N = True
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('hi', 'Hindi'),
    ('de', 'Dutch')
]

# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(RUN_DIR, 'SECRET.key'))

# these persons receive error notification
ADMINS = (
    ('yazeed hasan', 'yazeed.hasan.97@gmail.com'),
)
MANAGERS = ADMINS

# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '{}.wsgi.application'.format(SITE_NAME)

# the root URL configuration
ROOT_URLCONF = '{}.urls'.format(SITE_NAME)

# the URL for static files
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

# Default auto field for id fields of all apps
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# adjust the minimal login
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:login"

# If users check the remember me checkbox,
# their session expiry date will be extended to stay logged in 
REMEMBER_ME_SESSION_EXPIRY = 7  # IN DAYS

# finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string

        if not os.path.exists(RUN_DIR):
            os.mkdir(RUN_DIR)

        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception(f"Could not open {SECRET_FILE} for writing!")

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'International B2B Ventures API',
    'DESCRIPTION': 'This is the API for International B2B Ventures',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
   
}

