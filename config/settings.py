"""
Django settings for PIGOE — FAREMAK SERVICES.

Configuration alignée sur :
- ADR-0012 : Django comme framework backend
- ADR-0013 (révisé) : LWS cPanel comme plateforme d'hébergement MVP —
  voir config/settings_lws.py et LWS_DEPLOY.md pour la configuration de
  production complète (Railway a été abandonné, cf. décision du 2026-07-05).
- ADR-0002 : Architecture API First obligatoire (Django Rest Framework)
- ADR-0003 : PostgreSQL comme moteur de données principal (production)

En développement local, SQLite est utilisé par défaut pour la simplicité.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: en production, SECRET_KEY doit venir d'une variable
# d'environnement (cPanel Setup Python App), jamais être committée en clair.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-change-in-production",
)

# SECURITY WARNING: DEBUG doit être False en production (settings_lws.py le
# force explicitement, indépendamment de cette variable d'environnement).
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# L'application est servie derrière un proxy TLS-terminating (Apache/Passenger
# sur LWS) — sans ce réglage, Django considère à tort toutes les requêtes
# comme non sécurisées.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    f"https://{h}" for h in ALLOWED_HOSTS if h not in ("localhost", "127.0.0.1")
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Tiers — API First (ADR-0002)
    "rest_framework",
    # Tiers — Authentification sociale OAuth2 (ADR-0004)
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # Apps métier PIGOE — une app par capacité de la Business Architecture
    "core",            # Organization — socle transverse (Chapitre 6.2)
    "members",          # Member, Family — US-01 à US-06 (Chapitre 6.3)
    "finance",           # Contribution — US-07 à US-12 (Chapitre 6.4)
    "events",            # Event, Attendance — US-13 à US-16 (Chapitre 6.5)
    "communication",    # Announcement — US-17 à US-20 (Chapitre 6.6)
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database — ADR-0003 (PostgreSQL). En local : SQLite par défaut.
# En production (LWS), settings_lws.py écrase entièrement DATABASES avec
# la configuration PostgreSQL cPanel — voir ce fichier.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization — marché pilote togolais (ADR-0008)

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Lome"
USE_I18N = True
USE_TZ = True


# Static files

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django.contrib.sites — requis par allauth
SITE_ID = 1

# Backends d'authentification — standard Django + allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# django-allauth — configuration Google OAuth2 (ADR-0004)
# Les credentials Google (CLIENT_ID, SECRET) sont configurés via
# la commande setup_google_oauth ou l'admin Django, jamais en clair ici.
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
    }
}

# Comportement allauth adapté au contexte PIGOE
# (organisation pilote = administrateurs identifiés, pas d'auto-inscription)
ACCOUNT_LOGIN_METHODS = {"email"}                      # connexion par email uniquement
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"   # simplifié pour MVP — à renforcer en Horizon 1
SOCIALACCOUNT_AUTO_SIGNUP = True      # connexion Google crée le compte automatiquement
LOGIN_REDIRECT_URL = "/admin/"        # après login → admin Django (premier client API)
LOGOUT_REDIRECT_URL = "/accounts/login/"


# Django Rest Framework — ADR-0002 (API First)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
}

