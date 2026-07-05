"""
settings_lws.py — Configuration de production pour LWS cPanel.

Ce fichier étend config/settings.py sans rien dupliquer.
Il est activé en définissant la variable d'environnement dans cPanel :
  DJANGO_SETTINGS_MODULE = config.settings_lws

La base PostgreSQL LWS est configurée via les variables d'environnement
définies dans Setup Python App → Environment Variables de cPanel.
"""

from .settings import *  # noqa: F401, F403 — hérite de toute la config de base

import os

# Production : désactiver le mode debug
DEBUG = False

# Domaine du sous-domaine LWS (ex: pigoe.eglisebasar.org)
allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,faremak.com,www.faremak.com")
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts.split(",") if h.strip()]
ALLOWED_HOSTS += ["localhost", "127.0.0.1", "0.0.0.0", "faremak.com", "www.faremak.com", ".faremak.com"]
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    f"https://{h.lstrip('.')}"
    for h in ALLOWED_HOSTS
    if h not in ("localhost", "127.0.0.1", "0.0.0.0") and h != "*"
]
CSRF_TRUSTED_ORIGINS += ["https://faremak.com", "https://www.faremak.com"]
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))

# Base de données PostgreSQL LWS
# Les valeurs viennent des variables d'environnement définies dans cPanel
# Setup Python App → Environment Variables
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# Fichiers statiques servis par WhiteNoise (déjà configuré dans settings.py)
# Aucune modification nécessaire.
