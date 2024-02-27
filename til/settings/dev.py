from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-(qeaf_2vlf3zsfmk%o7g-@)g#(0g_gpnd8d^@f@08180@lxczb"


ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"