# Documentation Technique - Améliorations de l'Interopérabilité

## 1. Gestion des CRL (Commission de Reconnaissance Locale)

### 1.1 Modèle `RoleCrl` (`models/RoleCrl.py`)

#### Méthode `insert_role(data)`

**Avant :**
```python
def insert_role(self, data):
    # data = [iddemande, id_role, idpersonne, titulaire]
    SQL: INSERT INTO demande_crl(iddemande, id_role, idpersonne, titulaire, affiche)
```

**Après :**
```python
def insert_role(self, data):
    # data = [iddemande, id_role, idpersonne, titulaire, president]
    SQL: INSERT INTO demande_crl(iddemande, id_role, idpersonne, titulaire, president, affiche)
    SQL: UPDATE demande_crl SET idpersonne=%s, titulaire=%s, president=%s, affiche=true
```

La colonne `president` (booléenne) est maintenant gérée dans l'upsert (UPDATE puis INSERT conditionnel).

#### Nouvelle méthode `find_or_create_by_lib(lib)`

```python
def find_or_create_by_lib(self, lib):
    role = self.find_by_lib(lib)
    if role:
        return role
    # INSERT INTO role_crl (libelle_role) VALUES (%s) RETURNING id_role
    return (id_role, lib)
```

Crée automatiquement le rôle dans `role_crl` s'il n'existe pas. Évite les erreurs silencieuses quand un rôle comme "President" est absent de la table.

### 1.2 Dialogue Attribution des dates (`Dates/AttributionDateRun.py`)

#### Méthode `assignerCRL()`

**Améliorations :**
- Barre de progression via `QProgressDialog`
- `QApplication.processEvents()` pour une UI responsive
- Vérifications préalables (demandes sélectionnées, membres CRL présents)
- `try/except` global avec message d'erreur explicite
- Ajout de `data.append(False)` pour le champ `president`

#### Méthode `lisCRL()`

**Correction :** Vérification que `find_by_lib` ne retourne pas `None` avant d'accéder à `role[0]`.

---

## 2. Transformation des demandes (`Interroperabilite/ListeDossierExterneRun.py`)

### 2.1 Nouvelle insertion CRL dans `_traiterDemande()`

**Emplacement :** Après l'insertion des voisins (l.766-802)

**Logique :**
```python
rl = item.get("rl") or {}
for m in rl.get("membres_crl") or []:
    pdata = m.get("personne", m)
    role_lib = m.get("role", "")
    is_titulaire = m.get("titulaire", True)
    is_president = m.get("president", False)
    
    # 1. Trouver ou créer le rôle
    role = RoleCrl.find_or_create_by_lib(role_lib)
    
    # 2. Insérer la personne
    p = Personne()
    # ... mapping des champs ...
    id_personne = Personne.insert(self.connection, p)
    
    # 3. Lier à la demande
    data = [id_demande, role[0], id_personne, is_titulaire, is_president]
    RoleCrl.insert_role(data)
```

### 2.2 Nouvelle insertion CRL dans `validerDemandes()`

Même logique que `_traiterDemande()`, utilisant les `membres` déjà extraits du payload.

### 2.3 Gestion des transactions

#### `enregistrerDemande()`

```python
# Avant
except Exception as e:
    print("Erreur:", str(e))           # Pas de rollback

# Après
except Exception as e:
    print("Erreur:", str(e))
    self.connection.rollback()          # Nettoyage de la transaction
finally:
    self.progressBar.hide()

# Et si aucune demande n'a été traitée avec succès :
if not traite_ok:
    self.connection.rollback()
```

#### `validerDemandes()` (dans ListeDossierExterneRun et BatchDemandeRun)

```python
# Après updateTraitementStatut
self.connection.commit()

# En cas d'exception
except Exception as e:
    self.connection.rollback()
    # ... affichage erreur ...
```

---

## 3. Fiabilisation connexion base (`modeles/fiplofIngestionModel.py`)

### 3.1 `updateTraitementStatut()` - Fermeture du curseur

```python
@staticmethod
def updateTraitementStatut(connection, ...):
    cursor = connection.cursor()
    try:
        # ... execution SQL ...
        return cursor.rowcount > 0
    finally:
        cursor.close()      # Évite la fuite de curseurs
```

---

## 4. Envoi des retours API (`EnvoiMiseAJourRun.py`)

### 4.1 Mécanisme de réessai

Extraction de la logique d'envoi dans `_push_ids()` :

```python
def _push_ids(self, ids, url):
    payload = {"ids": ids}
    data = json.dumps(payload)
    req = urllib2.Request(url, data, {"Content-Type": "application/json"})
    resp = urllib2.urlopen(req, timeout=30)
    body = resp.read()
    resp.close()
```

Avec proposition de réessai en cas d'erreur HTTP :

```python
except urllib2.HTTPError as e:
    retry = QMessageBox.question(self, ..., "Voulez-vous réessayer ?")
    if retry == QMessageBox.Yes:
        self._push_ids(ids, url)
    else:
        raise
```

---

## 5. Schéma récapitulatif des flux

```
┌─────────────────────────────────────────────────────────────┐
│                  Transformation Demande                       │
│  (ListeDossierExterneRun.py)                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  JSON externe ──► enregistrerDemande() ──► _traiterDemande() │
│                                              │               │
│                    ┌─────────────────────────┼───────────┐   │
│                    ▼                         ▼           ▼   │
│              Insertion Parcelle       Insertion Demande  CRL │
│              (parcelled)              (demande)         │   │
│                                                        │   │
│                    ┌────────────────────────────────────┘   │
│                    ▼                                        │
│              Insertion Personne                             │
│              (personne)                                     │
│                    │                                        │
│                    ▼                                        │
│              Insertion AvoirDemande                         │
│              Insertion BlobPersonne                         │
│              Insertion LimiteParcelle                       │
│                    │                                        │
│                    ▼                                        │
│              Insertion Membre CRL                           │
│              ├─ Trouver/créer le rôle                       │
│              ├─ Insérer la personne                         │
│              └─ Insérer dans demande_crl                    │
│                    │                                        │
│                    ▼                                        │
│              COMMIT ou ROLLBACK                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 6. Modifications par fichier

| Fichier | Modifications |
|---------|---------------|
| `models/RoleCrl.py` | `insert_role()` gère `president` ; nouvelle méthode `find_or_create_by_lib()` |
| `Dates/AttributionDateRun.py` | Barre de progression, `try/except`, vérif null role, `president=False` |
| `Interroperabilite/ListeDossierExterneRun.py` | Insertion CRL dans `_traiterDemande()` et `validerDemandes()` ; commit/rollback |
| `Interroperabilite/BatchDemandeRun.py` | Ajout `commit()` et `rollback()` |
| `Interroperabilite/modeles/fiplofIngestionModel.py` | Fermeture curseur dans `updateTraitementStatut()` |
| `Interroperabilite/EnvoiMiseAJourRun.py` | Mécanisme de réessai + extraction `_push_ids()` |

## 7. Tests à effectuer

1. **Attribution CRL :** Ajouter des membres CRL, sélectionner des demandes, cliquer Assigner → vérifier barre de progression et message de succès
2. **Rôle inexistant :** Utiliser un rôle qui n'existe pas dans `role_crl` → vérifier création automatique
3. **Transformation demande :** Importer un JSON avec `membres_crl` → vérifier insertion dans `demande_crl`
4. **Flag président :** Vérifier que `president=true` est correctement sauvegardé
5. **Erreur transaction :** Simuler une erreur réseau → vérifier rollback et absence de blocage
6. **Envoi API :** Déclencher une erreur 500 → vérifier la boîte de réessai
