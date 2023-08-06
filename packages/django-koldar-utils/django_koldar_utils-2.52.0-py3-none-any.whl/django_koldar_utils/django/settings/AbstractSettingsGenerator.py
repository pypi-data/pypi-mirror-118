import abc
import os
from typing import List

import environ
from django.conf import settings

from django_koldar_utils.django.settings import settings_helper
from datetime import timedelta
from pathlib import Path

from django.core.management.commands.runserver import Command as runserver
from django_koldar_utils.django.Orm import Orm
from django_koldar_utils.django.settings import settings_helper


class AbstractSettingsGenerator(abc.ABC):
    """
    A class that setup automatically settings.py.
    If you need to edit the file for every app, this is the place to update
    """

    def __init__(self):
        self.env: environ.Env = None
        self.settings_module: any = None

    def get_server_port(self) -> int:
        return self.env("SERVER_PORT")

    def get_secret_key(self) -> int:
        return self.env("SECRET_KEY")

    @abc.abstractmethod
    def configure_installed_apps(self, original: List[str]) -> List[str]:
        pass

    @abc.abstractmethod
    def configure_middlewares(self, original: List[str]) -> List[str]:
        pass

    def add_other_settings(self):
        pass

    def generate(self):
        SETTING_DIR, BASE_DIR, PROJECT_DIR, PROJECT_DIRNAME = settings_helper.get_paths(__file__)
        self.env = settings_helper.read_env_file(
            ORM_TABLE_NAMING_CONVENTION="standard"
        )
        self.settings_module = settings
        SECRET_KEY = self.get_secret_key()

        # SECURITY WARNING: don't run with debug turned on in production!
        DEBUG = self.env("DEBUG")

        ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

        if DEBUG:
            # used for static live test server
            ALLOWED_HOSTS.extend(["testserver"])

        CORS_ALLOW_HEADERS = ['*']
        CORS_ORIGIN_ALLOW_ALL = True
        CORS_ALLOW_ALL_ORIGINS = True

        # PORT
        # see https://stackoverflow.com/a/48277389/1887602
        runserver.default_port = self.get_server_port()

        # alter the table convention
        Orm.set_table_naming_convention(self.env("ORM_TABLE_NAMING_CONVENTION"))

        # INSTALLED_APPS
        INSTALLED_APPS = [
            # standard
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ]
        INSTALLED_APPS = self.configure_installed_apps(INSTALLED_APPS)

        # MIDDLEWARE
        MIDDLEWARE = [
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        MIDDLEWARE = self.configure_middlewares(self.middlewares_to_append)

        ROOT_URLCONF = f"{PROJECT_DIRNAME}.urls"  # 'researchers_registry_service_be_project.urls'

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]

        WSGI_APPLICATION = f'${PROJECT_DIRNAME}.wsgi.application'

        # Database
        # https://docs.djangoproject.com/en/3.1/ref/settings/#databases

        DATABASES = {
            'default': {
                'ENGINE': self.env('DATABASE_ENGINE'),
                'NAME': self.env("DATABASE_NAME"),
                'USER': self.env("DATABASE_USERNAME"),
                'PASSWORD': self.env("DATABASE_PASSWORD"),
                'HOST': self.env("DATABASE_HOSTNAME"),
                'PORT': self.env("DATABASE_PORT"),
            }
            # 'default': {
            #     'ENGINE': 'django.db.backends.mysql',
            #     'HOST': "auth.c0zcaytggc0x.eu-south-1.rds.amazonaws.com",
            #     'PORT': 3306,
            #     'NAME': "researchers-registry-service",
            #     'USER': "user-researcher-registry",
            #     'PASSWORD': "n5AYS*f!jVu&vGS*teHSOfBv666IM0hoI",
            # },
        }

        # Password validation
        # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

        AUTHENTICATION_BACKENDS = [
            "researchers_registry_service_be.backend.ResearcherViaAccessTokenAuthenticationBackend",
            "researchers_registry_service_be.backend.ResearcherViaApiTokenAuthenticationBackend"
        ]

        AUTH_USER_MODEL = "django_cbim_general_service.AuthUser"

        # Internationalization
        # https://docs.djangoproject.com/en/3.1/topics/i18n/

        LANGUAGE_CODE = 'en-us'

        TIME_ZONE = 'UTC'

        USE_I18N = True

        USE_L10N = True

        USE_TZ = True

        # Static files (CSS, JavaScript, Images)
        # https://docs.djangoproject.com/en/3.1/howto/static-files/

        STATIC_URL = '/static/'

        # ##############################################################################
        # ADDED
        # ##############################################################################

        # CORS

        # see https://github.com/adamchainz/django-cors-headers
        # CORS_ALLOWED_ORIGINS = []
        # for x in ALLOWED_HOSTS:
        #     CORS_ALLOWED_ORIGINS.append(f"http://{x}")
        #     CORS_ALLOWED_ORIGINS.append(f"https://{x}")
        # CORS_ALLOWED_ORIGINS.append("http://127.0.0.1:3000")
        # CORS_ALLOWED_ORIGINS.append("http://127.0.0.1:8000")
        # CORS_ALLOWED_ORIGINS.append("http://127.0.0.1:8001")

        # logging

        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                },
            },
            'root': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }

        # CACHE system.
        # Used to sav user,roles,permissions

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'default',
            },
            'users': {
                'BACKEND': 'django_cbim_general_service.cache.UserCache',
                'LOCATION': 'users',
                'TIMEOUT': '1h',
            }
        }

        # cbim-general-service

        DJANGO_CBIM_GENERAL_SERVICE = {
            "JWT_API_TOKEN_AUDIENCE": None,
            "JWT_API_TOKEN_ISSUER": None,
            "JWT_API_TOKEN_ALGORITHM": "HS256",
            "JWT_API_TOKEN_SECRET_KEY": self.env("API_TOKEN_SECRET_KEY"),
            "JWT_API_TOKEN_PUBLIC_KEY": None,
            "JWT_API_TOKEN_PRIVATE_KEY": None,
            "JWT_API_TOKEN_EXPIRATION_TIME": timedelta(hours=1),
            # needs to be the same of user-auth-service
            "ACCESS_TOKEN_SECRET_KEY": "sK00uj3O#6VcbK!HlxmHuWS#G9JQZaL@BVcl7Zf@b0JU09",
            "ACCESS_TOKEN_PUBLIC_KEY": None,
            "ACCESS_TOKEN_AUDIENCE": None,
            "ACCESS_TOKEN_ISSUER": None,
            "ACCESS_TOKEN_ALGORITHM": "HS256"
        }

        # django-graphene-authentication

        GRAPHENE_AUTHENTICATION = {
            "JWT_REFRESH_TOKEN_N_BYTES": 20,
            "JWT_REFRESH_TOKEN_MODEL": "from django_graphene_authentication.refresh_token.models.StandaloneRefreshToken"
        }

        # django-app-graphqls

        GRAPHENE = {
            "SCHEMA": "django_app_graphql.graphene.schema.SCHEMA",
            'SCHEMA_OUTPUT': 'graphqls-schema.json',
            'SCHEMA_INDENT': 2,
            'MIDDLEWARE': [
                "researchers_registry_service_be.middleware.GeneralServiceApiTokenGraphQLAuthenticationMiddleware",
                "django_app_graphql.middleware.GraphQLStackTraceInErrorMiddleware",
            ],
        }

        GRAPHENE_DJANGO_EXTRAS = {
            'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.LimitOffsetGraphqlPagination',
            'DEFAULT_PAGE_SIZE': 20,
            'MAX_PAGE_SIZE': 50,
            'CACHE_ACTIVE': True,
            'CACHE_TIMEOUT': 300  # seconds
        }

        DJANGO_APP_GRAPHQL = {
            "BACKEND_TYPE": "graphene",
            "EXPOSE_GRAPHIQL": True,
            "GRAPHQL_SERVER_URL": "",
            "ENABLE_GRAPHQL_FEDERATION": True,
            "SAVE_GRAPHQL_SCHEMA": os.path.join("output", "schema.graphql"),
            "ADD_DUMMY_QUERIES_IF_ABSENT": True,
            "ADD_DUMMY_MUTATIONS_IF_ABSENT": True,
        }

        self.add_other_settings()

        # """
        # Django settings for researchers_registry_service_be_project project.
        #
        # Generated by 'django-admin startproject' using Django 3.1.4.
        #
        # For more information on this file, see
        # https://docs.djangoproject.com/en/3.1/topics/settings/
        #
        # For the full list of settings and their values, see
        # https://docs.djangoproject.com/en/3.1/ref/settings/
        # """
        # import os
        # from datetime import timedelta
        # from pathlib import Path
        #
        # #  Directory to this file
        # from django.core.management.commands.runserver import Command as runserver
        # from django_koldar_utils.django.Orm import Orm
        #
        # SETTING_DIR = Path(__file__).resolve()
        # # Build paths inside the project like this: BASE_DIR / 'subdir'.
        # BASE_DIR = Path(__file__).resolve().parent.parent
        #
        # # ###################################################################################
        # # django-environ setup
        # # ###################################################################################
        # # see https://django-environ.readthedocs.io/en/latest/#settings-py
        # import environ
        # env = environ.Env(
        #     # set casting, default value
        #     DEBUG=(bool, False)
        # )
        # # reading .env file
        # environ.Env.read_env()
        # ####################################################################################
        # # Django settings
        # ####################################################################################
        #
        # # Quick-start development settings - unsuitable for production
        # # See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
        #
        # # SECURITY WARNING: keep the secret key used in production secret!
        # SECRET_KEY = 'o0jv=_qtdg$nd1#8wt22#%c4n$-(v%+%*8x4(e#p*zm6ow10zm'
        #
        # # SECURITY WARNING: don't run with debug turned on in production!
        # DEBUG = True
        #
        # # ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
        # ALLOWED_HOSTS = ["*"]
        #
        # CORS_ALLOW_HEADERS = ['*']
        # CORS_ORIGIN_ALLOW_ALL = True
        # CORS_ALLOW_ALL_ORIGINS = True
        #
        # # PORT
        # # see https://stackoverflow.com/a/48277389/1887602
        # runserver.default_port = 8001
        #
        # # alter the table convention
        # Orm.set_table_naming_convention("standard")
        #
        # # Application definition
        #
        # INSTALLED_APPS = [
        #     # you need to add if you want Authorization header to be included in the request of the wsgi server
        #     'corsheaders',
        #     # standard
        #     'django.contrib.admin',
        #     'django.contrib.auth',
        #     'django.contrib.contenttypes',
        #     'django.contrib.sessions',
        #     'django.contrib.messages',
        #     'django.contrib.staticfiles',
        #     # cbim apps all need this
        #     'django_cbim_commons',
        #     # cbim services using authentication need this
        #     'django_cbim_general_service',
        #     # graphql
        #     'graphene_django',
        #     'django_filters',
        #     'researchers_registry_service_be',
        #     # make sure the django_app_graphql is the last app you add!
        #     'django_app_graphql',
        # ]
        #
        # MIDDLEWARE = [
        #     'corsheaders.middleware.CorsMiddleware',
        #     'django.middleware.common.CommonMiddleware',
        #     'django.middleware.security.SecurityMiddleware',
        #     'django.contrib.sessions.middleware.SessionMiddleware',
        #     'django.middleware.csrf.CsrfViewMiddleware',
        #     'django.contrib.auth.middleware.AuthenticationMiddleware',
        #     'django.contrib.messages.middleware.MessageMiddleware',
        #     #'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # ]
        #
        # ROOT_URLCONF = 'researchers_registry_service_be_project.urls'
        #
        # TEMPLATES = [
        #     {
        #         'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #         'DIRS': [],
        #         'APP_DIRS': True,
        #         'OPTIONS': {
        #             'context_processors': [
        #                 'django.template.context_processors.debug',
        #                 'django.template.context_processors.request',
        #                 'django.contrib.auth.context_processors.auth',
        #                 'django.contrib.messages.context_processors.messages',
        #             ],
        #         },
        #     },
        # ]
        #
        # WSGI_APPLICATION = 'researchers_registry_service_be_project.wsgi.application'
        #
        #
        # # Database
        # # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
        #
        # DATABASES = {
        #     'default': {
        #         'ENGINE': 'django.db.backends.mysql',
        #         'HOST': "auth.c0zcaytggc0x.eu-south-1.rds.amazonaws.com",
        #         'PORT': 3306,
        #         'NAME': "researchers-registry-service",
        #         'USER': "user-researcher-registry",
        #         'PASSWORD': "n5AYS*f!jVu&vGS*teHSOfBv666IM0hoI",
        #     },
        # }
        #
        #
        # # Password validation
        # # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
        #
        # AUTH_PASSWORD_VALIDATORS = [
        #     {
        #         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        #     },
        #     {
        #         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        #     },
        #     {
        #         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        #     },
        #     {
        #         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        #     },
        # ]
        #
        # AUTHENTICATION_BACKENDS = [
        #     "django_cbim_general_service.backend.GeneralServiceAuthenticationBackend",
        # ]
        #
        #
        # # Internationalization
        # # https://docs.djangoproject.com/en/3.1/topics/i18n/
        #
        # LANGUAGE_CODE = 'en-us'
        #
        # TIME_ZONE = 'UTC'
        #
        # USE_I18N = True
        #
        # USE_L10N = True
        #
        # USE_TZ = True
        #
        #
        # # Static files (CSS, JavaScript, Images)
        # # https://docs.djangoproject.com/en/3.1/howto/static-files/
        #
        # STATIC_URL = '/static/'
        #
        # # ##############################################################################
        # # ADDED
        # # ##############################################################################
        #
        # # CORS
        #
        # # see https://github.com/adamchainz/django-cors-headers
        # # CORS_ALLOWED_ORIGINS = []
        # # for x in ALLOWED_HOSTS:
        # #     CORS_ALLOWED_ORIGINS.append(f"http://{x}")
        # #     CORS_ALLOWED_ORIGINS.append(f"https://{x}")
        # # CORS_ALLOWED_ORIGINS.append("http://127.0.0.1:3000")
        # # CORS_ALLOWED_ORIGINS.append("http://127.0.0.1:8000")
        # # CORS_ALLOWED_ORIGINS.append("http://127.0.0.1:8001")
        #
        # # logging
        #
        # LOGGING = {
        #     'version': 1,
        #     'disable_existing_loggers': False,
        #     'handlers': {
        #         'console': {
        #             'class': 'logging.StreamHandler',
        #         },
        #     },
        #     'root': {
        #         'handlers': ['console'],
        #         'level': 'DEBUG',
        #     },
        # }
        #
        # # CACHE system.
        # # Used to sav user,roles,permissions
        #
        # CACHES = {
        #     'default': {
        #         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #         'LOCATION': 'default',
        #     },
        #     'users': {
        #         'BACKEND': 'django_cbim_general_service.cache.UserCache',
        #         'LOCATION': 'users',
        #     }
        # }
        #
        # # django-app-graphqls
        #
        # GRAPHENE = {
        #     "SCHEMA": "django_app_graphql.graphene.schema.SCHEMA",
        #     'SCHEMA_OUTPUT': 'graphqls-schema.json',
        #     'SCHEMA_INDENT': 2,
        #     'MIDDLEWARE': [
        #         "graphql_jwt.middleware.JSONWebTokenMiddleware",
        #         "django_app_graphql.middleware.GraphQLStackTraceInErrorMiddleware",
        #     ],
        # }
        #
        # GRAPHENE_DJANGO_EXTRAS = {
        #     'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.LimitOffsetGraphqlPagination',
        #     'DEFAULT_PAGE_SIZE': 20,
        #     'MAX_PAGE_SIZE': 50,
        #     'CACHE_ACTIVE': True,
        #     'CACHE_TIMEOUT': 300  # seconds
        # }
        #
        # # see https://django-graphql-jwt.domake.io/en/latest/refresh_token.html
        # GRAPHQL_JWT = {
        #     # This configures graphqls-jwt to add "token" input at each request to be authenticated
        #     'JWT_ALLOW_ARGUMENT': True,
        #     'JWT_ARGUMENT_NAME': "token",
        #     'JWT_VERIFY_EXPIRATION': True,
        #     'JWT_EXPIRATION_DELTA': timedelta(days=1),
        #     'JWT_ALGORITHM': "HS256",
        #     'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
        #     'JWT_AUTH_HEADER_PREFIX': "Bearer",
        #     # VERY IMPORTANT TO MAKE PERMISSION FETCHER AUTHENTICATION BACKEND WORK!
        #     'JWT_DECODE_HANDLER': 'django_cbim_general_service.backend.jwt_decoder_handler',
        #     'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'django_cbim_general_service.backend.jwt_payload_get_username',
        #     'JWT_GET_USER_BY_NATURAL_KEY_HANDLER': 'django_cbim_general_service.backend.user_by_natural_key_handler',
        #     "JWT_SECRET_KEY": "#I0MI5Y$y0^y7@nssN#r@F#7lamW1&1cfmT1^cD94aI&x8JucO",
        #     "JWT_PAYLOAD_HANDLER": "django_cbim_general_service.backend.jwt_payload_handler",
        # }
        #
        # ACCESS_TOKEN_SECRET_KEY = "sK00uj3O#6VcbK!HlxmHuWS#G9JQZaL@BVcl7Zf@b0JU09"
        # """
        # Token key used to encode the access token
        # """
        #
        # DJANGO_APP_GRAPHQL = {
        #     "BACKEND_TYPE": "graphene",
        #     "EXPOSE_GRAPHIQL": True,
        #     "GRAPHQL_SERVER_URL": "",
        #     "ENABLE_GRAPHQL_FEDERATION": True,
        #     "SAVE_GRAPHQL_SCHEMA": os.path.join("output", "schema.graphql"),
        #     "ADD_DUMMY_QUERIES_IF_ABSENT": True,
        #     "ADD_DUMMY_MUTATIONS_IF_ABSENT": True,
        # }