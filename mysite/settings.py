import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT
STRIPE_API_KEY=''

DEBUG = True

DATABASES = {
    "default": {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'pop',
        'USER': 'super',
        'PASSWORD': '',
        'HOST': 'soncojmk-178.postgres.pythonanywhere-services.com',
        'PORT': '10178',
    }
}

ALLOWED_HOSTS = ['www.wpoppin.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "America/New_York"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media/media/")



# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

LOGIN_URL = "/account/login/"


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static", "dist"),
    os.path.join(PROJECT_ROOT, "static"),
    os.path.join(PROJECT_ROOT, "static", "src"),
    os.path.join(PROJECT_ROOT, "Post", "static"),


]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "jbc9p*d%jjot1=njw$!7mgteq3du^p0t_t8h4v&_owgg6ctb%!"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PACKAGE_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
                "pinax_theme_bootstrap.context_processors.theme",

                "social.apps.django_app.context_processors.backends",
                "social.apps.django_app.context_processors.login_redirect",

                "django.core.context_processors.request",
            ],
        },
    },
]


''' django el_pagination
from django.conf.global_settings import TEMPLATES

TEMPLATES[0]['OPTIONS']['context_processors'].insert(0, 'django.core.context_processors.request')
'''


ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    #"account.middleware.MethodOverrideMiddleware",
]

ROOT_URLCONF = "mysite.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "mysite.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.gis",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
#    "django.contrib.postgres",
    "pinax.likes",
    #"mailer",

    "Post",
    "blog",

    "taggit",
    "taggit_templatetags2",
    "taggit_labels",
    "pinax.messages",
    "stdimage",
    #"datetimewidget",
    "djgeojson",
    #"stream_django",
    #"activity_stream",

    "fcm_django",
    "restapi",
    "ticketing",

    "el_pagination",
    "rest_framework",
    "rest_framework.authtoken",

    "rest_auth",
    "djoser",
    "push_notifications", #this should be refactored soon

    "drf_extra_fields",
    "notifications",



    #for search sbar
    "haystack",

    # theme

    "bootstrapform",
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",
    # external
    "account",
    "pinax.eventlog",
    "pinax.webanalytics",

    "social.apps.django_app.default",
    "oauth2_provider",
    "rest_framework_social_oauth2",

    # project
    "mysite",
]

SITE_ID = 1


PUSH_NOTIFICATIONS_SETTINGS = {
        "FCM_API_KEY": ":",
        #"APNS_CERTIFICATE": "/path/to/your/certificate.pem",
        "FCM_POST_URL": 'https://fcm.googleapis.com/fcm/send',
}


FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY": "",
        "ONE_DEVICE_PER_USER": True, # true if you want to have only one active device per registered user at a time
        "DELETE_INACTIVE_DEVICES": False, # devices to which notifications cannot be sent, are deleted upon receiving error response from FCM
}


'''
EMAIL_BACKEND = "mailer.backend.DbBackend"
MAILER_EMAIL_BACKEND = "sgbackend.
ridBackend"

SEND_CONFIRMATION_EMAIL = True;


'''
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_USER = ""
SENDGRID_PASSWORD = ""
DEFAULT_FROM_EMAIL = 'WhatsPoppin <noreply@wpoppin.com>'
THEME_CONTACT_EMAIL = "kitongajoseph@gmail.com"


PINAX_LIKES_LIKABLE_MODELS = {
    "Post.Post": {},
    "Post.Question": {},
    "Post.Concert": {}, # can override default config settings for each model here
}

#search bar
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://www.wpoppin.com/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}

#restapi
REST_FRAMEWORK = {
    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),


    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    '''


    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),


    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    '''

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},

    #'AUTHORIZATION_CODE_EXPIRE_SECONDS' : 315400000000,
    'ACCESS_TOKEN_EXPIRE_SECONDS': 315400000,
}


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    'Post.utils.associate_by_email',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)





# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]



ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL = "post_list"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True


AUTHENTICATION_BACKENDS = [
    "social.backends.twitter.TwitterOAuth",
    "social.backends.facebook.FacebookOAuth2",
    "pinax.likes.auth_backends.CanLikeBackend",
    "account.auth_backends.UsernameAuthenticationBackend",
    "account.auth_backends.EmailAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",

    "rest_framework_social_oauth2.backends.DjangoOAuth2",

    'social.backends.facebook.FacebookAppOAuth2',


]

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email,picture',
}


SOCIAL_AUTH_TWITTER_KEY = ""
SOCIAL_AUTH_TWITTER_SECRET = ""

SOCIAL_AUTH_FACEBOOK_KEY = ""
SOCIAL_AUTH_FACEBOOK_SECRET = ""

STREAM_API_KEY = ''
STREAM_API_SECRET = ''



