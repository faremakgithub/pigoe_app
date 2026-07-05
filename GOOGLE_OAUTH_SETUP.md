# Configuration Google OAuth2 — PIGOE v1

Guide pas-à-pas pour activer la connexion Google sur l'application.
Durée estimée : 10 minutes.

## Partie 1 — Google Cloud Console (à faire une seule fois)

### Étape 1 — Créer un projet Google Cloud

1. Aller sur [console.cloud.google.com](https://console.cloud.google.com)
2. Cliquer **Nouveau projet**
3. Nommer le projet : `PIGOE-Production`
4. Cliquer **Créer**

### Étape 2 — Configurer l'écran de consentement OAuth

1. Dans le menu, aller **APIs & Services → Écran de consentement OAuth**
2. Choisir **Externe** (pour les utilisateurs avec un compte Google standard)
3. Remplir les champs obligatoires :
   - Nom de l'application : `PIGOE — Gestion de l'église`
   - Email d'assistance : votre adresse
   - Email de contact : votre adresse
4. Cliquer **Enregistrer et continuer**
5. Dans la section **Portées** : ajouter `email` et `profile`
6. Dans la section **Utilisateurs test** : ajouter votre adresse email (mode test)
7. Terminer l'assistant

### Étape 3 — Créer les identifiants OAuth

1. Aller **APIs & Services → Identifiants**
2. Cliquer **Créer des identifiants → ID client OAuth 2.0**
3. Type d'application : **Application Web**
4. Nom : `PIGOE Web Client`
5. **Origines JavaScript autorisées** :
   ```
   https://<votre-app>.up.railway.app
   http://localhost:8000
   ```
6. **URI de redirection autorisés** :
   ```
   https://<votre-app>.up.railway.app/accounts/google/login/callback/
   http://localhost:8000/accounts/google/login/callback/
   ```
7. Cliquer **Créer**
8. Copier le **Client ID** et le **Client Secret** qui s'affichent

## Partie 2 — Variables d'environnement Railway

Dans votre projet Railway → service app → **Variables**, ajouter :

| Variable | Valeur |
|---|---|
| `GOOGLE_CLIENT_ID` | Le Client ID copié à l'étape 3 |
| `GOOGLE_CLIENT_SECRET` | Le Client Secret copié à l'étape 3 |

## Partie 3 — Activer dans Django (via Railway CLI ou shell)

Une fois les variables définies sur Railway, exécuter :

```bash
railway run python manage.py setup_google_oauth --domain <votre-app>.up.railway.app
```

Cette commande :
1. Configure le Site Django avec votre domaine Railway
2. Crée le SocialApp Google avec vos credentials
3. Affiche l'URL de callback pour vérification

## Partie 4 — Test

1. Ouvrir `https://<votre-app>.up.railway.app/accounts/login/`
2. Cliquer **Se connecter avec Google**
3. Sélectionner votre compte Google (celui ajouté en utilisateurs test)
4. Vous devez être redirigé vers `/admin/`

## Passage en production

Une fois les tests validés, dans Google Cloud Console :
1. Aller **APIs & Services → Écran de consentement OAuth**
2. Cliquer **Publier l'application** (passe du mode test au mode production)
3. Tout utilisateur avec un compte Google peut alors se connecter

## Note de sécurité

Seuls les utilisateurs ayant un compte créé dans `/admin/auth/user/` pourront
accéder aux données de PIGOE, même s'ils se connectent avec Google.
Le flag `is_staff` doit être activé manuellement par l'administrateur.
Cela garantit que la connexion Google ne donne pas automatiquement accès
à l'administration — conforme au principe Security by Design (P18 du FEB).
