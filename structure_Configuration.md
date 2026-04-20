# Structure du module Configuration

## Description
Le module Configuration gère l'ensemble des paramètres de configuration de l'application, incluant la connexion à la base de données, les paramètres applicatifs et la synchronisation.

## Fichiers principaux

### Configuration de la base de données
- `DbConfig.py` - Configuration de la base de données
- `DbConnect.py` - Interface de connexion à la base de données
- `DbConnect.ui` - Formulaire de connexion
- `DbSyncroChange.py` - Gestion de la synchronisation de la base
- `DbSyncroChangeRun.py` - Logique de synchronisation
- `DbSyncroChange.ui` - Interface de synchronisation
- `DbChangeRun.py` - Gestion des changements de base

### Configuration applicative
- `Configurations.py` - Gestion des configurations générales
- `Configurations.ui` - Interface de configuration
- `ConfigurationsRun.py` - Logique de configuration
- `AppConfig.py` - Configuration de l'application

### Configuration des paramètres
- `Params.py` - Gestion des paramètres
- `Params.ui` - Interface des paramètres
- `ParamsRun.py` - Logique de gestion des paramètres
- `ParamsConfig.py` - Configuration des paramètres

### Configuration d'interconnexion
- `IntercoConfig.py` - Configuration des interconnexions

## Fichiers de configuration

### Fichiers .ini
- `admin_tables_spec_insert.ini` - Spécifications d'insertion des tables admin
- `gf_tables_spec.ini` - Spécifications des tables GF
- `gf_tables_spec_insert.ini` - Spécifications d'insertion des tables GF
- `gf_tables_spec_territoire.ini` - Spécifications des tables territoire
- `params.ini` - Paramètres généraux
- `remote.ini` - Configuration remote
- `topo_tables_spec.ini` - Spécifications des tables topographiques

### Fichiers de liste
- `liste_territoire.txt` - Liste des territoires

## Fonctionnalités principales

### 1. Gestion des connexions base de données
- Configuration des paramètres de connexion
- Test de connexion
- Gestion des connexions multiples
- Synchronisation des bases

### 2. Configuration applicative
- Paramètres généraux de l'application
- Configuration des modules
- Gestion des préférences utilisateur

### 3. Gestion des paramètres métier
- Paramètres fiscaux
- Configuration des certificats
- Paramètres territoriaux

### 4. Synchronisation
- Synchronisation entre bases locales et distantes
- Gestion des conflits
- Suivi des synchronisations

## Dépendances
- PyQt4 pour l'interface graphique
- psycopg2 pour la connexion PostgreSQL
- Modules système pour la gestion des fichiers de configuration

## Architecture de configuration

### Structure hiérarchique
1. **Niveau Application**: Configuration globale de l'application
2. **Niveau Base de données**: Paramètres de connexion et synchronisation
3. **Niveau Module**: Configuration spécifique à chaque module
4. **Niveau Utilisateur**: Préférences personnelles

### Fichiers de configuration par type
- **.ini**: Paramètres structurés (base de données, modules)
- **.txt**: Listes et référentiels
- **Python**: Classes de gestion de configuration

## Flux de configuration
1. Chargement des paramètres par défaut
2. Lecture des fichiers de configuration
3. Application des paramètres utilisateur
4. Validation des configurations
5. Sauvegarde des modifications
