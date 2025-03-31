"""
Django settings for OpenClubManager project.

Generated by 'django-admin startproject' using Django 4.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import cloudinary
if os.path.exists('env.py'):
    import env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
LOGIN_URL = '/login/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')




# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [ 'localhost', '8000-joesuth13-openclubmanag-wf8lig7ea43.ws.codeinstitute-ide.net', 'https://*.herokuapp.com', 'openclubmanager-fbf0e93c3ef0.herokuapp.com', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://*.codeinstitute-ide.net', 'https://*.herokuapp.com']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "django_htmx",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cloudinary_storage',
    'cloudinary',
    'bootstrap5',
    'colorfield',
    'crispy_forms',
    'crispy_bootstrap4',
    'bootstrap_datepicker_plus',
    "django_flatpickr", 
    'dashboard',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'allauth.account.middleware.AccountMiddleware',
]



ROOT_URLCONF = 'OpenClubManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context_processors.customization_settings',
                'dashboard.context_processors.timetables',
                'dashboard.context_processors.stripe_context',
            ],
        },
    },
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'OpenClubManager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Fallback to default SQLite database for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

print("DATABASE_URL:", DATABASE_URL)
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)



DJANGO_FLATPICKR = {
    # Name of the theme to use
    # More themes: https://flatpickr.js.org/themes/
    "theme_name": "dark",
    #
    # Complete URL of theme CSS file
    # theme_name is ignored if theme_url is provided
    # "theme_url": "https://..",
    #
    # Global HTML attributes for flatpickr <input> element
    # "attrs": {
    #     "class": "my-custom-class",
    #     "placeholder": "Select Date..",
    # },
    #
    # Global options for flatpickr
    # More options: https://flatpickr.js.org/options/
    # Some options are managed by this package e.g mode, dateFormat, altInput
    # "options": {
    #     "locale": "bn",             # locale option can be set here only
    #     "altFormat": "m/d/Y H:i",   # specify date format on the front-end
    # }
    # You can set date and event hook options using JavaScript, usage in README.
    #
    # HTML template to render the flatpickr input
    # Example: https://github.com/monim67/django-flatpickr/blob/2.0.0/dev/myapp/templates/myapp/custom-flatpickr-input.html
    # "template_name": "your-app/custom-flatpickr-input.html",
    #
    # Specify CDN roots. Choose where from static JS/CSS are served.
    # Can be set to localhost (offline setup) or any other preferred CDN.
    # The default values are:
    #    "flatpickr_cdn_url": "https://cdn.jsdelivr.net/npm/flatpickr@4.6.13/dist/",
    #    "app_static_url": "https://cdn.jsdelivr.net/gh/monim67/django-flatpickr@2.0.0/src/django_flatpickr/static/django_flatpickr/",
    #
    # Advanced:
    # If you want to serve static files yourself without CDN (from staticfiles) and
    # you know how to serve django static files on production server (DEBUG=False)
    # Then download and extract https://registry.npmjs.org/flatpickr/-/flatpickr-4.6.13.tgz
    # Copy the dist directory (package/dist) to any of your static directory and rename it to flatpickr
    # and use following options
    #    "flatpickr_cdn_url": "flatpickr/",
    #    "app_static_url": "django_flatpickr/",
    }
