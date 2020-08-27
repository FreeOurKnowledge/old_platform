"""
Django settings for free_our_knowledge project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../apps')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gd7^%u6zb3%nb%p^_+^4)f1qom2%8l)32#9n#*m$=jd1ndg_zz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_summernote',
    'fok',
    'constance.backends.database',
    'constance',
    'cc_cms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'free_our_knowledge.urls'

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
                'fok.context_processors.add_config'
            ],
        },
    },
]

WSGI_APPLICATION = 'free_our_knowledge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fok',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
        'HOST': 'docker_db_1', #os.environ.get('DB_HOST', '127.0.0.1')
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

AUTHENTICATION_BACKENDS = [
    # 'django.contrib.auth.backends.ModelBackend'
    'fok.backends.OrcidBackend'
]

USE_ORCID = False
BASE_ORCID_URL = None
ORCID_ID = None
ORCID_SECRET = None
ORCID_REDIRECT_URL = None
BASE_ORCID_API_URL = None

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
LOGIN_REDIRECT_URL = '/'

DEV_SETTINGS_MODULE = 'free_our_knowledge.settings.dev'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTH_USER_MODEL = 'fok.User'
SIGNUP_FORM = 'fok.forms.FokSignUpForm'

FIXTURE_FACTORIES = 'free_our_knowledge/resources/fixtures.yml'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'OVERRIDE_SUPPORT_METRICS_TEXT': ("", """
        If this text value is not empty, when a display metric is gonna be shown will be replaced by this text. 
    """
    ),
    'ANONYMOUS_USERS_FACTOR': (0.25, """
        The factor to estimate the impact into the support metric for non registered users.
    """),
    'FRONTPAGE_SENTENCE': (
        'People empowering the future of scholarly communication',
        'The sentence that appears over the image into the front page. '
    ),
    'FRONTPAGE_VIDEO_URL': (
        'https://s3.wasabisys.com/codi.coop/fok-mvp/FreeOurKnowledge_linked2website.mp4',
        'Video url for the front page.'
    ),
    'CAMPAIGNS_TITLE_IN_FRONTPAGE': (
        'Together we can fix academia',
        'Text shown as title on the frontpage for campaigns section.'
    ),
    'INTRODUCTION_TITLE_IN_FRONTPAGE': (
        'Scholarly publishing is broken',
        'Text shown as title on the frontpage for the introduction section.'
    ),
    'ACTIVATE_GREETINGS': (
        True,
        'Activate greetings window.'
    ),
    'TITLE_GREETINGS': (
        'Welcome to Free Our Knowledge!',
        'Title for the pop-up greetings window.'
    ),
    'TEXT_GREETINGS': (
        'This is Free Our Knowledge, give me your mail NOW:',
        'Text for the pop-up greetings window.'
    ),
    'SHOW_SIGNUP_MAILING_ON_GREETINGS': (
        True,
        'Check this if you want to show the sign up for the mailing list on the greetings pop-up.'
    ),
    'COOKIES_TEXT': (
        'We use cookies to ensure that we give you the best experience on our website.',
        'Add text for the cookies warning.'
    ),
    'TWITTER_PROFILE': (
        'https://twitter.com/', ''
    ),
    'FACEBOOK_PROFILE': (
        'https://www.facebook.com/', ''
    ),
    'INSTAGRAM_PROFILE': (
        'https://www.instagram.com/', ''
    ),
    'YOUTUBE_PROFILE': (
        'https://www.youtube.com/', ''
    ),
    'GITHUB_PROFILE': (
        'https://www.github.com/', ''
    )
}

SIGNUP_SEND_MAIL = False
SIGNUP_ACTIVE_USER_BY_DEFAULT = True

FIXTURES_PATH_TO_COVER_IMAGES = 'test-images/logos'

# Storage Service

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = 'codi.coop.test'
AWS_S3_CUSTOM_DOMAIN = f's3.wasabisys.com/{AWS_STORAGE_BUCKET_NAME}'
AWS_S3_ENDPOINT_URL = 'https://s3.wasabisys.com'
AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'cc_lib.storages.MediaStorage'
EXTERNAL_MEDIA_PATH = 'fok/media'
MEDIA_FILE_OVERWRITE = True
