"""
Django settings for electivo_2023 project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from manifest_loader.loaders import DefaultLoader

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*x@(j@3=_b*s*^n60q#xp@^o&8l=#fwjndpfm@ozotx0hnq@x3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'administrator',
    'caracterizacion',
    'mathfilters',
    'manifest_loader',
    'rest_framework',
    'core',

    
    
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

ROOT_URLCONF = 'electivo_2023.urls'

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

WSGI_APPLICATION = 'electivo_2023.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'HOST': 'localhost',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'consultoria',
        'USER': 'postgres',
        'PASSWORD': 'n4ik3l4m3l4'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Chile/Continental'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
#Media files
STATIC_ROOT = '/core/static/'
#Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'core','static','core')

LOGIN_REDIRECT_URL = 'check_profile'
LOGOUT_REDIRECT_URL = 'login'



#Emails
#Emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'#servidor de salida del proveedor de correo, por lo general se usa smtp.dominio
EMAIL_PORT = 587 #Puerto del servidor de salida, el proveedor de correo debe indicar el puerto que usará
EMAIL_HOST_USER = 'especialidaddb@gmail.com'#correo que se usará para el envio, esta casilla debe existir en el servidor CAMBIAR
EMAIL_HOST_PASSWORD = 'qcei finl sffe xbnn'#contraseña de acceso del correo usado en el paso anterior
EMAIL_USE_TLS = True #habilita el protocolo de seguridad que cifra los correos

MANIFEST_LOADER = {
    'output_dir': 'core/static/dist/',  # where webpack outputs to, if not 
    'manifest_file': 'manifest.json',  # name of your manifest file
    'cache': False,  # recommended True for production, requires a server restart to pick up new values from the manifest.
    'loader': DefaultLoader  # how the manifest files are interacted with
    }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}
