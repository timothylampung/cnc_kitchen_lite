import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.contrib import admin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k*b$$!%hiswnhp2pad)6(u4x_g)r5w%@&zlv&@2hrz4#f3+#57'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

TASK_UPDATE_BOARD_CAST = 'task_update_board_cast'
REDIS_HOST = 'localhost'

CHANNEL_LAYERS = {
    "default": {
        "CONFIG": {
            # "hosts": [('redis', '6379')],
            "capacity": 1500,  # default 100
            "expiry": 10,  # default 60
            "hosts": [(REDIS_HOST, '6379')]
        },
        "BACKEND": 'channels_redis.core.RedisChannelLayer'
    }
}

STIR_FRY_MODULE = 'STIR_FRY_MODULE'
DEEP_FRY_MODULE = 'DEEP_FRY_MODULE'
GRILLING_MODULE = 'GRILLING_MODULE'
DRINKS_MODULE = 'DRINKS_MODULE'
BOILER_MODULE = 'BOILER_MODULE'
STEAMING_MODULE = 'STEAMING_MODULE'
TRANSPORTER_MODULE = 'TRANSPORTER_MODULE'

HANDLER_TYPE = (
    (STIR_FRY_MODULE, 'STIR_FRY_MODULE'),
    (DEEP_FRY_MODULE, 'DEEP_FRY_MODULE'),
    (GRILLING_MODULE, 'GRILLING_MODULE'),
    (DRINKS_MODULE, 'DRINKS_MODULE'),
    (BOILER_MODULE, 'BOILER_MODULE'),
    (STEAMING_MODULE, 'STEAMING_MODULE'),
    (TRANSPORTER_MODULE, 'TRANSPORTER_MODULE'),
)

MODULE_QUEUE_NAME = [
    ('192.168.42.116', '192.168.42.116'),
    ('192.168.42.117', '192.168.42.117'),
    ('192.168.42.118', '192.168.42.118'),
    ('192.168.42.119', '192.168.42.119'),
    ('192.168.42.120', '192.168.42.120'),
    ('192.168.42.121', '192.168.42.121'),
    ('192.168.42.122', '192.168.42.122'),
    ('192.168.42.123', '192.168.42.123'),
]

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    '192.168.42.116': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    '192.168.42.117': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    '192.168.42.118': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    '192.168.42.119': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    '192.168.42.120': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    '192.168.42.121': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    '192.168.42.122': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    '192.168.42.123': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },

}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'corsheaders',
    'channels',
    'rest_framework',

    'crispy_forms',
    'tinymce',
    'django_rq',

    'marketing',
    'posts',
    'tasks',
    'recipe',
    'module',
    'ingredients',

    'django_seed'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cnc_kitchen_lite.urls'

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

WSGI_APPLICATION = 'cnc_kitchen_lite.wsgi.application'
ASGI_APPLICATION = 'cnc_kitchen_lite.asgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'blogdb',
            'USER': 'blog_admin',
            'PASSWORD': 'testing123',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Tinymce

TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

MAILCHIMP_API_KEY = ''
MAILCHIMP_DATA_CENTER = ''
MAILCHIMP_EMAIL_LIST_ID = ''

# Django Allauth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
SITE_ID = 1
