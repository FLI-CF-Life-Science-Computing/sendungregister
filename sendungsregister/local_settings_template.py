import os

EMAIL_HOST = '127.0.0.1'
SECRET_KEY = '23841234890234'
ALLOWED_HOSTS = ['127.0.0.1', ]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")
ADMIN_EMAIL = ''
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DEBUG = True# SECURITY WARNING: don't run with debug turned on in production!


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}
