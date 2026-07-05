# Guide de Déploiement Railway — PIGOE v1

Conforme à ADR-0013. Durée estimée : 10-15 minutes.

## Pré-requis

- Un compte Railway (gratuit pour démarrer) : https://railway.app
- Ce projet poussé sur un dépôt GitHub (privé ou public)

## Étape 1 — Pousser le code sur GitHub

```bash
cd pigoe_project
git init
git add .
git commit -m "PIGOE v1 — Phase 1 : modèle de données des 4 capacités"
git branch -M main
git remote add origin https://github.com/<votre-compte>/pigoe.git
git push -u origin main
```

Le `.gitignore` déjà présent exclut `db.sqlite3`, `staticfiles/` et tout `.env` — aucune donnée locale ou secret ne sera poussé.

## Étape 2 — Créer le projet Railway

1. Sur [railway.app](https://railway.app), cliquer **New Project**
2. Choisir **Deploy from GitHub repo**
3. Sélectionner le dépôt `pigoe` (autoriser Railway à accéder à GitHub si demandé)
4. Railway détecte automatiquement `manage.py` et reconnaît un projet Django

## Étape 3 — Ajouter la base de données PostgreSQL

1. Dans le canvas du projet Railway, cliquer **+ New**
2. Choisir **Database** → **Add PostgreSQL**
3. Railway provisionne la base et génère automatiquement la variable `DATABASE_URL`

C'est cette variable que `settings.py` lit déjà via `dj-database-url` — aucune configuration manuelle de connexion requise.

## Étape 4 — Configurer les variables d'environnement

Sur le service de l'application (pas la base de données), aller dans **Variables** et ajouter :

| Variable | Valeur | Notes |
|---|---|---|
| `DJANGO_SECRET_KEY` | une chaîne aléatoire de 50+ caractères | Générer avec la commande ci-dessous — **ne jamais réutiliser celle de développement** |
| `DJANGO_DEBUG` | `False` | Obligatoire en production |
| `DJANGO_ALLOWED_HOSTS` | `<votre-app>.up.railway.app` | Visible dans l'onglet Settings une fois le premier déploiement lancé |

Pour générer une `DJANGO_SECRET_KEY` forte :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Étape 5 — Premier déploiement

Railway déploie automatiquement après la configuration des variables. Le `Procfile` exécute dans l'ordre :
1. `release` — migrations de base de données + collecte des fichiers statiques
2. `web` — démarrage du serveur Gunicorn

Suivre les logs en temps réel dans l'onglet **Deployments** du service.

## Étape 6 — Créer le superuser et initialiser l'organisation pilote

Une fois le déploiement réussi, ouvrir un shell Railway sur le service :

```bash
railway run python manage.py createsuperuser
railway run python manage.py seed_organization
```

La seconde commande crée automatiquement l'organisation pilote — **Église des Assemblées de Dieu, Temple de la Grâce de Bassar Kpankissi** — conformément à ADR-0011.

## Étape 7 — Vérification

1. Ouvrir l'URL générée par Railway (`<votre-app>.up.railway.app/admin/`)
2. Se connecter avec le superuser créé à l'Étape 6
3. Vérifier que l'organisation pilote apparaît dans **Core → Organisations**
4. Créer un membre de test pour valider la chaîne complète (US-01)

## Critère de succès de la Phase 1

Conformément à l'Architecture Vision (Chapitre 6, Phase 1) : *"Une instance vide mais déployée et accessible publiquement."* Une fois l'Étape 7 validée, ce jalon est atteint.

## Dépannage rapide

| Symptôme | Cause probable | Solution |
|---|---|---|
| `DisallowedHost` | `DJANGO_ALLOWED_HOSTS` n'inclut pas le domaine Railway | Copier le domaine exact depuis Settings → Networking |
| Fichiers statiques absents (admin sans style) | `collectstatic` non exécuté | Vérifier le `Procfile`, relancer un déploiement |
| Erreur de connexion base de données | Service PostgreSQL non lié | Vérifier que `DATABASE_URL` apparaît bien dans les Variables du service app |
| `CSRF verification failed` à la connexion admin | `CSRF_TRUSTED_ORIGINS` non aligné | Vérifier que `DJANGO_ALLOWED_HOSTS` contient le bon domaine (la config le déduit automatiquement) |

## Prochaine étape de gouvernance

Conformément à la Charte ARB, ce premier déploiement public devrait être signalé en **Session ARB 003** comme jalon de clôture de la Phase 1 (Architecture Vision, Chapitre 6).
