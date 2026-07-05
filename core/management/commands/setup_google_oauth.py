import os

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    """
    Configure Google OAuth2 pour PIGOE v1.

    Lit GOOGLE_CLIENT_ID et GOOGLE_CLIENT_SECRET depuis les variables
    d'environnement (définies dans Railway) et crée ou met à jour le
    SocialApp allauth correspondant.

    Conforme à ADR-0004 (OAuth2 / OIDC) — les credentials ne sont jamais
    stockés en clair dans le code ou commités dans Git.

    Usage (local ou railway run) :
        GOOGLE_CLIENT_ID=xxx GOOGLE_CLIENT_SECRET=yyy \\
            python manage.py setup_google_oauth --domain pigoe.up.railway.app
    """

    help = "Configure Google OAuth2 via les variables d'environnement"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            default="localhost:8000",
            help="Domaine Railway ou local (ex: pigoe.up.railway.app)",
        )

    def handle(self, *args, **options):
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise CommandError(
                "Variables d'environnement manquantes : "
                "GOOGLE_CLIENT_ID et GOOGLE_CLIENT_SECRET sont requises."
            )

        domain = options["domain"]

        # 1. Mettre à jour le Site (requis par allauth)
        site, _ = Site.objects.get_or_create(id=1)
        site.domain = domain
        # django.contrib.sites.models.Site.name est limité à 50 caractères
        site.name = "PIGOE — Temple de la Grâce (Bassar)"
        site.save()
        self.stdout.write(f"Site configuré : {site.domain}")

        # 2. Créer ou mettre à jour le SocialApp Google
        app, created = SocialApp.objects.get_or_create(provider="google")
        app.name = "Google"
        app.client_id = client_id
        app.secret = client_secret
        app.save()
        app.sites.add(site)

        action = "créé" if created else "mis à jour"
        self.stdout.write(
            self.style.SUCCESS(
                f"Google OAuth2 {action} pour le domaine {domain}.\n"
                f"URL de callback à enregistrer dans Google Cloud Console :\n"
                f"  https://{domain}/accounts/google/login/callback/"
            )
        )
