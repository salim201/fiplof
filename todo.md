# Modifications dans ListeDossierExterneRun.py

## 1. Bouton "Transformer en Demande" connecté
**Fichier :** ListeDossierExterneRun.py:132  
**Action :** `self.ui.pushButtonTransformerDemande.clicked.connect(self.enregistrerDemande)`  
Ajouté dans `initActions()`.

## 2. Méthode `enregistrerDemande()` (ligne 485)
- Parcourt `tableWidget_dossier`
- Récupère les lignes cochées
- Groupe par batch ID (colonne 1) et code parcelle (colonne 2)
- Pour chaque batch : charge le payload JSON via `FiplofIngestionModel.getIngestionsWithPayload()`
- Trouve les demandes correspondant aux codes parcelles cochés
- Appelle `_traiterDemande()` pour chaque parcelle trouvée
- Supprime du tableau les lignes transformées avec succès

## 3. Méthode `_traiterDemande()` (ligne 564)
Pipeline complet de transformation d'une demande JSON en enregistrement :
- **Géométrie** : `geojson_to_wkb_hex()`
- **Parcelle** : `Parcelled.insert_parcelle_d_by_interrop()`
- **Localité** : lookup District / Commune / Fokontany / Hameau
- **Demande** : `Demande.insert()` + `creationNum()`
- **Personnes/ayants droit** : `Personne.insert()` + `AvoirDemande.insert()` + photos (`BlobPersonne.insertPhotos()`)
- **Voisins** : `Limiteparcelle.insert()` avec `Pointscardinaux.findByPosition()`
- **Statut** : `FiplofIngestionModel.updateTraitementStatut(batch_id, "SUCCESS", [code_parcelle], [])`
- Rollback implicite via exception

## 4. Filtre SQL dans `_buildSearchQuery()` (lignes 186-195)
Ajout de deux conditions à la requête SQL :
1. `EXISTS (json_array_elements(r.valid_parcelle::json) AS vp WHERE vp #>> '{}' = code_parcelle)`  
   → N'affiche que les parcelles présentes dans `valid_parcelle`
2. `NOT EXISTS (json_array_elements(r.traitement_parcelle_valide::json) AS val WHERE val #>> '{}' = code_parcelle)`  
   → Exclut les parcelles déjà transformées en demande

Ajout des colonnes `valid_parcelle` et `traitement_parcelle_valide` dans la sous-requête `FROM (SELECT ...)`.

## Problème : SQL JSON ne fonctionne pas
Le filtrage par `json_array_elements` dans la condition SQL ne retournait aucun résultat car les colonnes `valid_parcelle` et `traitement_parcelle_valide` contiennent une chaîne vide au lieu d'un tableau JSON valide.

### Solution
**Fichier :** ListeDossierExterneRun.py:218-228  
Supprimer les conditions SQL JSON, remplacer par filtrage Python :
```python
if row.valid_parcelle and self._is_code_in_json(row.valid_parcelle, code_parcelle):
    if not row.traitement_parcelle_valide or not self._is_code_in_json(row.traitement_parcelle_valide, code_parcelle):
        # ligne affichée
```

## Correction statut dans enregistrerDemande()
**Fichier :** ListeDossierExterneRun.py  
**Problème :** `updateTraitementStatut` appelée pour chaque parcelle, `commit()` après chaque parcelle, statut `SUCCESS` même pour des cas partiels.
**Solution :** accumulation par batch, appel unique, `PARTIAL_SUCCESS` si échecs

# EnvoiMiseAJour

**Fichiers :** `EnvoiMiseAJour.ui`, `EnvoiMiseAJour.py`, `EnvoiMiseAJourRun.py`  
**Controller :** `batchDemandeController.py` → `showEnvoiMiseAJour()`  
**Menu :** `plof.py` → actionEnvoiMiseAJour après Transformation en demande

### Fonctionnalités
- Tableau : code_parcelle, numero, type, statut, date
- Filtre combo : Tous / Non envoyé / Envoyé / Vu
- Bouton ENVOYER : POST `/api/ui/retours/push` avec les IDs sélectionnés
- Si succès : `statut_retour = 'RETURNED'` + `updated_at = NOW()` en DB
- Si erreur API : dialogue erreur, pas de modif DB
- Barre de progression pendant l'envoi
- `API_BASE_URL` depuis `api_config.getApiBaseUrl()` (configurable)

# Suivi

**Fichier :** `SuiviRun.py`  
**Controller :** `batchDemandeController.py` → `showSuivi()`  
**Menu :** `actionSuiviReception_Demande` (main.ui), connecté dans `plof.py`

### 4 onglets (données DB locale)
1. **Dossiers reçus** (`inbound_dossiers`) : source_transfer_id, source_system, statuts
2. **Retours parcellaires** (`retour_externe`) : code_parcelle, numero, type, statut + push API
3. **Processing ARQ** (`inbound_dossiers`) : résumé + retry callback / reprocess via API
4. **Gestion Batch** (`fiplof_raw_ingestion`) : statut, validation, nb_OK/nb_Err

### API (écritures seulement)
- Push retours, retry callback, reprocess → depuis `getApiBaseUrl()` (configurable)

# SecuriteCompte (Gestion de compte)

**Fichiers :** `SecuriteCompte.ui`, `SecuriteCompte.py`, `SecuriteCompteRun.py`  
**Controller :** `securiteCompteController.py` → `showDialog()`  
**Menu :** `actionSecuriteCompte` (main.ui), connecté dans `plof.py`

### Changements
- **Encodage** : `.ui` réparé (double encodage UTF-8, BOM, balises XML invalides), `.py` regénéré
- **Unicode partout** : méthode `_u()` pour décoder les données DB, messages en `u"..."` avec échappements
- **Colonne ID masquée** : `setColumnHidden(0, True)`
- **Colonnes étirées** : `QHeaderView.Stretch` pour remplir la fenêtre
- **Police réduite** : table 9pt, combo statut 7pt, row height 30px
- **Boutons simplifiés** : seul **Enregistrer** reste visible (Statut combo + Actif checkbox)
- **Valider supprimé** : combo permet déjà de choisir VALIDATED
- **CSS fixé** : `alternate-background-color` (était en camelCase)
- **QString** : `unicode(currentText())` pour psycopg2

# Configuration Service FIPLOF

**Fichier :** `ConfigFIPLOFRun.py`  
**Config :** `api_config.py` → lit/écrit `interop.ini` (section `[api]`, clé `base_url`)  
**Utilisé par :** `SuiviRun.py`, `EnvoiMiseAJourRun.py` → `getApiBaseUrl()`  
**Menu :** `actionConfiguuration_Service_FIPLOF` (main.ui, menuConfiguration), connecté dans `plof.py`

### Dialog
- QLineEdit pour l'URL de base de l'API FastAPI
- Enregistrer/Annuler
- Valeur par défaut : `http://localhost:8001`

# Problèmes connus
- `/api/ui/retours/push` retourne 500 si TopoManager (`http://192.168.1.233:8000`) injoignable
- `valid_parcelle`/`traitement_parcelle_valide` peuvent contenir `''` → filtrage Python gère
- Les push retours, retry callback, reprocess passent par FastAPI (pas de DB directe)

# Structure du menu
```
Interopérabilité                     MenuConfiguration
├── Réception Demande                └── Configuration Service FIPLOF
├── Transformation en demande
├── Envoi mise à jour
├── Suivi
└── Configuration
```
