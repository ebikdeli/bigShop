import os
from collections import OrderedDict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',

    'rest_framework',
    "debug_toolbar",
    'django_filters',
    'taggit',
    'django_countries',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'django_quill',
    'silk',
    'sorl.thumbnail',
    'constance',
    # To be able to use database for 'constance'
    'constance.backends.database',
    'watchman',

    'accounts',
    'login',
    'support',
    'product',
    'cart',
    'dashboard',
    'payment',
    'order',
]


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",    # To enable 'django-debug-tool'
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',        # for per site cache
    'corsheaders.middleware.CorsMiddleware',                # To activate 'cors-headers'
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',     # for per site cache
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'silk.middleware.SilkyMiddleware',				   # To enable django-silk
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cart.custom_middleware.InitialSessionMiddleware',      # Customized middleware to check sessions
]


ROOT_URLCONF = 'config.urls'


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 
                os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processor.get_cart',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,
                    }
    }
}


# Using django memcache for caching
"""
CACHES = {
    'default': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600                                        # cache never expires
    }
}
"""

# for cache per site:

# CACHE_MIDDLEWARE_ALIAS = 'apadana_cache'

# CACHE_MIDDLEWARE_SECONDS = 900

# CACHE_MIDDLEWARE_KEY_PREFIX = 'mem'


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


AUTH_USER_MODEL = 'accounts.User'


LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ','

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
# To deploy on Host (Sub folders do not accepted by host!):
# STATIC_ROOT = '/home/<serivce_name>/public_html/static'

STATICFILES_DIRS = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'statics')
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# To deploy on Host:
# MEDIA_ROOT = '/home/<serivce_name>/public_html/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = 'virtin:index'
LOGIN_URL = 'login:signup'

LOGOUT_REDIRECT_URL = 'vitrin:index'

# We can also use 'reverse_lazy' to handle login and logout urls like above examples but we can
# not to use 'reverse_lazy' (but it's recommended for good practice).


TAGGIT_CASE_INSENSITIVE = True


"""
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}
"""


# Cors headers settings (NOTE: Without 'cors', process on diffrent domains and ports could not speak to each other! 'same-origin' only enabled when two process work on same domain and port)
# In ajax request using 'fetch' or any front techs like 'reqct', 'angular' or even an script with 'requests' library, we must enable 'CORS' for the server.
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    'http://127.0.0.1:5500',
    'https://127.0.0.1:5500',
]
# * If we don't set 'CORS_ALLOW_CREDENTIALS = True', We will get this error on client side:
# Access to fetch at 'http://127.0.0.1:8000/add_product_cart' from origin 'http://127.0.0.1:5500' has been blocked by CORS policy: The value of the 'Access-Control-Allow-Credentials' header in the response is '' which must be 'true' when the request's credentials mode is 'include'.
# NOTE: Remember that without this field, any cookie sent by client, does not checked by server!
CORS_ALLOW_CREDENTIALS = True

# * To be able to let 'X-CSRFToken' header checked by server (this header sent by any client) we must 
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
    'http://*:*'
]


# CKEditor settings
# each one of three below is acceptable
CKEDITOR_BASEPATH = f"{STATIC_URL}ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

# CKEditor optional settings
# CKEDITOR_CONFIGS = {
    # 'default': {
        # 'toolbar': 'full',
        # 'toolbar': 'basic',
        # 'height': 300,
        # 'width': 300,
    # },
# }


# django-constance settings
# https://django-constance.readthedocs.io/en/latest/
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = OrderedDict([
    ('email', ('bigshop@gmail.com', 'Main email of the server')),
    # About us field
    ('about_us', ('', 'About Us field shown to users in "about us page"')),
    # Address of the links used in website
    ('instagram', ('', 'Instagram link')),
    ('linkedin', ('', 'Linkedin')),
    ('twitter', ('', 'Twitter')),
    ('whatsapp', ('', 'Whatsapp')),
    ('facebook', ('', 'Facebook')),
])

CONSTANCE_CONFIG_FIELDSETS = {
    'Email Options': ('email',),
    'About Us': ('about_us',),
    'Links': {'fields': ['instagram', 'linkedin', 'twitter', 'whatsapp', 'facebook'], 'collapse': True},
}

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True


# By default django uses 'redis' to store 'constance' variables. to use database we should follow this document:
# https://django-constance.readthedocs.io/en/latest/backends.html#database
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


# django-debug-toolbar settings

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
