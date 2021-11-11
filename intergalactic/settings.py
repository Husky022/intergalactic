"""
Django settings for intergalactic project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from intergalactic.secrets import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_summernote',
    'mainapp',
    'authapp',
    'userprofile',
    'adminapp',
    'moderation',
    'django_filters',
    'widget_tweaks',
    'corsheaders',
    'background_task',
    'mptt',

    'debug_toolbar',
    'template_profiler_panel',
    'moneyapp',
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# if DEBUG:
#    def show_toolbar(request):
#        return True
#
#    DEBUG_TOOLBAR_CONFIG = {
#        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
#    }
DEBUG_TOOLBAR_PANELS = [
   'debug_toolbar.panels.versions.VersionsPanel',
   'debug_toolbar.panels.timer.TimerPanel',
   'debug_toolbar.panels.settings.SettingsPanel',
   'debug_toolbar.panels.headers.HeadersPanel',
   'debug_toolbar.panels.request.RequestPanel',
   'debug_toolbar.panels.sql.SQLPanel',
   'debug_toolbar.panels.templates.TemplatesPanel',
   'debug_toolbar.panels.staticfiles.StaticFilesPanel',
   'debug_toolbar.panels.cache.CachePanel',
   'debug_toolbar.panels.signals.SignalsPanel',
   'debug_toolbar.panels.logging.LoggingPanel',
   'debug_toolbar.panels.redirects.RedirectsPanel',
   'debug_toolbar.panels.profiling.ProfilingPanel',
   'template_profiler_panel.panels.template.TemplateProfilerPanel',
]
ROOT_URLCONF = 'intergalactic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainapp.context_processors.category',
                'mainapp.context_processors.search_filter',
                'mainapp.context_processors.notification',
                'mainapp.context_processors.transactions_not_read',
                'mainapp.context_processors.get_sorted_type',

            ],
        },
    },
]

WSGI_APPLICATION = 'intergalactic.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'  # UTC +3

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authapp.IntergalacticUser'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Summernote config
SUMMERNOTE_THEME = 'bs5'
SUMMERNOTE_CONFIG = {
    'iframe': True,
    # You can put custom Summernote settings
    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,

        # Change editor size
        'width': '100%',
        'height': '400',
        'lang': 'ru-ru',
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            # You have to include theme file in 'css' or 'css_for_inplace' before using it.
            'theme': 'monokai',
        },
    },

    # размер файла в байтах
    'attachment_filesize_limit': 20000000
}

# отправление уведомлений на почту
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = "test-intergalactic@mail.ru"
EMAIL_HOST_PASSWORD = "jthgp5GC2L4Bx99WDJdx"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Модерация
MODERATION_STATUS = True
