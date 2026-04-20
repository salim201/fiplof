# Structure du module models

## Description
Le module models contient l'ensemble des classes de modèles de données utilisées par l'application pour interagir avec la base de données. Il implémente le pattern ORM pour la gestion des entités métier.

## Fichiers principaux

### Modèles de base
- `BaseModel.py` - Classe de base pour tous les modèles
- `CompareDbModel.py` - Modèle de comparaison de bases de données

### Modèles de gestion des accès
- `Acces.py` - Gestion des accès
- `Groupe.py` - Gestion des groupes d'utilisateurs
- `GroupeAcces.py` - Gestion des accès par groupe
- `RoleCrl.py` - Gestion des rôles CRL
- `Utilisateur.py` - Gestion des utilisateurs

### Modèles territoriaux
- `Region.py` - Gestion des régions
- `District.py` - Gestion des districts
- `Commune.py` - Gestion des communes
- `Fokontany.py` - Gestion des fokontany

### Modèles métier principaux
- `Certificat.py` - Gestion des certificats fonciers
- `Demande.py` - Gestion des demandes de certificat
- `Inventaire.py` - Gestion des inventaires
- `ProprietaireParcelled.py` - Gestion des propriétaires de parcelles

### Modèles de géométrie
- `Limiteparcelle.py` - Gestion des limites de parcelles
- `Parcelled.py` - Gestion des parcelles

### Modèles de synchronisation
- `DateSynchro.py` - Gestion des dates de synchronisation
- `ConnectRemoteModel.py` - Modèle de connexion distante

### Modèles spécifiques
- `ProjetCouche.py` - Gestion des projets de couches
- `Journal.py` - Gestion du journal des opérations
- `demande_crl.py` - Gestion des demandes CRL

## Fonctionnalités principales

### 1. Abstraction de la base de données
- Mapping objet-relationnel
- Gestion des connexions
- Validation des données

### 2. Gestion des entités métier
- CRUD (Create, Read, Update, Delete)
- Relations entre entités
- Contraintes d'intégrité

### 3. Gestion des accès et sécurité
- Authentification
- Autorisation par rôles
- Gestion des permissions

### 4. Gestion territoriale
- Hiérarchie administrative
- Géolocalisation
- Relations spatiales

### 5. Synchronisation
- Suivi des modifications
- Réplication des données
- Gestion des conflits

## Architecture des modèles

### Hiérarchie d'héritage
```
BaseModel
├── Acces
├── Groupe
├── Utilisateur
├── Region
├── District
├── Commune
├── Fokontany
├── Certificat
├── Demande
├── Inventaire
└── ...
```

### Relations principales
- **Utilisateur** ↔ **Groupe** (plusieurs à plusieurs via GroupeAcces)
- **Region** → **District** → **Commune** → **Fokontany** (hiérarchie)
- **Demande** → **Certificat** (transformation)
- **Certificat** ↔ **ProprietaireParcelled** (plusieurs à plusieurs)
- **Parcelled** ↔ **Limiteparcelle** (composition)

## Dépendances
- psycopg2 pour la connexion PostgreSQL
- Python standard library pour les fonctionnalités de base
- Configuration module pour les paramètres de connexion

## Patterns utilisés

### 1. Active Record
- Chaque modèle connaît ses méthodes de persistance
- Méthodes save(), delete(), find(), etc.

### 2. Data Mapper
- Séparation entre la logique métier et la persistance
- Gestion des requêtes SQL complexes

### 3. Unit of Work
- Gestion des transactions
- Suivi des modifications

## Conventions de nommage
- Noms de classes en CamelCase
- Noms de fichiers en snake_case correspondant aux classes
- Tables en minuscules avec underscores
- Clés primaires : `id_` + nom de la table
