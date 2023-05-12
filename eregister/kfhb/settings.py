import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o+yb*_k0je5qiz2_hep(r-u#uu8*^1b!wvs3z(xedu4ij+w2i+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ebanking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ebanking.middleware.CustomMiddleware',
]

ROOT_URLCONF = 'kfhb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'kfhb.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bahrain'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

"""
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
#STATIC_URL = os.path.join(PROJECT_DIR,'static/')
#STATIC_URL = os.path.join(BASE_DIR,'static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'),]
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')
"""

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/eregister/static/'
# STATIC_URL = os.path.join(PROJECT_DIR,'static/')
# STATIC_URL = os.path.join(BASE_DIR,'static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/'), ]
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
