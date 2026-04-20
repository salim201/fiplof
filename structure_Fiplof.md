# Structure du module Fiplof

## Description
Le module Fiplof est le cœur de l'application, gérant la fiscalité et le Plan Local d'Occupation Foncière. Il contient les fonctionnalités principales de gestion des contribuables et des informations fiscales.

## Sous-modules

### 1. CalculImpot/
- **Rôle**: Gestion des calculs d'impôts
- **Fichiers principaux**: Scripts de calcul et de traitement des impôts

### 2. Saisie/
- **Rôle**: Interface de saisie des données fiscales
- **Fichiers principaux**: Formulaires et logique de saisie

### 3. Parametres/
- **Rôle**: Configuration des paramètres fiscaux
- **Fichiers principaux**: Gestion des paramètres et configurations

## Fichiers principaux du module

### Fichiers de gestion des contribuables
- `Contribuable.py` - Gestion des informations des contribuables
- `Contribuable.ui` - Interface utilisateur pour la gestion des contribuables
- `ListeContribuables.py` - Liste des contribuables
- `VoirContribuable.py` - Consultation des détails d'un contribuable

### Fichiers de gestion fiscale
- `InformationFiscale.py` - Gestion des informations fiscales
- `MarquagePaiementImpot.py` - Suivi des paiements d'impôts
- `RecalculImpot.py` - Recalcul des impôts
- `ListeAvisImposition.py` - Gestion des avis d'imposition

### Fichiers de reporting
- `Report.py` - Génération de rapports
- `ListeConsorts.py` - Gestion des consorts

### Fichiers d'authentification
- `Authentification.py` - Gestion de l'authentification des utilisateurs

## Dépendances
- PyQt4 pour l'interface graphique
- Base de données PostgreSQL via psycopg2
- Modules QGIS pour les fonctionnalités géospatiales

## Fonctionnalités principales
1. Gestion des contribuables (physiques et moraux)
2. Calcul et gestion des impôts fonciers
3. Suivi des paiements
4. Génération de rapports fiscaux
5. Authentification et gestion des accès
