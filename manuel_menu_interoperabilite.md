# Manuel d'utilisation — Menu Interopérabilité

## 1. Accès au menu

Le menu **Interopérabilité** se trouve dans la barre de menus principale de l'application FIPLOF.

![Menu Interopérabilité]()

---

## 2. Structure du menu

```
Interopérabilité
├── Transformation en demande
├── Envoi mise à jour
├── Suivi
├── ─────────────
├── Gestion Compte Interopérabilité          (masqué par défaut)
└── Configuration Service FIPLOF
```

---

## 3. Description des actions

### 3.1 Transformation en demande

**Raccourci :** Menu > Interopérabilité > Transformation en demande

**Fonction :** Convertir des dossiers reçus d'un système externe en demandes locales dans FIPLOF.

**Utilisation :**
1. Cliquer sur **Transformation en demande**.
2. La fenêtre **Liste des dossiers externes** s'ouvre, affichant les dossiers issus de la table `fiplof_raw_ingestion` (statut DONE ou PARTIAL_SUCCESS non encore traités).
3. Filtrer la liste par :
   - Fokontany / Hameau
   - Numéro de parcelle
   - Numéro de décision
   - Dates (demande, décision, affichage, reconnaissance locale)
4. Cocher les lignes à transformer.
5. Cliquer sur **Transformer en demande**.
6. Le système crée automatiquement :
   - Une parcelle (avec sa géométrie)
   - Une demande avec un numéro généré
   - Les personnes (demandeurs) avec leurs photos
   - Les relations `AvoirDemande`
   - Les voisins (`Limiteparcelle` + `PointsCardinaux`)
   - Les membres CRL avec leurs rôles
7. Le statut de traitement dans `fiplof_raw_ingestion` passe à `SUCCESS` ou `PARTIAL_SUCCESS`.

---

### 3.2 Envoi mise à jour

**Raccourci :** Menu > Interopérabilité > Envoi mise à jour

**Fonction :** Envoyer les retours parcellaires (statuts) vers le serveur FIPLOF central.

**Utilisation :**
1. Cliquer sur **Envoi mise à jour**.
2. La fenêtre **Envoi mise à jour** s'ouvre, listant les enregistrements de la table `retour_externe`.
3. Filtrer par statut : Tous, En attente, Retourné, Consulté.
4. Le tableau affiche : Code parcelle, Numéro, Type (Fangatahana / Karatany), Statut, Date statut.
5. Cocher les retours à envoyer.
6. Cliquer sur **Envoyer**.
7. Le système POST les IDs sélectionnés vers l'API : `{base_url}/api/ui/retours/push`.
8. En cas de succès, le statut passe à `RETURNED`.
9. En cas d'échec, une boîte de dialogue propose de réessayer.

---

### 3.3 Suivi

**Raccourci :** Menu > Interopérabilité > Suivi

**Fonction :** Tableau de bord de monitoring des échanges avec le serveur FIPLOF.

**Fenêtre :** 3 onglets

#### 3.3.1 Dossiers reçus

Liste des dossiers entrants (`inbound_dossiers`) avec :
| Colonne | Description |
|---|---|
| Réf. transfert | Identifiant du transfert source |
| Source | Système source |
| Réception | Badge "Reçu" |
| Traitement | Badge coloré : En file (orange), Traité (vert), Rejeté (rouge) |
| Callback | Badge + détail d'erreur éventuel |
| Mise à jour | Date de dernière modification |

#### 3.3.2 Processing ARQ

Mêmes données que l'onglet Réceptions, mais avec :
- **Cartes résumé** en haut : En file / Traités / Rejetés / Total
- **Boutons d'action par ligne :**
  - `↻ CB` — Relancer le callback (visible si le callback a échoué)
  - `↻ Re` — Reprocesser (visible si le statut est "Rejeté")

Ces actions appellent les endpoints API :
- `POST {base_url}/api/ui/processing/{id}/retry-callback`
- `POST {base_url}/api/ui/processing/{id}/reprocess`

#### 3.3.3 Gestion Batch

Liste des batchs (`fiplof_raw_ingestion`) avec statut DONE ou PARTIAL_SUCCESS non encore complètement traités.

| Colonne | Description |
|---|---|
| ID | Identifiant du batch |
| Source | Système source |
| Commune | Commune concernée |
| Validation | Badge : Reçu / En cours / Validé / Partiel / Erreur |
| Traitement | Badge : Succès / Partiel / En attente |
| Parcelles | Compteurs OK / Err |
| Reçu le | Date de réception |

---

### 3.4 Gestion Compte Interopérabilité

**Visibilité :** Masqué par défaut.

**Fonction :** Gérer les comptes utilisateurs autorisés à utiliser l'interopérabilité.

**Utilisation (si activé) :**
1. La fenêtre **Sécurité Compte** s'ouvre.
2. Liste des comptes avec : ID, Login, Nom, Système, Actif (Oui/Non), Statut, Dernière connexion.
3. Rechercher un compte par login.
4. Sélectionner un compte pour voir ses détails.
5. Actions possibles :
   - **Enregistrer** — Sauvegarder les modifications
   - **Activer / Désactiver** — Activer ou désactiver le compte
   - **Valider Statut** — Passer le statut à VALIDATED et activer
   - **Rejeter Statut** — Passer le statut à REJECTED
   - **Réinitialiser** — Effacer le formulaire

---

### 3.5 Configuration Service FIPLOF

**Raccourci :** Menu > Interopérabilité > Configuration Service FIPLOF

**Fonction :** Définir l'URL de base du serveur FIPLOF pour les appels API.

**Utilisation :**
1. Cliquer sur **Configuration Service FIPLOF**.
2. Saisir l'URL du serveur (ex. `http://localhost:8001`).
3. Cliquer sur **Enregistrer** pour sauvegarder dans le fichier `interop.ini`.
4. Cliquer sur **Annuler** pour fermer sans modification.

---

## 4. Configuration technique

### Fichier de configuration

**Chemin :** `Interroperabilite/interop.ini`

```ini
[api]
base_url = http://localhost:8001
```

Ce fichier est lu et écrit par le module `api_config.py`.

### API exposée

| Endpoint | Méthode | Appelé par |
|---|---|---|
| `/api/ui/retours/push` | POST | Envoi mise à jour |
| `/api/ui/processing/{id}/retry-callback` | POST | Suivi > Processing ARQ |
| `/api/ui/processing/{id}/reprocess` | POST | Suivi > Processing ARQ |

---

## 5. Tables de la base de données

| Table | Rôle |
|---|---|
| `fiplof_raw_ingestion` | Stocke les données brutes des batchs reçus |
| `inbound_dossiers` | Suivi des transferts de dossiers entrants |
| `retour_externe` | Retours parcellaires à pousser vers le serveur |
| `securite_compte` | Comptes autorisés pour l'interopérabilité |
