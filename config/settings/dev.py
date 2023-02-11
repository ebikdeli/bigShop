from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-yadhs4-b&bm7_e!rm^yxdgi!%!prb)my-gf+9x5)hgw)mec+4c'

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Security srttings
SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

try:
    from .local import *
except ImportError:
    pass
