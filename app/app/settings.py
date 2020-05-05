"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-hxl&df)hn8$-g+j5%u9a4oqaaiz@sqrnm$wk=goyddhx(kpp9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '.demo.local', '192.168.1.11']


# Application definition

SHARED_APPS = [
    'django_tenants',
    'customer',
    'user',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'donate',
    'crispy_forms',
    'mathfilters',
    'ckeditor',
]

TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'user',
    'school.apps.SchoolConfig',
    'feed.apps.FeedConfig',
    'task.apps.TaskConfig',
    'rest_framework',
    'ckeditor',
    'comments',
]

INSTALLED_APPS = list(set(SHARED_APPS + TENANT_APPS))

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PUBLIC_SCHEMA_NAME = 'public'
PUBLIC_SCHEMA_URLCONF = 'app.public_urls'
ROOT_URLCONF = 'app.urls'
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

WSGI_APPLICATION = 'app.wsgi.application'

#WSGI_APPLICATION = 'wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'HOST':'localhost',
        'NAME':'ls_sms_saas',
        'USER':'wisner',
        'PASSWORD':'password',
        'PORT':'5432',
        #'HOST': os.environ.get('DB_HOST'),
        #'NAME': os.environ.get('DB_NAME'),
        #'USER': os.environ.get('DB_USER'),
        #'PASSWORD': os.environ.get('DB_PASS'),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)



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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"

STATICFILES_FINDERS = (
    'django_tenants.staticfiles.finders.TenantFileSystemFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MULTITENANT_STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "tenants/%s/static"),
]

STATICFILES_STORAGE = "django_tenants.staticfiles.storage.TenantStaticFilesStorage"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # dev only after collecting static schemas
]


CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'user.User'

TENANT_MODEL = "customer.Client" # app.Model
TENANT_DOMAIN_MODEL = "customer.Domain" # app.Model

# My constants
MY_DEMO_DOMAIN = '.demo.local'
SUPER_USER_PASSORD_LENGTH = 7
# End my constants


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

MULTITENANT_RELATIVE_STATIC_ROOT = "tenants/%s"
os.path.join(BASE_DIR, "tenants/%s/static"),
MULTITENANT_RELATIVE_MEDIA_ROOT = "%s/"


LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = "/feed"


LOGIN_EXEMPT_URLS = (
        'accounts/logout/',
        'accounts/password_reset/',
        'accounts/password_reset/done/',
        'accounts/reset/<uidb64>/<token>/',
        'accounts/password_reset/complete/',
    )

# Mail Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('MY_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('MY_EMAIL')
SERVER_EMAIL = os.environ.get('MY_EMAIL')
EMAIL_PORT = 587



#Stream API Keys