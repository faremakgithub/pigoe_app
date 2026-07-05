"""
passenger_wsgi.py — Point d'entrée WSGI pour Phusion Passenger (LWS cPanel).

Ce fichier remplace Gunicorn (utilisé sur Railway) par l'interface
Passenger requise par l'hébergement mutualisé LWS.

Adapté à la structure PIGOE :
  ~/pigoe_app/           ← Application root (cPanel)
  ~/pigoe_app/passenger_wsgi.py   ← ce fichier
  ~/pigoe_app/manage.py
  ~/pigoe_app/config/settings.py
  ~/pigoe_app/members/, finance/, events/, communication/, core/
"""

import os
import sys

# Ajouter le répertoire du projet au PYTHONPATH
# Passenger peut démarrer depuis un autre répertoire que l'application root.
# Il faut donc utiliser le chemin du fichier lui-même.
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Pointer vers les settings LWS par défaut pour ce point d'entrée
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_lws")

try:
    from django.core.wsgi import get_wsgi_application
except Exception as exc:
    raise RuntimeError(f"Impossible d'importer Django WSGI: {exc}") from exc

# Passenger exige que la variable s'appelle exactement "application"
application = get_wsgi_application()


class PassengerPathInfoFix:
    """
    Corrige le PATH_INFO fourni par Passenger, qui omet parfois le préfixe
    du sous-domaine. Nécessaire sur certaines configurations LWS.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        from urllib.parse import unquote

        request_uri = unquote(environ.get("REQUEST_URI", ""))
        script_name = unquote(environ.get("SCRIPT_NAME", ""))
        offset = (
            len(script_name)
            if request_uri.startswith(script_name)
            else 0
        )
        environ["PATH_INFO"] = request_uri[offset:].split("?", 1)[0]
        return self.app(environ, start_response)


application = PassengerPathInfoFix(application)
