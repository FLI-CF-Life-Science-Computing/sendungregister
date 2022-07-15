import os

EMAIL_HOST = '127.0.0.1'
SECRET_KEY = 'dfjie583093aesdfR5'
ALLOWED_HOSTS = ['127.0.0.1', ]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_collected")
# The admin gets a mail if a new user logged in 
#ADMIN_EMAIL = '' 
# The admin gets a mail if an error occurred
#TEC_ADMIN_EMAIL = ''

DEBUG = True# SECURITY WARNING: don't run with debug turned on in production!

