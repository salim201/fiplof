# Architecture du projet FIPLOF

## Vue d'ensemble
FIPLOF (Fiscalité - Plan Local d'Occupation Foncière) est une application de gestion foncière développée en Python avec PyQt4 et QGIS, utilisant PostgreSQL comme base de données. L'application gère le cycle de vie complet des certificats fonciers, de la demande initiale aux opérations subséquentes.

## Configuration technique

### Environnement de développement
- **Système d'exploitation** : Windows (x86)
- **Python** : Version 2.7 (via environnement OSGeo4W)
- **QGIS** : Version Wien (2.x)
- **Framework GUI** : PyQt4
- **Base de données** : PostgreSQL avec psycopg2

### Configuration des variables d'environnement
```batch
SET OSGEO4W_ROOT=C:\Program Files (x86)\QGIS Wien\apps\
SET PYTHONHOME=%OSGEO4W_ROOT%Python27
SET PATH=%OSGEO4W_ROOT%Python27\Scripts;C:\Program Files (x86)\QGIS Wien\bin;%OSGEO4W_ROOT%qgis-ltr\bin
SET PYTHONPATH=%OSGEO4W_ROOT%qgis-ltr\python
```

### Dépendances principales
- **PyQt4** : Interface graphique (QtCore, QtGui)
- **QGIS** : Fonctionnalités géospatiales (qgis.core, qgis.gui)
- **psycopg2** : Connecteur PostgreSQL
- **win32crypt** : Cryptographie Windows
- **ctypes** : Appels système Windows

### Configuration de la base de données
- **SGBD** : PostgreSQL
- **Connexion** : Gérée via le module Configuration
- **ORM** : Custom dans le module models
- **Synchronisation** : Support des bases locales et distantes

### Structure des fichiers de configuration
- **Fichiers .ini** : Paramètres de connexion et configurations
- **Fichiers .ui** : Interfaces PyQt4 générées avec Qt Designer
- **Environnement virtuel** : venv/ avec Python 2.7

### Compatibilité QGIS
Le code gère différentes versions QGIS :
- Support QGIS 1.7+ (vérifications `QGis.QGIS_VERSION_INT >= 10700`)
- Support QGIS 1.9+ (vérifications `QGis.QGIS_VERSION_INT >= 10900`)
- Compatibilité ascendante maintenue pour les fonctionnalités critiques

## Architecture modulaire

### Modules principaux

#### 1. **Fiplof** (Cœur métier)
- **Rôle**: Module central de gestion fiscale
- **Responsabilités**: 
  - Gestion des contribuables
  - Calcul des impôts fonciers
  - Suivi des paiements
  - Reporting fiscal

#### 2. **Demande** (Gestion des demandes)
- **Rôle**: Gestion du processus de demande de certificat
- **Responsabilités**:
  - Création et suivi des demandes
  - Gestion des oppositions
  - Workflow de validation
  - Notification des voisins

#### 3. **Certificat** (Gestion des certificats)
- **Rôle**: Gestion du cycle de vie des certificats fonciers
- **Responsabilités**:
  - Création à partir des demandes validées
  - Gestion des propriétaires
  - Gestion des charges et servitudes
  - Consultation et mise à jour

#### 4. **Configuration** (Paramètres système)
- **Rôle**: Gestion de la configuration de l'application
- **Responsabilités**:
  - Connexion base de données
  - Paramètres applicatifs
  - Synchronisation
  - Configuration des modules

#### 5. **models** (Couche d'accès aux données)
- **Rôle**: ORM et gestion des entités métier
- **Responsabilités**:
  - Mapping objet-relationnel
  - Gestion des entités (utilisateurs, territoires, certificats, etc.)
  - Validation des données
  - Gestion des transactions

#### 6. **OperationsSubsequentes** (Opérations post-certificat)
- **Rôle**: Gestion des opérations après émission du certificat
- **Responsabilités**:
  - Transferts de propriété
  - Mutations
  - Actes notariés
  - Suivi juridique

#### 7. **Parametres** (Configuration métier)
- **Rôle**: Gestion des paramètres métier
- **Responsabilités**:
  - Paramètres fiscaux
  - Configuration administrative
  - Taux et barèmes

#### 8. **Utilisateur** (Gestion des accès)
- **Rôle**: Gestion des comptes et autorisations
- **Responsabilités**:
  - Authentification
  - Gestion des rôles
  - Permissions par module
  - Sécurité

## Flux de données et interactions

### Flux principal de demande de certificat
```
Utilisateur → Demande → Validation → Certificat → OperationsSubsequentes
    ↓           ↓          ↓           ↓              ↓
Authentification → Configuration → models → Fiplof → Parametres
```

### Interdépendances des modules

#### Dependencies directes
- **Tous les modules** → **Configuration** (pour les paramètres de connexion)
- **Tous les modules** → **models** (pour l'accès aux données)
- **Tous les modules** → **Utilisateur** (pour l'authentification)
- **Demande** → **Certificat** (transformation demande → certificat)
- **Certificat** → **OperationsSubsequentes** (opérations post-certificat)
- **Fiplof** → **Parametres** (pour les calculs fiscaux)

#### Dependencies indirectes
- **Certificat** → **Fiplof** (calcul des impôts sur les certificats)
- **OperationsSubsequentes** → **Fiplof** (impôts sur les transferts)
- **Demande** → **Parametres** (validation selon les paramètres)

## Architecture technique

### Couches applicatives

#### 1. Couche Présentation (PyQt4)
- Interfaces utilisateur (.ui)
- Contrôleurs (fichiers .py)
- Widgets personnalisés

#### 2. Couche Métier
- Logique métier dans chaque module
- Gestion des workflows
- Validation des règles métier

#### 3. Couche Accès aux Données (models)
- ORM avec PostgreSQL
- Gestion des transactions
- Mapping objet-relationnel

#### 4. Couche Infrastructure
- Configuration (base de données, paramètres)
- Géomatique (QGIS)
- Utilitaires et helpers

### Patterns architecturaux utilisés

#### 1. **Model-View-Controller (MVC)**
- **Models**: Module models
- **Views**: Fichiers .ui et interfaces PyQt4
- **Controllers**: Fichiers .py contenant la logique de contrôle

#### 2. **Repository Pattern**
- Centralisation de l'accès aux données via models
- Abstraction des requêtes SQL
- Gestion des entités métier

#### 3. **Observer Pattern**
- Notification entre modules lors des changements
- Mise à jour automatique des interfaces
- Synchronisation des données

#### 4. **Factory Pattern**
- Création des différents types de formulaires
- Instanciation des objets métier
- Gestion des dépendances

## Communication inter-modules

### Mécanismes de communication

#### 1. **Appels directs**
- Importation et utilisation directe des classes
- Passage d'objets entre modules
- Méthodes publiques d'interface

#### 2. **Événements et signaux (PyQt4)**
- Communication asynchrone
- Mise à jour des interfaces
- Gestion des actions utilisateur

#### 3. **Base de données partagée**
- Persistance des données
- Partage d'état entre modules
- Intégrité référentielle

### Points d'integration critiques

#### 1. **Transformation Demande → Certificat**
- Point de passage obligatoire
- Validation complexe
- Gestion des erreurs

#### 2. **Calculs fiscaux**
- Intégration Fiplof ↔ Parametres
- Mise à jour des taux
- Historique des calculs

#### 3. **Synchronisation des bases**
- Configuration ↔ models
- Gestion des conflits
- Réplication des données

## Sécurité et autorisations

### Modèle de sécurité
- **Authentification**: Module Utilisateur
- **Autorisation**: Rôles et permissions par module
- **Audit**: Journalisation des opérations
- **Contrôle d'accès**: Validation à chaque niveau

### Flux de sécurité
```
Connexion → Authentification → Vérification rôles → Accès module → Journalisation
```

## Performance et scalabilité

### Optimisations
- **Connexions base de données**: Pool de connexions via Configuration
- **Cache**: Mise en cache des configurations et paramètres
- **Lazy loading**: Chargement à la demande des données volumineuses
- **Indexation**: Optimisation des requêtes SQL critiques

### Points de vigilance
- **Géomatique**: Performance des opérations spatiales QGIS
- **Calculs fiscaux**: Optimisation des algorithmes de calcul
- **Interface**: Réactivité des formulaires complexes

## Évolution et maintenance

### Points d'extension
- **Nouveaux types d'actes**: Extension OperationsSubsequentes
- **Nouveaux paramètres**: Extension Parametres
- **Nouveaux rôles**: Extension Utilisateur
- **Nouveaux états**: Extension Configuration

### Stratégie de maintenance
- **Modularité**: Isolation des changements
- **Tests**: Validation des intégrations
- **Documentation**: Mise à jour des interfaces
- **Versionning**: Gestion des évolutions de schéma

## Conclusion

L'architecture FIPLOF est conçue pour être modulaire, extensible et maintenable. La séparation claire des responsabilités entre modules permet une évolution contrôlée et une maintenance facilitée. Les points d'integration sont bien définis et documentés, assurant une cohérence globale du système.
