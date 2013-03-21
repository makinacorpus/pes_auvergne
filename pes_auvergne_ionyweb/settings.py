# -*- coding: utf-8 -*-
# Django settings for the allianceprovence project.
from ionyweb import get_ionyweb_path
from ionyweb.settings import *
import os

ABSOLUTE_PATH = os.getcwd()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     # ('Manager', 'webmaster@localhost'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coop_allianceprovence',                      # Or path to database file if using sqlite3.
        'USER': 'dbuser',                      # Not used with sqlite3.
        'PASSWORD': 'xxxxxxx',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-fr'

SITE_NAME = "allianceprovence"
GRAPPELLI_ADMIN_HEADLINE = SITE_NAME
GRAPPELLI_ADMIN_TITLE = SITE_NAME

SITE_URL = "http://localhost:8000"              # No trailing slash
DOMAIN_NAME = "localhost"

# GOOGLE_ANALYTICS_ACCOUNT_CODE = "UA-XXXXXX-XX"

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'no-reply@%s' % DOMAIN_NAME
SERVER_EMAIL = DEFAULT_FROM_EMAIL


from settings_local import *


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ABSOLUTE_PATH, 'medias/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '%s/_medias/' % SITE_URL

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ABSOLUTE_PATH, 'collected_static/')

STATIC_URL = '/_static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(ABSOLUTE_PATH, 'static'),
    os.path.join(get_ionyweb_path(), 'static'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kt^d69-e(vw58l#(vh)^=qkv#pfne-%hqzw@92pc7mhi!z4@(q'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(ABSOLUTE_PATH, 'templates'),
    os.path.join(get_ionyweb_path(), 'templates'),
)

LAYOUTS_DIRS = (
    os.path.join(ABSOLUTE_PATH, 'layouts'),
    os.path.join(get_ionyweb_path(), 'contrib', 'layouts'),
)

THEMES_DIRS = (
    os.path.join(ABSOLUTE_PATH, 'themes'),
    os.path.join(get_ionyweb_path(), 'contrib', 'themes'),
)


# TEMPLATE_CONTEXT_PROCESSORS += ()

ADMIN_THEME = 'dark' # 'snow', 'dark', ... Will load ionyweb_admin_%%%.less

INSTALLED_APPS += (
    'django.contrib.staticfiles',
    # Apps
    'ionyweb.page_app.page_text',
    'ionyweb.page_app.page_blog',
    'ionyweb.page_app.page_redirect',
    'ionyweb.page_app.page_agenda',
    'ionyweb.page_app.page_book',
    'ionyweb.page_app.page_gallery_images',
    'ionyweb.page_app.page_sitemap',
    
    # Plugins
    'ionyweb.plugin_app.plugin_text',
    'ionyweb.plugin_app.plugin_image',
    'ionyweb.plugin_app.plugin_website_title',
    'ionyweb.plugin_app.plugin_video',
    'ionyweb.plugin_app.plugin_map',
    'ionyweb.plugin_app.plugin_links_list',
    'ionyweb.plugin_app.plugin_blog_entries_list',
    'ionyweb.plugin_app.plugin_contact',
    'ionyweb.plugin_app.plugin_fb_likebox',
    'ionyweb.plugin_app.plugin_breadcrumb',
    'ionyweb.plugin_app.plugin_slideshow',
)

