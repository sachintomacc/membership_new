import os
from decouple import config
from django.conf.global_settings import STATIC_ROOT, STATICFILES_DIRS
from django.contrib.messages import constants as messages
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-warning',
    messages.INFO: 'alert-warning',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-warning',
}

INTERNAL_IPS = [
    '127.0.0.1',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.herokuapp.com', '127.0.0.1', 'localhost', '.example.com','bc81a8550254.ngrok.io']

CORS_ORIGIN_WHITELIST = ('https://example.com', 'https://bc81a8550254.ngrok.io',)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'django.contrib.sites',
    'sslserver',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft',
    'django_shortcuts',
    'django_countries',
    'stripe',
    'djstripe',
    'corsheaders',
    'crispy_forms',
    'social_django',
    'social.apps.django_app.default',
    'core',
    'membership',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'project.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles_dirs')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.yahoo.YahooOpenId',

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# facebook
SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET')

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = ['first_name', 'last_name']
SOCIAL_AUTH_FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'popup', }

# twitter
SOCIAL_AUTH_TWITTER_KEY = config('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = config('SOCIAL_AUTH_TWITTER_SECRET')

# google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')


# linkedin
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = config('SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = config(
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_emailaddress', 'r_liteprofile']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = [
    'email-address', 'headline', 'industry']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('first-name', 'first_name'),
    ('last-name', 'last_name'),
    ('email-address', 'email_address'),
    ('headline', 'headline'),
    ('industry', 'industry')
]
FIELD_SELECTORS = ['email-address', ]

LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress','r_fullprofile']

LINKEDIN_EXTRA_FIELD_SELECTORS = ['email-address','positions', 'headline','summary','picture-url','site-standard-profile-request','public-profile-url','location','interests','skills','languages',]

LINKEDIN_EXTRA_DATA = [('id', 'id'), ('first-name', 'first_name'), ('last-name', 'last_name'), ('email-address', 'email_address'), ('positions', 'positions'), ('summary', 'summary'), ('headline', 'headline'), ('picture-url', 'picture_url'),
 ('site-standard-profile-request', 'site_standard_profile_request'), ('public-profile-url', 'public_profile_url'), ('location', 'location'), ('interests', 'interests'), ('skills', 'skills'), ('languages', 'languages'),]

# instagram
SOCIAL_AUTH_INSTAGRAM_KEY = config('SOCIAL_AUTH_INSTAGRAM_KEY')
SOCIAL_AUTH_INSTAGRAM_SECRET = config('SOCIAL_AUTH_INSTAGRAM_SECRET')
SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = [('user', 'user'), ]





SITE_ID = 1
STRIPE_KEY = config('STRIPE_KEY')
SESSION_COOKIE_AGE = 60 * 60 * int(config('LOGIN_DAYS_THRESHOLD'))


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)



SOCIALACCOUNT_PROVIDERS = {
    'microsoft': {
        'APP': {
            'client_id': config('MICROSOFT_CLIENT_ID'),
            'secret': config('MICROSOFT_SECRET'),
            'key': ''
        }
    }
}



STRIPE_LIVE_PUBLIC_KEY = ''
STRIPE_LIVE_SECRET_KEY = ''
STRIPE_TEST_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')
STRIPE_TEST_SECRET_KEY = config('STRIPE_KEY')
STRIPE_LIVE_MODE = False  # Change to True in production
# Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_WEBHOOK_SECRET = config('DJSTRIPE_WEBHOOK_SECRET')


