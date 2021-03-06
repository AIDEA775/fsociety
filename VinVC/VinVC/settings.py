"""
Django settings for VinVC project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u!7pvmz-t)aee1coxp#&l$^*5id(1jyxsm^yslwe@v&8fjtyqe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.vinvc.com', '192.168.0.12']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'social.apps.django_app.default',
    'channels',

    # Project apps
    'login.apps.LoginConfig',
    'user.apps.UserConfig',
    'search.apps.SearchConfig',
    'video.apps.VideoConfig',
    'friendship.apps.FriendshipConfig',
    'chat_room.apps.ChatRoomConfig',
    'video_room.apps.VideoRoomConfig'
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

ROOT_URLCONF = 'VinVC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'VinVC/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',

                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',

                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Python Social Auth Context Processors
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'VinVC.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# OAuth backends
# http://python-social-auth.readthedocs.io/en/latest/configuration/django.html#authentication-backends

AUTHENTICATION_BACKENDS = (
    # Social OAuth
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',

    # Our backend
    'login.backend.UsernameOrEmailBackend',
)


# http://python-social-auth.readthedocs.io/en/latest/pipeline.html
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.user.user_details',
)


# Topic model reference for Chat Room
TOPIC_MODEL = 'video_room.VideoRoom'


# Auth settings
# https://docs.djangoproject.com/en/1.10/ref/settings/#login-url
LOGIN_URL = 'login:index'
AUTH_USER_MODEL = 'user.CustomUser'


# OAuth keys
# https://python-social-auth.readthedocs.io/en/latest/backends/index.html
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '705222363656-5ng8t00km43m9autga4sdc4jrn5sjm0q.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YktK-5yt8HRlmwUe0acfBXDz'

SOCIAL_AUTH_FACEBOOK_KEY = '1798770117036103'
SOCIAL_AUTH_FACEBOOK_SECRET = '8292bc09a6835e8d328cfcfbbf5706b8'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}

SOCIAL_AUTH_TWITTER_KEY = '6rNAfPUpjGgJZkkWswOFWM2vR'
SOCIAL_AUTH_TWITTER_SECRET = '8jAgdx8NArfD0w63Y7cehP880PEyxhbmbS1lpWK2vcgCkoYDYp'


# OAuth globals
# https://python-social-auth.readthedocs.io/en/latest/configuration/settings.html
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/feed/"


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Argentina/Cordoba'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Valid video extension
VIDEO_TYPES = ['video/web', 'video/webm', 'video/mp4', 'video/egg']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "VinVC/static")]

# Channel settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
        "ROUTING": "VinVC.routing.channel_routing",
    },
}
