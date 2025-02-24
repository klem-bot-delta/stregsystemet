"""
Django settings for stregsystem project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from configparser import ConfigParser
from io import StringIO
import json


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# @UPGRADE remove the specific unicode "u" here when we finalize the upgrade to
# python3. It's only required to satisfy python2 StringIO
defaults = u"""
[general]
SECRET_KEY=_Secret_
X_FRAME_OPTIONS = SAMEORIGIN

[debug]
DEBUG = True
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIT_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False

[database]
ENGINE = django.db.backends.sqlite3
HOST =
PORT =
NAME = db.sqlite3
USER =
PASSWORD =

[hostnames]
2=127.0.0.1
3=localhost

[logging]
HANDLERS = [
    "console"
    ]
FILE = /tmp/stregsystem.log
LEVEL = DEBUG
"""

cfg = ConfigParser()
cfg.read_file(StringIO(defaults))
cfg.read(os.path.join(BASE_DIR, "local.cfg"))

if cfg.getboolean("debug", "DEBUG") is True:
    print("WARNING: Not in production mode, If you are running on the server, stop right now")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = cfg.get("general", "SECRET_KEY")

# Setting debug to false forces everything else into secure production settings
DEBUG = cfg.getboolean("debug", "DEBUG")

CSRF_COOKIE_SECURE = cfg.getboolean("debug", "CSRF_COOKIE_SECURE")
CSRF_COOKIE_HTTPONLY = cfg.getboolean("debug", "CSRF_COOKIE_HTTPONLY")
CSRF_TRUSTED_ORIGINS = ["fappen.fklub.dk"]
SESSION_COOKIE_SECURE = cfg.getboolean("debug", "SESSION_COOKIT_SECURE")

SECURE_BROWSER_XSS_FILTER = cfg.getboolean("debug", "SECURE_BROWSER_XSS_FILTER")

SECURE_CONTENT_TYPE_NOSNIFF = cfg.getboolean("debug", "SECURE_CONTENT_TYPE_NOSNIFF")

X_FRAME_OPTIONS = cfg.get("general", "X_FRAME_OPTIONS")

# We don't have any default hostnames for debug
# But you really should have some when you are deploying
ALLOWED_HOSTS = []

for e in cfg.items("hostnames"):
    ALLOWED_HOSTS.append(e[1])

# Application definition

INSTALLED_APPS = [
    'stregsystem',
    'stregreport',
    'kiosk',
    'django_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'stregsystem.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'treo.urls'

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

WSGI_APPLICATION = 'treo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': cfg.get("database", "ENGINE"),
        'HOST': cfg.get("database", "HOST"),
        'PORT': cfg.get("database", "PORT"),
        'NAME': cfg.get("database", "NAME"),
        'USER': cfg.get("database", "USER"),
        'PASSWORD': cfg.get("database", "PASSWORD"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Enable the use of old password hashes
# https://docs.djangoproject.com/en/1.10/topics/auth/passwords/#password-upgrades
# TODO: Please do remove in future

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',  # <--- THIS ONE IS UNSAFE
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'da-dk'

TIME_ZONE = 'Europe/Copenhagen'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

INTERNAL_IPS = [
    "127.0.0.1",
]

SELECT2_JS = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/js/select2.min.js'
SELECT2_CSS = (
    '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.4/css/select2.min.css'
)

TEST_RUNNER = 'stregsystem.utils.stregsystemTestRunner'

LOGIN_REDIRECT_URL = '/admin/login'
LOGIN_URL = '/admin/login'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': cfg.get('logging', 'FILE')
        }
    },
    'loggers': {
        '': {
            'level': cfg.get('logging', 'LEVEL'),
            'handlers': json.loads(cfg.get('logging', 'HANDLERS'))
        }
    }
}
