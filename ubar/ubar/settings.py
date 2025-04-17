"""
Django settings for ubar project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d%48=b0)hhpb!_h!_w3cj$)=vo&kdad@9vvdrb8*z1qndzs8=8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1",]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
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

ROOT_URLCONF = 'ubar.urls'

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

WSGI_APPLICATION = 'ubar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres', 
        'PASSWORD': 'postgres', 
        'HOST': 'db', 
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
    'user.authentication.IsAuthenticatedWithToken',
]
}

import os
from dotenv import load_dotenv

load_dotenv()

# JWT Settings 
""" Note that private and public key should be in .env file """

JWT_EXPIRATION_SECS = 20 * 60
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_PRIVATE_KEY="""-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCd90HCZ8sYkbuB
pymsEYgqcFb3Pcq2sbQN7QDuu09z2/A6nCDOPsZzxfU2ibp404IKKTYG42hJJ88M
TZ80llqsRUR2sdY82qdhRae1YJRMAEYxE2xsZQ+/4b1cKaHWd5PhD0bdx8S4VHjX
a+wXeyQs5DepyVujl0NMeW4WdDdCdyxGHlmmgRfNWSh1YkxBLTOVDCAZo5vN3EUC
3g5S9IbN7JxYQUjv2EtD9EjCAy4Z2KX3XAthrq9NxPt6MGGQaJbAIHkI9igMF+Oc
XlIZWyy+1cjOT6rs+LnL2sXJzIfwQh0t+of+/28NYAOBOoDfQzrdk2ic7wigNRKB
L3M1wW3jAgMBAAECggEABOCXA7EfuLT7NKAcLcdmzGSmksCyKxzmgc2RC032QI4I
Z07dxnBywS1aCmKLQuLI75ZhKCpKVIPppSgaY83Go+4JlJ6eDkf0BhFYAcYnHgee
IzLF1Lz0FQkbxyYz7ILJqpfFqOBbpxNYndIjun/fWJF9VH02mqD3f3t6VjAlaqRl
4HiD5/aujcgWust4tybKwvakoVs1m8/fkMBQ4aCYdhpIeLak1s2Y6RoaADSoiybp
8hfCy/HJ2tYqw1xbAj7cm9xr2wzcsiWociztSwHyny6vZSYkOpluV/ZhmmhZAoj1
xXLlTU0aKVVX06LPkIB74DOkR1LdXNZdxfxf6PUo3QKBgQDaKZYV0DPtIrZUIWfx
KaJZWyRt7Zens3gXSt+oyZTCKbuYFNsX7ac2RsAsOJFCuSsDnZW1cDvZaNjxJDv/
Kqoh+sMYBt81g2qTZJwnBqu6NVvQz9gRdQO0KrF7mfItYNV+Z4ra9AUoNZQHpZXc
H8iY991az7Zb6W/Ab4unZxbefwKBgQC5XPD4cBFCpT2+ZIaYPuMbSPjj1CPed3G7
JSBpdzjq0sff5B60ZkWdB3MaKFNl7g/8bWvkf3L8yALM2MEptOT/dvxhAwLM9U6r
ZE6qWpPqE2aKAvQq3Yb2Zeyueb43BlnLUcUKcrsWheD2/WejgavMYeHETTwhVXP1
Wm36UnwGnQKBgGeMCYJ8+ch6C1RPLsiWXEpRKi9K8ApW8o8LqLCyTPsDV9jNPVhU
ImNunVPf3YJv5OyoZSBjDuUYELAT5K4uD+Zk4SiMSnFZ2MHwpPUZA3U0Ukn//Kv8
gC+JfAgQf5PuPCbs+kkGPVRiacpfW4vJQiroqpWptQJXAAW0a/KeyYn9AoGAUIEE
CvIpHOfFNB5WsmKFogEET3aACYuYsm3CcOudpabbtepOR40vaK6ml9KxvdAx0zD2
reuIVi7LwInXArUUy7qyi7OSEM/tVdSfsa7bFMtOOlxkDQXfKr5Dl9c5/I3ei8Y8
rHf9tx93/+04iLO1mHNeaTIeDmAdl46puxD92qUCgYB+eIhqB7gN+nr6od209rSs
1NZJ2mYq0u+AO0w5P2LHcC+P3xpXArhOaC+u9LwXX32UTqKUl2jd2ANbt5pMbbH+
I2a8LO1p8jJLpacsYg6CKaKqGa8rRkJSDLguP/jI+wQWgbre5n+97aqylvFgAfi7
8jKgBOFFy2wr4N0B5ezOUg==
-----END PRIVATE KEY-----"""
JWT_PUBLIC_KEY="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnfdBwmfLGJG7gacprBGI
KnBW9z3KtrG0De0A7rtPc9vwOpwgzj7Gc8X1Nom6eNOCCik2BuNoSSfPDE2fNJZa
rEVEdrHWPNqnYUWntWCUTABGMRNsbGUPv+G9XCmh1neT4Q9G3cfEuFR412vsF3sk
LOQ3qclbo5dDTHluFnQ3QncsRh5ZpoEXzVkodWJMQS0zlQwgGaObzdxFAt4OUvSG
zeycWEFI79hLQ/RIwgMuGdil91wLYa6vTcT7ejBhkGiWwCB5CPYoDBfjnF5SGVss
vtXIzk+q7Pi5y9rFycyH8EIdLfqH/v9vDWADgTqA30M63ZNonO8IoDUSgS9zNcFt
4wIDAQAB
-----END PUBLIC KEY-----"""


# OTP and PASSWORD
OTP_EXPIRE_TIME_SEC = 5 * 60  # how long an OTP is valid?
OTP_RESEND_DELAY_SEC = (
    2 * 60
)  # how much user should wait until asking to resending the otp
OTP_MAX_RETRY_COUNTS = 3  # max retries for otp
OTP_DIGITS = 6
OTP_LOWER_BOUND = 10 ** (OTP_DIGITS - 1)
OTP_UPPER_BOUND = (10**OTP_DIGITS) - 1
PASSWORD_MAX_LENGTH = 25
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_RETRY_COUNTS = 3  # Max password failed attempts per user
OTP_AND_PASSWORD_BAN_TIME_SEC = 3600 # Ban duration (in seconds) for phone/IP