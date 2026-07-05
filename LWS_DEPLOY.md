# Déploiement PIGOE sur LWS cPanel — Sous-domaine

Durée estimée : 20-30 minutes. Accès SSH requis (activable dans cPanel).

---

## Étape 1 — Créer la base de données PostgreSQL

1. Dans votre cPanel LWS, section **Bases de données**, cliquer **pgSQL & PhPgAdmin**
2. Cliquer **"Cliquez ici pour créer une base PgSql"**
3. LWS envoie un email avec les paramètres :
   - Adresse du serveur (HOST)
   - Nom de la base (DB_NAME)
   - Nom d'utilisateur (DB_USER)
   - Mot de passe (DB_PASSWORD)

**Conservez ces informations — vous en aurez besoin à l'Étape 4.**

> Important : pour rester compatible avec votre base PostgreSQL actuelle (10.23), le projet doit utiliser Django 3.2.x. Les versions Django plus récentes requièrent PostgreSQL 12+. Si vous souhaitez monter en version Django, il faudra aussi changer de base de données.

---

## Étape 2 — Créer le sous-domaine

1. cPanel → **Domaines → Sous-domaines**
2. Sous-domaine : `pigoe` (donnera `pigoe.votredomaine.tld`)
3. Racine du document : laisser la valeur suggérée (sera écrasée par Passenger)
4. Cliquer **Créer**

---

## Étape 3 — Créer l'application Python (Setup Python App)

1. cPanel → **Logiciel → Setup Python App**
2. Cliquer **Create Application**
3. Remplir :

| Champ | Valeur |
|---|---|
| Python version | **3.9.23** |
| Application root | `pigoe_app` (dossier hors de public_html) |
| Application URL | Sélectionner `pigoe.votredomaine.tld` |
| Application startup file | `passenger_wsgi.py` |
| Application entry point | `application` |

4. Cliquer **Create**

cPanel crée `~/pigoe_app/` avec un environnement virtuel Python. Notez la commande d'activation affichée — elle ressemble à :
```
source /home/VOTRE_USER/virtualenv/pigoe_app/3.9/bin/activate
```

---

## Étape 4 — Définir les variables d'environnement

Toujours dans Setup Python App, section **Environment Variables**, ajouter :

| Nom | Valeur |
|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings_lws` |
| `DJANGO_SECRET_KEY` | *(valeur forte — générer avec la commande ci-dessous)* |
| `DJANGO_ALLOWED_HOSTS` | `pigoe.votredomaine.tld` |
| `DB_NAME` | *(reçu par email à l'Étape 1)* |
| `DB_USER` | *(reçu par email à l'Étape 1)* |
| `DB_PASSWORD` | *(reçu par email à l'Étape 1)* |
| `DB_HOST` | *(reçu par email à l'Étape 1)* |
| `DB_PORT` | `5432` |

Pour générer la SECRET_KEY :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Cliquer **Save** après chaque ajout.

---

## Étape 5 — Uploader le projet via SSH

Activer SSH dans cPanel si ce n'est pas fait (**Sécurité → Accès SSH**).

```bash
# Depuis votre machine locale, dans le dossier pigoe_project/
scp -r . VOTRE_USER@VOTRE_SERVEUR_LWS:~/pigoe_app/
```

Ou utiliser FileZilla / le gestionnaire de fichiers cPanel pour uploader le contenu de `pigoe_project/` dans `~/pigoe_app/`.

**Structure finale attendue dans ~/pigoe_app/ :**
```
~/pigoe_app/
├── passenger_wsgi.py      ← point d'entrée Passenger
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── settings_lws.py    ← settings de production LWS
│   └── wsgi.py
├── core/
├── members/
├── finance/
├── events/
├── communication/
└── ...
```

---

## Étape 6 — Installer les dépendances via SSH

```bash
# Se connecter au serveur LWS en SSH
ssh VOTRE_USER@VOTRE_SERVEUR_LWS

# Activer l'environnement virtuel Python créé par cPanel
source ~/virtualenv/pigoe_app/3.9/bin/activate

# Aller dans le dossier du projet
cd ~/pigoe_app

# Installer les dépendances avec le Python du virtualenv
python -m pip install -r requirements.txt
```

---

## Étape 7 — Migrer la base de données et initialiser

```bash
# (environnement virtuel toujours activé)
cd ~/pigoe_app

# Variables d'environnement pour cette session SSH
export DJANGO_SETTINGS_MODULE=config.settings_lws
export DJANGO_SECRET_KEY="VOTRE_SECRET_KEY"
export DJANGO_ALLOWED_HOSTS="pigoe.votredomaine.tld"
export DB_NAME="..."        # vos valeurs
export DB_USER="..."
export DB_PASSWORD="..."
export DB_HOST="..."

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --no-input

# Créer le superuser
python manage.py createsuperuser

# Initialiser l'organisation pilote
python manage.py seed_organization
```

---

## Étape 8 — Redémarrer l'application

Dans cPanel → **Setup Python App**, localiser votre application et cliquer **Restart**.

---

## Étape 9 — Vérification

1. Ouvrir `https://pigoe.votredomaine.tld/admin/`
2. Se connecter avec le superuser créé à l'Étape 7
3. Vérifier que l'organisation pilote apparaît dans **Core → Organisations**

---

## Dépannage fréquent

| Symptôme | Solution |
|---|---|
| Page blanche ou "Internal Server Error" | Activer `PassengerFriendlyErrorPages on` dans `~/pigoe_app/.htaccess` pour voir l'erreur |
| "ModuleNotFoundError" | Vérifier que `pip install -r requirements.txt` a bien été exécuté dans le bon virtualenv |
| "DisallowedHost" | Vérifier que `DJANGO_ALLOWED_HOSTS` contient exactement votre sous-domaine |
| Admin sans CSS | Vérifier que `python manage.py collectstatic` a été exécuté |
| Erreur de connexion PostgreSQL | Vérifier les valeurs DB_* dans les variables d'environnement cPanel |

---

## Note sur la coexistence Railway / LWS

Vous pouvez maintenir les deux déploiements en parallèle :
- **Railway** → environnement de développement/test (push GitHub → redéploiement automatique)
- **LWS** → environnement de production stable (mise à jour manuelle via SSH)

Les deux utilisent le même codebase et le même `config/settings.py` de base.
Seul `DJANGO_SETTINGS_MODULE` diffère :
- Railway → `config.settings` (lit `DATABASE_URL`)
- LWS → `config.settings_lws` (lit les variables DB_* individuelles)
