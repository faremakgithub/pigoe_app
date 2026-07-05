# PIGOE v1 — FAREMAK SERVICES

Plateforme de gestion des organisations — MVP solo, Phase 1.

## Traçabilité

Ce projet est l'implémentation directe de :
- **FEB v2.0** — FAREMAK Enterprise Blueprint (25 principes directeurs)
- **Architecture Vision PIGOE v1** — ADR-0011 (périmètre MVP validé Session ARB 001)
- **ADR-0012** — Django comme framework backend
- **ADR-0013 (révisé 2026-07-05)** — LWS cPanel comme plateforme d'hébergement MVP (Railway abandonné avant tout déploiement public, cf. `LWS_DEPLOY.md`)
- **ADR-0014** — PayDunya comme agrégateur Mobile Money (Togo)
- **Business Architecture PIGOE v1** — 20 user stories, validée Session ARB 002

## Structure du projet

Chaque app Django correspond exactement à une capacité du MVP :

| App | Capacité (Business Architecture) | User Stories |
|---|---|---|
| `core` | Socle transverse (Organization) | — |
| `members` | Gestion des Membres | US-01 à US-06 |
| `finance` | Cotisations & Dons | US-07 à US-12 |
| `events` | Événements | US-13 à US-16 |
| `communication` | Communication | US-17 à US-20 |

## Démarrage local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

L'admin Django est accessible sur `/admin/` — il sert de premier client de
l'API pendant les Phases 1-2 (ADR-0012), avant le développement d'un
frontend dédié.

## Déploiement LWS cPanel (ADR-0013 révisé)

Voir [LWS_DEPLOY.md](LWS_DEPLOY.md) pour la procédure complète (sous-domaine,
Setup Python App, variables d'environnement, migrations, Passenger).

## Organisation pilote

**Église des Assemblées de Dieu, Temple de la Grâce de Bassar Kpankissi** (Togo)

Pour initialiser cette organisation dans une nouvelle instance :

```bash
python manage.py seed_organization
```

## État de la Phase 1 (Semaines 1-4)

- [x] Choix et configuration de la stack — ADR-0012, 0013 actés
- [x] Dépôt et structure de projet initialisés
- [x] Modèle de données des 4 capacités implémenté (Chapitre 6, Business Architecture)
- [x] Migrations générées et appliquées — base de données opérationnelle
- [x] Admin Django configuré pour les 5 modèles (recherche, filtres, autocomplete)
- [x] Test de bout en bout validé — y compris détection de doublon (US-03)
- [x] Organisation pilote identifiée et commande d'initialisation prête
- [ ] Authentification utilisateur finale (OAuth Google) — à configurer avant déploiement public
- [ ] Premier déploiement LWS accessible publiquement

## Sécurité — points d'attention avant mise en production

- `SECRET_KEY` actuelle est un placeholder de développement — **à régénérer avant tout déploiement**
- Le mot de passe du superuser de démonstration (`admin`) doit être changé immédiatement
- Conformément à US-12, le chiffrement au repos des données financières (`Contribution`) reste à activer au niveau infrastructure LWS/PostgreSQL avant la Phase 3
