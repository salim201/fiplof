# Structure du module Demande

## Description
Le module Demande gère l'ensemble du processus de demande de certificat foncier, de la création à la validation, en passant par la consultation et l'opposition.

## Fichiers principaux

### Gestion des demandes
- `CreaDemande.py` - Interface de création de nouvelle demande
- `CreaDemande.ui` - Formulaire de création de demande
- `DemandeDetails.py` - Gestion détaillée des demandes
- `DemandeDetailsRun.py` - Logique métier de gestion des demandes
- `ConsultationDemande.py` - Interface de consultation des demandes

### Gestion des demandeurs
- `Demandeurs.py` - Gestion des demandeurs
- `DemandeursForm.py` - Formulaire des demandeurs
- `DemandeursFormRun.py` - Logique de gestion des demandeurs
- `DemandeursUpdateFormRun.py` - Mise à jour des informations des demandeurs

### Recherche et consultation
- `FindDemandeRun.py` - Recherche de demandes
- `RechercheDemandeForm.py` - Formulaire de recherche
- `DetailsDemande.py` - Affichage des détails d'une demande
- `DetailsDemandeRunn.py` - Logique d'affichage des détails

### Gestion des oppositions
- `Opposition.py` - Gestion des oppositions
- `OppositionForm.py` - Formulaire d'opposition
- `OppositionFormRun.py` - Logique de gestion des oppositions
- `Oppositions.py` - Liste des oppositions

### Gestion des voisins
- `Voisins.py` - Gestion des voisins de parcelle
- `Voisins.ui` - Interface de gestion des voisins
- `VoisinsRun.py` - Logique de gestion des voisins

### Validation et rejet
- `ConfirmDelete.py` - Confirmation de suppression
- `rejet.py` - Gestion des rejets de demande
- `ReglementForm.py` - Formulaire de règlement
- `ReglementFormRun.py` - Logique de règlement

## Fonctionnalités principales

1. **Création de demandes**
   - Saisie des informations du demandeur
   - Description de la parcelle
   - Pièces jointes

2. **Consultation des demandes**
   - Recherche par critères
   - Affichage détaillé
   - Historique des modifications

3. **Gestion des oppositions**
   - Dépôt d'opposition
   - Suivi des oppositions
   - Validation/rejet

4. **Gestion des voisins**
   - Identification des parcelles adjacentes
   - Notification des voisins
   - Gestion des réponses

5. **Workflow de validation**
   - Validation par étapes
   - Rejet avec motifs
   - Règlement des litiges

## Dépendances
- PyQt4 pour l'interface graphique
- Base de données via les modèles
- Module Configuration pour les paramètres
- Module Certificat pour la liaison

## Flux typique
1. Création d'une demande (`CreaDemande`)
2. Recherche et consultation (`FindDemandeRun`, `ConsultationDemande`)
3. Gestion des oppositions éventuelles (`Opposition`)
4. Validation ou rejet (`ReglementForm`)
