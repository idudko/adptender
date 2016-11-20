# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1','192.168.0.136')

ADMINS = (
    ('Ivan U. Dudko', 'dudko.iu@yandex.ru'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'notify@adptender.ru'
if DEBUG:
    EMAIL_HOST = 'localhost'
else:
    EMAIL_HOST = '192.168.0.250'

EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 25

DATABASES = {}
if DEBUG:
    DATABASES['default']={
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT + '/db.sql',
        'USER': 'auction',
        'PASSWORD': 'auction',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'adptender',
        'NAME': 'adptender',
        'PASSWORD': 'nDy37hDwy3kDFjh',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }

DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i'
TIME_FORMAT = 'H:i'
YEAR_MONTH_FORMAT = 'F Y'

DECIMAL_SEPARATOR = ','

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT,'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@a*$)hyy6vwq6k7ny4!)i$4m+^#2%4sjsw1$plio@(yjvllevh'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'breadcrumbs.middleware.BreadcrumbsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    # copied from docs.
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.csrf",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",

    # appended custom value
    #"app.utils.append_privileges",
)

ROOT_URLCONF = 'auction.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.webdesign',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'notification',
    'pagination',
    'registration',
    'treemenus',
    # Мои аппликухи
    'apps.core',
    'apps.accreditation',
    'apps.auction',
    'apps.profile',
    #'apps.storage',
    'apps.defaulter',
    'apps.lot',
    'apps.request',
    'apps.menu_extension',
)

# Сколько дней ждем активацию пользователя
ACCOUNT_ACTIVATION_DAYS = 3
AUTH_USER_EMAIL_UNIQUE = True
AUTH_PROFILE_MODULE = 'profile.Profile'

if DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
        'django.contrib.webdesign',
    )
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
