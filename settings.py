"""
Django settings for django15 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '555@op&4u$2$i%lq%i(*5vh7#97pf*55&lmh25(8-q1%zj%flw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

######  customized variables  #######
#file paths
ROOT_DIR = os.path.join(BASE_DIR, 'django15')
FILE_DIR = os.path.join(ROOT_DIR, 'files')
#THEATRE_XML_PATH = os.path.join(FILE_DIR, 'on_usa_samp_mov_sources_YYYYMMDD.xml')
#MOVIE_XML_PATH = os.path.join(FILE_DIR, 'on_usa_samp_mov_programs_YYYYMMDD.xml')
#SHOWTIME_XML_PATH = os.path.join(FILE_DIR, 'on_usa_samp_mov_schedules_YYYYMMDD.xml')
#THEATRE_XML_GZ = "on_usa_samp_mov_sources_YYYYMMDD.xml.gz"
#MOVIES_XML_GZ = "on_usa_samp_mov_programs_YYYYMMDD.xml.gz"
#SHOWTIME_XML_GZ = "on_usa_samp_mov_schedules_YYYYMMDD.xml.gz"
THEATRE_CSV_PATH = os.path.join(FILE_DIR, 'theatres.csv')
MOVIE_CSV_PATH = os.path.join(FILE_DIR, 'movies.csv')
SHOWTIME_CSV_PATH = os.path.join(FILE_DIR, 'showtimes.csv')

#file pattern
#THEATRE_XML_GZ_PATTERN = "on_usa_samp_mov_sources_(\d{8}).xml.gz"
#MOVIE_XML_GZ_PATTERN = "on_usa_samp_mov_programs_(\d{8}).xml.gz"
#SHOWTIME_XML_GZ_PATTERN = "on_usa_samp_mov_schedules_(\d{8}).xml.gz"

THEATRE_XML_GZ_PATTERN = "on_usa_samp_mov_sources_YYYYMMDD.xml.gz"
MOVIE_XML_GZ_PATTERN = "on_usa_samp_mov_programs_YYYYMMDD.xml.gz"
SHOWTIME_XML_GZ_PATTERN = "on_usa_samp_mov_schedules_YYYYMMDD.xml.gz"

THEATRE_XML_PATTERN = "on_usa_samp_mov_sources_YYYYMMDD.xml"
MOVIE_XML_PATTERN = "on_usa_samp_mov_programs_YYYYMMDD.xml"
SHOWTIME_XML_PATTERN = "on_usa_samp_mov_schedules_YYYYMMDD.xml"

#ftp
TMS = {}
#TMS.FTP_SERVER = 'on.tmstv.com'
#TMS.FTP_USER = 'onsample'
#TMS.FTP_PASSWORD = '441gn906'

FTP_SERVER = {}
FTP_USER = {}
FTP_PASSWORD = {}
FTP_SERVER['tms'] = 'on.tmstv.com'
FTP_USER['tms'] = 'onsample'
FTP_PASSWORD['tms'] = '441gn906'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'whatever',
    'xmlparser',
    'newapp',
    'south',
    'spatial',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django15.urls'

WSGI_APPLICATION = 'django15.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'moochase_movies',
	#'USER': 'power_user',
	#'PASSWORD': '$poweruserpassword',
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'mydb',
    'USER': 'ec2',
    'PASSWORD': 'woshinibaba',
	#'HOST': 'e-1-252.us-west-1.compute.amazonaws.com',
	'HOST': 'mydbpostgres.cmkkqcjq5cji.us-west-1.rds.amazonaws.com',
	'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
