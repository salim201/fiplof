# Structure du module Certificat

## Description
Le module Certificat gère le cycle de vie complet des certificats fonciers, de leur création initiale à leur consultation, en passant par la gestion des propriétaires et des charges.

## Fichiers principaux

### Création et gestion des certificats
- `CreationInitialeRun.py` - Logique de création initiale des certificats
- `creationInitiale.py` - Interface de création initiale
- `ConsultationCF.py` - Interface de consultation des certificats fonciers
- `ConsultationCFRun.py` - Logique de consultation
- `RechercheCF.py` - Recherche de certificats
- `RechercheCFRun.py` - Logique de recherche
- `EditionCF.py` - Édition des certificats
- `EditionCFRun.py` - Logique d'édition

### Gestion des propriétaires
- `PersonnePhysique.py` - Gestion des personnes physiques
- `PersonnePhysiqueRun.py` - Logique de gestion des personnes physiques
- `PersonneMorale.py` - Gestion des personnes morales
- `PersonneMoraleRun.py` - Logique de gestion des personnes morales
- `ProprietairesRun.py` - Gestion des propriétaires
- `ConsultationProprietaire.py` - Consultation des propriétaires
- `ConsultationProprietaireRun.py` - Logique de consultation

### Gestion des charges et servitudes
- `ChargesRun.py` - Gestion des charges
- `AutresCharges.py` - Gestion des autres charges
- `AutresChargesRun.py` - Logique de gestion des autres charges
- `ConsultationCharges.py` - Consultation des charges
- `ConsultationChargesRun.py` - Logique de consultation
- `ServitudePassageRun.py` - Gestion des servitudes de passage
- `ListeDesServitudes.py` - Liste des servitudes

### Gestion des limites et parcelles
- `LimiteParcelleRun.py` - Gestion des limites de parcelles
- `ListeLimitesRun.py` - Liste des limites
- `ConsultationLimites.py` - Consultation des limites
- `ConsultationLimitesRun.py` - Logique de consultation

### Gestion des hypothèques
- `HypothequesRun.py` - Gestion des hypothèques
- `hypothques.py` - Interface des hypothèques
- `hypothquesConsultation.py` - Consultation des hypothèques

### Historique et suivi
- `Historique.py` - Gestion de l'historique
- `HistoriqueRun.py` - Logique de gestion de l'historique

### Transformations groupées
- `TransformationGroupeeDmd.py` - Transformations groupées de demandes
- `TransformationGroupeeDmdRun.py` - Logique de transformation groupée

### Listes et référentiels
- `ListeFokontany.py` - Gestion des fokontany
- `ListePersonneMorale.py` - Liste des personnes morales
- `ListePersonnePqueRun.py` - Liste des personnes physiques
- `ListePointsCardinaux.py` - Gestion des points cardinaux
- `ListeConsistanceRun.py` - Gestion de la consistance

## Fonctionnalités principales

### 1. Création de certificats
- Création initiale à partir d'une demande
- Saisie des informations de la parcelle
- Définition des limites et superficie

### 2. Gestion des propriétaires
- Ajout/modification de propriétaires (personnes physiques/morales)
- Gestion des quotes-parts
- Historique des transferts

### 3. Gestion des charges
- Charges foncières
- Servitudes diverses
- Hypothèques et privilèges

### 4. Consultation et recherche
- Recherche par numéro de certificat
- Recherche par propriétaire
- Consultation détaillée avec historique

### 5. Édition et mise à jour
- Mise à jour des informations
- Édition des certificats
- Transformations groupées

### 6. Géométrie et limites
- Définition des limites parcellaires
- Points cardinaux
- Superficie et consistance

## Dépendances
- PyQt4 pour l'interface graphique
- Base de données PostgreSQL via psycopg2
- Module QGIS pour les fonctionnalités géospatiales
- Module Demande pour la liaison avec les demandes
- Module Configuration pour les paramètres

## Flux typique
1. Création à partir d'une demande validée
2. Saisie des informations de la parcelle et des propriétaires
3. Définition des limites et charges
4. Validation et édition du certificat
5. Consultation et mises à jour ultérieures
