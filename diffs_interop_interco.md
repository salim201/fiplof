# Guide de fusion : fiplof_interop vers fiplof_interco

> **Objectif** : Integrer la fonctionnalite Interoperabilite de fiplof_interop dans
> fiplof_interco sans regression.
> **Date d'analyse** : 2026-08-25
> **Auteur** : Agent IA (analyse automatique)

---

## Table des matieres

1. [Vue d'ensemble des differences](#1-vue-densemble-des-differences)
2. [Pre-requis et mises en garde](#2-pre-requis-et-mises-en-garde)
3. [Phase 1 - Fichiers SQL a appliquer](#3-phase-1--fichiers-sql-a-appliquer)
4. [Phase 2 - Copier les nouveaux fichiers](#4-phase-2--copier-les-nouveaux-fichiers)
5. [Phase 3 - Modifier les fichiers existants](#5-phase-3--modifier-les-fichiers-existants)
6. [Phase 4 - Modifications dans main.ui / main.py](#6-phase-4--modifications-dans-mainui--mainpy)
7. [Phase 5 - Modifications dans plof.py](#7-phase-5--modifications-dans-plofpy)
8. [Phase 6 - Modifications dans Utils.py](#8-phase-6--modifications-dans-utilspy)
9. [Phase 7 - Modifications dans les modules existants](#9-phase-7--modifications-dans-les-modules-existants)
10. [Fichiers a NE PAS copier](#10-fichiers-a-ne-pas-copier)
11. [Verifications post-fusion](#11-verifications-post-fusion)

---

## 1. Vue d'ensemble des differences

| Categorie | Nombre de fichiers | Description |
|---|---|---|
| Nouveau module Interroperabilite/ | 21 .py + 5 .ui + 1 .ini | Module complet d interoperabilite (MVC) |
| Nouveaux modeles models/ | 6 fichiers | AvoirDemande, BlobPersonne, Hameau, Personne, Pointscardinaux, Projet |
| Modeles modifies models/ | 8 fichiers | Demande, Parcelled, Commune, District, Fokontany, Limiteparcelle, RoleCrl, CompareDbModel |
| Fichiers d entree modifies | 4 fichiers | plof.py, main.py, main.ui, Utils.py |
| Modules modifies | 4 fichiers | Crl/CrlRun.py, Dates/AttributionDateRun.py, Projet/AddLayerRun.py, Synchronisation/ConnectRemote.py |
| Nouveau SQL | 1 fichier | interoperabilite05_08_2025.sql (5 tables + triggers) |
| Documentation | 5 fichiers .md | Guides utilisateur et technique |

---

## 2. Pre-requis et mises en garde

### AVANT de commencer

1. **Sauvegarder la base de donnees** PostgreSQL de fiplof_interco
2. **Sauvegarder le code source** de fiplof_interco (git commit ou copie)
3. Verifier que fiplof_interco a le module Python `shapely` disponible (requis par BatchDemandeRun.py et ListeDossierExterneRun.py)
4. Verifier que fiplof_interco a le module Python `urllib2` (requis par EnvoiMiseAJourRun.py et SuiviRun.py)
5. Le module Interroperabilite communique avec une API FastAPI externe (URL configurable via Interroperabilite/interop.ini). Cette API doit etre operationnelle pour que l interoperabilite fonctionne.

### Conventions de ce document

- **Copier depuis interop** = copier le fichier tel quel depuis `/mnt/c/fiplof_interop/`
- **Fusionner** = appliquer le diff specifique decrit, en conservant le reste du fichier interco
- Les noms de chemins sont relatifs a la racine du projet

---

## 3. Phase 1 - Fichiers SQL a appliquer

### 3.1 Copier le fichier SQL d interoperabilite

**Source** : `/mnt/c/fiplof_interop/sql/interoperabilite05_08_2025.sql`
**Destination** : `/mnt/c/fiplof_interco/sql/interoperabilite05_08_2025.sql`

Ce fichier cree :
- **5 nouvelles tables** : `fiplof_raw_ingestion`, `securite_compte_api`, `retour_externe`, `inbound_dossiers`, `inbound_idempotency`
- **2 functions** : `set_personne_identity_key()`, `update_updated_at()`
- **4 triggers** : `trg_set_personne_identity_key`, `trg_update_compte_api`, `trg_retour_externe_demande`, `trg_retour_externe_certificat`
- **Modifications sur `personne`** : supprime contrainte `uk_cin`, ajoute colonne `cin_nom_prenom_key` + contrainte `uk_personne_identity`
- **Ajout de colonnes** : commune, valid_parcelle, error_parcelle, traitement_* sur fiplof_raw_ingestion ; nom sur securite_compte_api
- **Index** sur fiplof_raw_ingestion et securite_compte_api

### 3.2 IMPORTANT - Executer le SQL sur la base de fiplof_interco

Avant de lancer l application, executer ce fichier SQL sur la base PostgreSQL de fiplof_interco. Le systeme de migration (adapters/migrations/) le fera automatiquement si le fichier est place dans sql/ avec une date inferieure ou egale a la date actuelle.

**Note** : La table `demande_crl` doit avoir une colonne `president` (booleen). Si elle n existe pas, ajouter :
```sql
ALTER TABLE demande_crl ADD COLUMN IF NOT EXISTS president BOOLEAN DEFAULT FALSE;
```

---

## 4. Phase 2 - Copier les nouveaux fichiers

### 4.1 Module Interroperabilite (tout le dossier)

Copier **tout le dossier** `/mnt/c/fiplof_interop/Interroperabilite/` vers `/mnt/c/fiplof_interco/Interroperabilite/`.

Structure a copier :
```
Interroperabilite/
  __init__.py                          # -*- coding: utf-8 -*-
  api_config.py                        # Lecture/ecriture URL API depuis interop.ini
  interop.ini                          # Config URL API (base_url)
  db_utils.py                          # Utilitaires reconnexion BD
  BatchDemande.py                      # UI (auto-genere depuis BatchDemande.ui)
  BatchDemande.ui                      # Qt Designer - fenetre batch
  BatchDemandeRun.py                   # Logique batch (~1317 lignes)
  ListeDossierExterne.py               # UI (auto-genere depuis ListeDossierExterne.ui)
  ListeDossierExterne.ui               # Qt Designer - transformation demande
  ListeDossierExterneRun.py            # Logique transformation (~1884 lignes)
  EnvoiMiseAJour.py                    # UI (auto-genere depuis EnvoiMiseAJour.ui)
  EnvoiMiseAJour.ui                    # Qt Designer - envoi mise a jour
  EnvoiMiseAJourRun.py                 # Logique envoi (289 lignes)
  SecuriteCompte.py                    # UI (auto-genere depuis SecuriteCompte.ui)
  SecuriteCompte.ui                    # Qt Designer - gestion comptes
  SecuriteCompteRun.py                 # Logique gestion comptes
  Suivi.ui                             # Qt Designer - suivi
  SuiviRun.py                          # Logique suivi (470 lignes)
  ConfigFIPLOFRun.py                   # Configuration URL service FIPLOF
  test_securite.py                     # Tests
  controlleurs/
    __init__.py                        # -*- coding: utf-8 -*-
    batchDemandeController.py          # Controleur batch (72 lignes)
    securiteCompteController.py        # Controleur securite (21 lignes)
  modeles/
    __init__.py                        # Exports SecuriteCompteModel, FiplofIngestionModel
    fiplofIngestionModel.py            # Modele ingestion (239 lignes)
    securiteCompteModel.py             # Modele comptes API (267 lignes)
```

**NE PAS copier** : `BatchDemandeRun copy.py` (fichier de surete inutile)

### 4.2 Nouveaux fichiers a la racine

Copier depuis interop :
- `batchdemande.py` -> racine de interco (fichier stub/auto-genere, peu utile mais inoffensif)
- `output.py` -> racine de interco (fichier stub/auto-genere)

### 4.3 Nouveaux fichiers dans models/

Copier ces 6 fichiers **tels quels** depuis interop :
- `models/AvoirDemande.py` (113 lignes)
- `models/BlobPersonne.py` (290 lignes)
- `models/Hameau.py` (73 lignes)
- `models/Personne.py` (208 lignes)
- `models/Pointscardinaux.py` (99 lignes)
- `models/Projet.py` (160 lignes)

### 4.4 Documentation (optionnel)

Copier depuis interop (optionnel mais recommande) :
- `manuel_menu_interoperabilite.md` -> racine
- `objet_objectif_fiplof.md` -> racine
- `todo.md` -> racine
- `docs/Amelioration_Interoperabilite_Guide_Utilisateur.md` -> dossier docs/
- `docs/Amelioration_Interoperabilite_Technique.md` -> dossier docs/

---

## 5. Phase 3 - Modifier les fichiers existants

### 5.1 models/Demande.py - Ajouter 3 methodes statiques

**Fichier** : `models/Demande.py`

**Action** : Ajouter `# -*- coding: utf-8 -*-` en premiere ligne du fichier.

**Action** : Ajouter le code suivant APRES la methode `__init__` (apres la ligne `self.idPresidentCrl = None`) et AVANT la methode `findBetween` :

```python
    @staticmethod
    def incrementCptDemande(connection, commune):
        try:
            cur = connection.cursor()
            sql = """
                UPDATE commune
                SET cptdemande = cptdemande + 1
                WHERE UPPER(TRIM(nomcommune)) = UPPER(TRIM(%s))
            """
            cur.execute(sql, (commune,))
            connection.commit()
            cur.close()
        except Exception as e:
            connection.rollback()
            print("Erreur incrementCptDemande :", e)

    @staticmethod
    def creationNum(connection, codedistrict, commune):
        """
        Format : 105-11-F-33000
        codedistrict-codeg-F-cptdemande(commune)
        """
        try:
            cur = connection.cursor()
            sql = """
                SELECT codeg, cptdemande
                FROM commune
                WHERE UPPER(nomcommune) = UPPER(%s)
            """
            cur.execute(sql, (commune,))
            result = cur.fetchone()
            if result:
                codeg = result[0]
                cptdemande = result[1]
            else:
                codeg = None
                cptdemande = 0
            num_demande = "%s-%s-F-%s" % (codedistrict, codeg, cptdemande)
            cur.close()
            return num_demande
        except Exception as e:
            print("Erreur creationNum :", e)
            return None

    @staticmethod
    def insert(connection, data):
        print('DEBUG  insert Demande: ', data)
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO demande (
                    numdemande, gid, datedemande, datedecision, numdecision,
                    datereconnaissance, region, district, commune, fokontany,
                    idfokontany, idcommune, consistance, idprojet, code_parcelle,
                    categorie, debut_affichage, fin_affichage, duree_occupation,
                    origine, avis_crl, texte_crl
                )
                VALUES (
                    %(numdemande)s, %(gid)s, %(datedemande)s, %(datedecision)s,
                    %(numdecision)s, %(datereconnaissance)s, %(region)s, %(district)s,
                    %(commune)s, %(fokontany)s, %(idfokontany)s, %(idcommune)s,
                    %(consistance)s, %(idprojet)s, %(code_parcelle)s, %(categorie)s,
                    %(debut_affichage)s, %(fin_affichage)s, %(duree_occupation)s,
                    %(origine)s, %(avis_crl)s, %(texte_crl)s
                )
                RETURNING iddemande;
            """
            cursor.execute(query, data)
            idd = cursor.fetchone()[0]
            connection.commit()
            return idd
        except Exception as e:
            connection.rollback()
            print("INSERT ERROR DEMANDE:", e)
            return None
        finally:
            cursor.close()
```

### 5.2 models/Parcelled.py - Ajouter 2 methodes statiques

**Fichier** : `models/Parcelled.py`

**Action** : Ajouter le code suivant APRES la derniere methode existante (apres `return None`) :

```python
    @staticmethod
    def insert_parcelle_d_by_interrop(connection, data):
        """
        data = dict venant de ton JSON API
        """
        print("DEBUG  insert_parcelle_d_by_interrop ", data)
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO parcelle_d (
                    codeparcelle, commune, district, region, fkt,
                    idhameau, consistance, categorie, id_commune,
                    geom, surface
                )
                VALUES (
                    %(parcelle)s, %(commune)s, %(district)s, %(region)s,
                    %(fkt)s, %(id_hameau)s, %(consistance)s, %(categorie)s,
                    %(id_commune)s,
                    ST_SetSRID(
                        ST_GeomFromWKB(decode(%(geom)s, 'hex')),
                        29702
                    ),
                    ST_Area(
                        ST_SetSRID(
                            ST_GeomFromWKB(decode(%(geom)s, 'hex')),
                            29702
                        )
                    )
                )
                RETURNING gid
            """
            cursor.execute(query, data)
            gid = cursor.fetchone()[0]
            connection.commit()
            print("DEBUG  gid ", gid)
            return gid
        except Exception as e:
            connection.rollback()
            print("INSERT ERROR parcelle_d:", str(e))
            return None
        finally:
            cursor.close()

    @staticmethod
    def updateNumDemande(connection, gid, numdemande):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            sql = """
                UPDATE parcelle_d
                SET numdemande = %s
                WHERE gid = %s
            """
            cursor.execute(sql, (numdemande, gid))
            connection.commit()
            print("INFO : updateNumDemande EFFECTUE")
            return True
        except Exception as e:
            connection.rollback()
            print("Erreur updateNumDemande :", e)
        finally:
            cursor.close()
        return False
```

### 5.3 models/Commune.py - Ajouter findByName

**Fichier** : `models/Commune.py`

**Action** : Ajouter APRES la methode `map` :

```python
    @staticmethod
    def findByName(connection, nom_commune):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('DEBUG: Commune', nom_commune)
        try:
            cursor.execute(
                """
                SELECT *
                FROM commune
                WHERE UPPER(TRIM(nomcommune)) = UPPER(TRIM(%s))
                """,
                (nom_commune,)
            )
            res = cursor.fetchone()
            if res is None:
                return None
            commune = Commune()
            commune.map(res)
            return commune
        except Exception as e:
            print("[Commune.findByName] erreur:", e)
            return None
        finally:
            cursor.close()
```

### 5.4 models/District.py - Ajouter getByName

**Fichier** : `models/District.py`

**Action** : Ajouter APRES la methode `map` :

```python
    @staticmethod
    def getByName(connection, nomdistrict):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('DEBUG: Nomdistrict', nomdistrict)
        try:
            cursor.execute("""
                SELECT *
                FROM district
                WHERE UPPER(TRIM(nomdistrict)) = UPPER(TRIM(%s))
            """, (nomdistrict,))
            res = cursor.fetchone()
            if res is None:
                return None
            t = District()
            t.map(res)
            print('DEBUG: res', res)
            return t
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return None
```

### 5.5 models/Fokontany.py - Ajouter imports + findByName

**Fichier** : `models/Fokontany.py`

**Action 1** : Ajouter en haut du fichier (avant `from BaseModel import BaseModel`) :
```python
import psycopg2
import psycopg2.extras
```

**Action 2** : Ajouter APRES la methode `map` :

```python
    @staticmethod
    def findByName(connection, nom_fokontany):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                """
                SELECT *
                FROM fokontany
                WHERE UPPER(TRIM(nomfokontany)) = UPPER(TRIM(%s))
                """,
                (nom_fokontany,)
            )
            res = cursor.fetchone()
            if res is None:
                return None
            f = Fokontany(connection)
            f.map(res)
            return f
        except Exception as e:
            print("[Fokontany.findByName] erreur:", e)
            return None
        finally:
            cursor.close()
```

### 5.6 models/Limiteparcelle.py - Ajouter insert

**Fichier** : `models/Limiteparcelle.py`

**Action** : Ajouter APRES la methode `findAll` :

```python
    @staticmethod
    def insert(connection, lp):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            sql = """
                INSERT INTO limitesparcelle
                (idpointscardinaux, idparcelle, description)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (
                lp.idpointscardinaux,
                lp.idparcelle,
                lp.description
            ))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print("Erreur insert LimitesParcelle :", e)
        finally:
            cursor.close()
        return False
```

### 5.7 models/RoleCrl.py - Modifier insert_role + ajouter find_or_create_by_lib

**Fichier** : `models/RoleCrl.py`

**Action 1** : Remplacer la methode `insert_role` existante par :

```python
    def insert_role(self, data):
        cursor = self.connection.cursor()
        try:
            sql = ('UPDATE demande_crl SET idpersonne=%s, titulaire=%s, president=%s, affiche=true '
                   'WHERE iddemande=%s AND id_role=%s AND titulaire=%s;'
                   'INSERT INTO demande_crl(iddemande, id_role, idpersonne, titulaire, president, affiche) '
                   'SELECT %s,%s,%s,%s,%s,true '
                   'WHERE NOT EXISTS(SELECT * FROM demande_crl WHERE iddemande=%s AND id_role=%s AND titulaire=%s)')
            print sql
            res = cursor.execute(sql, (
                data[2], data[3], data[4],
                data[0], data[1], data[3],
                data[0], data[1], data[2], data[3], data[4],
                data[0], data[1], data[3]
            ))
            self.connection.commit()
            return res
        except Exception as e:
            print(e)
            self.connection.rollback()
```

**Action 2** : Ajouter APRES la methode `insert_role` (et AVANT la fin du fichier) :

```python
    def find_or_create_by_lib(self, lib):
        role = self.find_by_lib(lib)
        if role:
            return role
        cursor = self.connection.cursor()
        try:
            sql = "INSERT INTO role_crl (libelle_role) VALUES (%s) RETURNING id_role"
            cursor.execute(sql, (lib,))
            id_role = cursor.fetchone()[0]
            self.connection.commit()
            return (id_role, lib)
        except Exception as e:
            print(e)
            self.connection.rollback()
            return None
```

### 5.8 models/CompareDbModel.py - Commenter les prints debug

**Fichier** : `models/CompareDbModel.py`

**Action** : La methode la plus simple est de **copier directement le fichier depuis interop** car les changements sont principalement du nettoyage de prints de debug. Les seuls changements fonctionnels sont :
1. Les `cur1.close()` / `cur2.close()` sont commentes dans le bloc except (evite des erreurs sur curseurs deja fermes)
2. Le print `+++++++++++++++++++ delete*************************` est supprime de la boucle de suppression

**Alternative** : Commenter les prints de debug identifies dans le diff, en suivant le fichier interop comme reference.

---

## 6. Phase 4 - Modifications dans main.ui / main.py

### 6.1 main.ui - Ajouter le menu Interoperabilite

**Fichier** : `main.ui`

**Action** : Ajouter un nouveau menu `menuInterrop_rabilite` dans la barre de menus.

Dans le fichier .ui XML, ajouter APRES la definition de menuA_Propos :

```xml
<widget class="QMenu" name="menuInterrop_rabilit">
 <property name="title">
  <string>Interopérabilité</string>
 </property>
 <addaction name="actionReception_Demande"/>
 <addaction name="actionTransformation_en_demande"/>
 <addaction name="actionSuiviReception_Demande"/>
 <addaction name="separator"/>
 <addaction name="actionGestion_Compte_Interrop_rabilit"/>
 <addaction name="actionConfiguuration_Service_FIPLOF"/>
</widget>
```

Et ajouter les actions correspondantes :

```xml
<action name="actionReception_Demande">
 <property name="text"><string>Reception Demande</string></property>
</action>
<action name="actionSuiviReception_Demande">
 <property name="text"><string>Suivi</string></property>
</action>
<action name="actionGestion_Compte_Interrop_rabilit">
 <property name="text"><string>Gestion Compte Interropérabilité</string></property>
</action>
<action name="actionTransformation_en_demande">
 <property name="text"><string>Transformation en demande</string></property>
</action>
<action name="actionConfiguuration_Service_FIPLOF">
 <property name="text"><string>Configuration Service FIPLOF</string></property>
</action>
```

**Alternative** : Recompiler le .ui avec `pyuic4 main.ui > main.py` apres modification.

### 6.2 main.py - Ajouter les actions et le menu

**Fichier** : `main.py`

**Action 1** : Ajouter APRES `self.menuA_Propos = ...` :

```python
        self.menuInterrop_rabilit = QtGui.QMenu(self.menubar)
        self.menuInterrop_rabilit.setObjectName(_fromUtf8("menuInterrop_rabilit"))
```

**Action 2** : Ajouter APRES `self.actionGestion_CLR = ...` :

```python
        self.actionReception_Demande = QtGui.QAction(MainWindow)
        self.actionReception_Demande.setObjectName(_fromUtf8("actionReception_Demande"))
        self.actionSuiviReception_Demande = QtGui.QAction(MainWindow)
        self.actionSuiviReception_Demande.setObjectName(_fromUtf8("actionSuiviReception_Demande"))
        self.actionGestion_Compte_Interrop_rabilit = QtGui.QAction(MainWindow)
        self.actionGestion_Compte_Interrop_rabilit.setObjectName(_fromUtf8("actionGestion_Compte_Interrop_rabilit"))
        self.actionTransformation_en_demande = QtGui.QAction(MainWindow)
        self.actionTransformation_en_demande.setObjectName(_fromUtf8("actionTransformation_en_demande"))
        self.actionConfiguuration_Service_FIPLOF = QtGui.QAction(MainWindow)
        self.actionConfiguuration_Service_FIPLOF.setObjectName(_fromUtf8("actionConfiguuration_Service_FIPLOF"))
```

**Action 3** : Ajouter APRES `self.menuPLOF.addAction(self.actionSauvergarde_en_ligne)` :

```python
        self.menuInterrop_rabilit.addAction(self.actionReception_Demande)
        self.menuInterrop_rabilit.addAction(self.actionTransformation_en_demande)
        self.menuInterrop_rabilit.addAction(self.actionSuiviReception_Demande)
        self.menuInterrop_rabilit.addSeparator()
        self.menuInterrop_rabilit.addAction(self.actionGestion_Compte_Interrop_rabilit)
        self.menuInterrop_rabilit.addAction(self.actionConfiguuration_Service_FIPLOF)
```

**Action 4** : Ajouter APRES `self.menubar.addAction(self.menuPLOF.menuAction())` :

```python
        self.menubar.addAction(self.menuInterrop_rabilit.menuAction())
```

**Action 5** : Ajouter APRES `self.menuA_Propos.setTitle(...)` :

```python
        self.menuInterrop_rabilit.setTitle(_translate("MainWindow", "Interopérabilité", None))
```

**Action 6** : Remplacer `"Gestion CLR"` par `"Gestion CRL"` (correction typo)

**Action 7** : Ajouter APRES `self.actionGestion_CLR.setText(...)` :

```python
        self.actionReception_Demande.setText(_translate("MainWindow", "Reception Demande", None))
        self.actionSuiviReception_Demande.setText(_translate("MainWindow", "Suivi", None))
        self.actionGestion_Compte_Interrop_rabilit.setText(_translate("MainWindow", "Gestion Compte Interropérabilité", None))
        self.actionTransformation_en_demande.setText(_translate("MainWindow", "Transformation en demande", None))
        self.actionConfiguuration_Service_FIPLOF.setText(_translate("MainWindow", "Configuration Service FIPLOF", None))
```

---

## 7. Phase 5 - Modifications dans plof.py

**Fichier** : `plof.py`

### 7.1 Connexion BD avec keepalive

**Action** : Remplacer la ligne de connexion BD (~ligne 257) :

```python
# ANCIEN :
self.connection = psycopg2.connect(database=self.db_config.db_name, user=self.db_config.db_user, password=self.db_config.db_pass, host=self.db_config.db_host)

# NOUVEAU :
try:
    self.connection = psycopg2.connect(database=self.db_config.db_name, user=self.db_config.db_user, password=self.db_config.db_pass, host=self.db_config.db_host,
                                       keepalives=1, keepalives_idle=30, keepalives_interval=10, keepalives_count=3)
except (psycopg2.OperationalError, TypeError):
    self.connection = psycopg2.connect(database=self.db_config.db_name, user=self.db_config.db_user, password=self.db_config.db_pass, host=self.db_config.db_host)
from Utils import disable_idle_timeout
disable_idle_timeout(self.connection)
```

### 7.2 Connexion des signaux Interoperabilite

**Action** : Ajouter APRES `self.ui.actionRe_Impression.triggered.connect(self.ReimpressionOriginal)` :

```python
        # Connexion du menu Interoperabilite
        self.ui.actionReception_Demande.setVisible(False)
        self.ui.actionTransformation_en_demande.triggered.connect(self.transformationEnDemande)
        self.ui.actionGestion_Compte_Interrop_rabilit.setVisible(False)

        self.actionEnvoiMiseAJour = QtGui.QAction(self.MainWindow)
        self.actionEnvoiMiseAJour.setText(u"Envoi mise \xe0 jour")
        self.ui.menuInterrop_rabilit.insertAction(
            self.ui.actionSuiviReception_Demande, self.actionEnvoiMiseAJour)
        self.actionEnvoiMiseAJour.triggered.connect(self.envoiMiseAJour)

        self.ui.actionSuiviReception_Demande.triggered.connect(self.showSuivi)
        self.ui.actionConfiguuration_Service_FIPLOF.triggered.connect(self.openConfigFIPLOF)
```

### 7.3 Ajouter les 6 methodes handler

**Action** : Ajouter les methodes suivantes dans la classe Plof (par exemple avant `def rechercheDemande`) :

```python
    def batchDemande(self):
        try:
            from Interroperabilite.controlleurs.batchDemandeController import BatchDemandeController
            controller = BatchDemandeController(self)
            controller.showBatchDemande()
        except Exception as er:
            print ("Erreur lors de l'ouverture du batch demande:", str(er))

    def transformationEnDemande(self):
        try:
            from Interroperabilite.controlleurs.batchDemandeController import BatchDemandeController
            controller = BatchDemandeController(self)
            controller.showListeDossierATransformer()
        except Exception as er:
            print ("Erreur lors de l'ouverture du batch demande:", str(er))

    def gestionCompteInteroperabilite(self):
        try:
            from Interroperabilite.controlleurs.securiteCompteController import SecuriteCompteController
            controller = SecuriteCompteController(self.connection)
            controller.showDialog()
        except Exception as er:
            print("Erreur Gestion Compte Interoperabilite:", str(er))

    def envoiMiseAJour(self):
        try:
            from Interroperabilite.controlleurs.batchDemandeController import BatchDemandeController
            controller = BatchDemandeController(self)
            controller.showEnvoiMiseAJour()
        except Exception as er:
            print("Erreur lors de l'ouverture envoi mise a jour:", str(er))

    def showSuivi(self):
        try:
            from Interroperabilite.controlleurs.batchDemandeController import BatchDemandeController
            controller = BatchDemandeController(self)
            controller.showSuivi()
        except Exception as er:
            print("Erreur lors de l'ouverture suivi:", str(er))

    def openConfigFIPLOF(self):
        try:
            from Interroperabilite.ConfigFIPLOFRun import ConfigFIPLOFRun
            dialog = ConfigFIPLOFRun()
            dialog.exec_()
        except Exception as er:
            print("Erreur lors de l'ouverture config FIPLOF:", str(er))
```

---

## 8. Phase 6 - Modifications dans Utils.py

**Fichier** : `Utils.py`

### 8.1 Ajouter les fonctions module-level

**Action** : Ajouter APRES les imports (avant `class Utils:`) :

```python
def disable_idle_timeout(conn):
    try:
        cur = conn.cursor()
        cur.execute("SET idle_in_transaction_session_timeout = 0")
        cur.close()
    except Exception:
        pass


def create_connection():
    from Configuration import DbConfig
    cfg = DbConfig.DbConfig()
    try:
        conn = psycopg2.connect(database=cfg.db_name, user=cfg.db_user,
                                password=cfg.db_pass, host=cfg.db_host,
                                keepalives=1, keepalives_idle=30,
                                keepalives_interval=10, keepalives_count=3)
    except (psycopg2.OperationalError, TypeError):
        conn = psycopg2.connect(database=cfg.db_name, user=cfg.db_user,
                                password=cfg.db_pass, host=cfg.db_host)
    disable_idle_timeout(conn)
    return conn
```

### 8.2 Ajouter _ensureConnection dans la classe Utils

**Action** : Ajouter dans la classe Utils, APRES `def __init__` :

```python
    def _ensureConnection(self):
        if self.connection is None or self.connection.closed:
            self.connection = create_connection()
```

### 8.3 Modifier fillComboWithSql

**Action** : Dans `fillComboWithSql`, ajouter `self._ensureConnection()` comme premiere ligne du corps, et wrapper le `self.connection.rollback()` dans un try/except :

```python
    def fillComboWithSql(self, combowidget, sql, column, idcolumn):
        self._ensureConnection()
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # ... (reste du code inchangé) ...
        except Exception as e:
            print(e)
            try:
                self.connection.rollback()
            except Exception:
                pass
```

---

## 9. Phase 7 - Modifications dans les modules existants

### 9.1 Crl/CrlRun.py

**Fichier** : `Crl/CrlRun.py`

**Action** : **Copier directement le fichier depuis interop** car le changement est massif (passe de 34 a 183 lignes). Les 6 nouvelles methodes sont :
- `initActions()` - connexion des signaux UI
- `changeFieldsStatus()` - activation/desactivation des champs
- `fillFokontany()` - remplissage combo fokontany
- `fillHameau()` - remplissage combo hameau
- `onDemandeClicked()` - affichage CRL pour une demande
- `rechercher()` - recherche dynamique avec filtres

### 9.2 Dates/AttributionDateRun.py

**Fichier** : `Dates/AttributionDateRun.py`

**Action 1** : Remplacer la methode `assignerCRL` par la version interop. Changements cles :
- Early returns au lieu de nested if/else
- Ajout d un QProgressDialog pour les boucles longues
- Ajout de `QApplication.processEvents()` pour la reactivite UI
- Ajout de `data.append(False)` pour le nouveau champ president
- Fix des prefixes unicode pour Python 2
- Wrapping du tout dans un try/except global

**Action 2** : Dans `lisCRL`, ajouter le guard `if role is None: continue` apres `role = RoleCrlModel.find_by_lib(rolecrl)`.

### 9.3 Projet/AddLayerRun.py

**Fichier** : `Projet/AddLayerRun.py`

**Action** : Appliquer les changements suivants :
1. Ajouter `import os` et `from osgeo import gdal`
2. Modifier `browse_file` pour ajouter un filtre raster spécifique
3. Ajouter la methode `_estRasterValide(self, filename)` qui valide les rasters via GDAL
4. Ajouter des `QMessageBox.warning` pour les champs requis dans la validation
5. Ajouter validation specifique pour les fichiers raster

### 9.4 Synchronisation/ConnectRemote.py

**Fichier** : `Synchronisation/ConnectRemote.py`

**Action** : Ajouter les prints de debug dans la methode de synchronisation (lignes ~112-125). Changements mineurs uniquement.

---

## 10. Fichiers a NE PAS copier

### 10.1 Configuration (specifiques a l environnement)

| Fichier interop | Raison |
|---|---|
| Configuration/app.ini | Contient les infos de connexion DB d interop (ambovombe) - garder celles de interco |
| Configuration/params.ini | Chemin de sauvegarde specifique a interop |
| Configuration/remote.ini | Hote distant specifique a interop |
| Parametres/schema_plof.sql | Nom de base different (ambovombe vs interco) |
| interco/schema_plof.sql | Idem |

### 10.2 Fichiers de sauvegarde/artefacts

| Fichier interop | Raison |
|---|---|
| Interroperabilite/BatchDemandeRun copy.py | Copie de sauvegarde |
| *.pyc.r* | Artefacts SVN |
| *.mine | Conflits SVN |
| *.r1* | Versions SVN |
| Crl/output_file.py | Fichier temporaire |
| Crl/python | Fichier temporaire |
| Crl/pyuic4 | Fichier temporaire |

### 10.3 Logs et runtime

| Element | Raison |
|---|---|
| logs/ | Logs specifiques a interop |
| venv/ | Environnement virtuel specifique |
| cache/, debug/, error-log vierges/ | Artefacts runtime |

---

## 11. Verifications post-fusion

### 11.1 Verifications de code

1. Verifier que `Interroperabilite/` est bien dans le PYTHONPATH ou dans le repertoire racine du projet
2. Verifier que `shapely` est installe : `python -c "from shapely.geometry import shape; print('OK')"`
3. Verifier que la table `demande_crl` a bien la colonne `president` (ajouter l ALTER TABLE si necessaire)
4. Verifier que la table `commune` a les colonnes `cptdemande` et `codeg` (necessaires pour Demande.creationNum)
5. Verifier que les tables fiplof_raw_ingestion, securite_compte_api, retour_externe, inbound_dossiers, inbound_idempotency ont ete creees par le SQL

### 11.2 Verifications de lancement

1. Lancer l application via plof.bat ou run.pyw
2. Verifier que le menu Interoperabilite apparaît dans la barre de menus
3. Verifier que les 5 actions du menu sont bien affichees
4. Verifier que la connexion BD fonctionne (keepalive + idle timeout)
5. Verifier que le menu Gestion CRL (et non CLR) est correctement orthographie

### 11.3 Tests fonctionnels

1. **Configuration FIPLOF** : Ouvrir Configuration Service FIPLOF -> verifier que l URL API s affiche et est modifiable
2. **Transformation en demande** : Ouvrir Transformation en demande -> verifier que la liste des dossiers externes se charge
3. **Suivi** : Ouvrir Suivi -> verifier que les 3 onglets s affichent (Dossiers recus, Processing ARQ, Gestion Batch)
4. **Envoi mise a jour** : Ouvrir via le menu -> verifier que la table des retours externes se charge
5. **CRL** : Ouvrir Gestion CRL -> tester la recherche par fokontany/hameau/numero de decision

---

## Annexe - Script de fusion automatique (optionnel)

Pour une fusion semi-automatique, voici les commandes bash principales :

```bash
# Variables
SRC=/mnt/c/fiplof_interop
DST=/mnt/c/fiplof_interco

# Phase 1: SQL
cp "$SRC/sql/interoperabilite05_08_2025.sql" "$DST/sql/"

# Phase 2: Nouveau module Interroperabilite (sans le fichier copy)
rsync -av --exclude='*copy*' "$SRC/Interroperabilite/" "$DST/Interroperabilite/"

# Phase 2: Nouveaux fichiers racine
cp "$SRC/batchdemande.py" "$DST/"
cp "$SRC/output.py" "$DST/"

# Phase 2: Nouveaux modeles
for f in AvoirDemande BlobPersonne Hameau Personne Pointscardinaux Projet; do
    cp "$SRC/models/$f.py" "$DST/models/"
done

# Phase 2: Documentation (optionnel)
cp "$SRC/manuel_menu_interoperabilite.md" "$DST/"
cp "$SRC/objet_objectif_fiplof.md" "$DST/"
cp "$SRC/todo.md" "$DST/"

# Phase 3: Modeles modifies (copie directe pour CompareDbModel)
cp "$SRC/models/CompareDbModel.py" "$DST/models/"

# Phase 7-8: Modules modifies (copie directe pour CrlRun)
cp "$SRC/Crl/CrlRun.py" "$DST/Crl/"
```

**ATTENTION** : Les fichiers suivants necessitent des modifications manuelles (voir phases detaillees ci-dessus) :
- `models/Demande.py`
- `models/Parcelled.py`
- `models/Commune.py`
- `models/District.py`
- `models/Fokontany.py`
- `models/Limiteparcelle.py`
- `models/RoleCrl.py`
- `main.py`
- `main.ui`
- `plof.py`
- `Utils.py`
- `Dates/AttributionDateRun.py`
- `Projet/AddLayerRun.py`
- `Synchronisation/ConnectRemote.py`
