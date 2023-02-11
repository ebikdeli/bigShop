"""
VERY IMPORTANT NOTE (THIS WAS BEFORE DJANGO==3.2):
When using signals, we must know that the app signals used in should be totally named to be able execute signals.
For example 'some_app' app total name is 'SomeAppConfig'.
We can do this in 2 ways:
1- in INSTALLED_APPS in 'settings.py' file we use whole name. for example:
instead of this:
INSTALLED_APPS = [                          INSTALLED_APPS = [
    'accounts',         we use this:              'accounts.apps.AccountsConfig',     
]
2- In <app_name>.__init__.py define a variable named 'default_app_config' with value of total name:
for example for accounts app we do this:
in accounts.__init__.py we write: default_app_config = 'accounts.apps.AccountsConfig'
https://docs.djangoproject.com/en/4.0/ref/applications/
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # If we put this application in a folder named 'apps' with absolute path
    # './apps' to project_base path (where manage.py resides):
    # name = 'apps.accounts'

    def ready(self):
        from . import signals

### for more information about how to implement signals:
# https://docs.djangoproject.com/en/3.2/ref/applications/#django.apps.AppConfig.ready
# https://docs.djangoproject.com/en/3.2/ref/signals/#post-migrate
