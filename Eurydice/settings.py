from pathlib import Path
import os
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "eurydice.onrender.com",
    os.getenv("RENDER_EXTERNAL_HOSTNAME"),
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "rest_framework",
    "shop",
]

# Conditionally add Cloudinary apps only if CLOUDINARY_URL is set
if os.getenv("CLOUDINARY_URL"):
    INSTALLED_APPS.insert(-1, "cloudinary_storage")
    INSTALLED_APPS.insert(-1, "cloudinary")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Eurydice.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shop.context_processors.categories",
            ],
        },
    },
]

WSGI_APPLICATION = "Eurydice.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files configuration - Cloudinary for production (Render), local for shared hosting
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
USE_CLOUDINARY = bool(CLOUDINARY_URL)

if USE_CLOUDINARY:
    # Use Cloudinary for media storage (production on Render)
    # Parse CLOUDINARY_URL if provided, otherwise use individual env vars
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    api_key = os.getenv("CLOUDINARY_API_KEY", "")
    api_secret = os.getenv("CLOUDINARY_API_SECRET", "")
    
    if CLOUDINARY_URL:
        # CLOUDINARY_URL format: cloudinary://api_key:api_secret@cloud_name
        import re
        match = re.match(r'cloudinary://([^:]+):([^@]+)@([^/]+)', CLOUDINARY_URL)
        if match:
            api_key, api_secret, cloud_name = match.groups()
    
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": cloud_name,
        "API_KEY": api_key,
        "API_SECRET": api_secret,
    }
    
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    MEDIA_URL = "/media/" 
    MEDIA_ROOT = ""  
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
