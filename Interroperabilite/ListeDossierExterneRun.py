# coding: utf-8
import sys
import os
import ast
try:
    from thread import get_ident
except ImportError:
    from threading import get_ident
from logs import xlsLogger
from PyQt4 import Qt,QtGui, QtCore
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *


from ListeDossierExterne import Ui_Dialog
import globalvars
from Etats.Html2Pdf import Html2Pdf
import webbrowser
import tempfile
from random import randint
import datetime
from Utils import Utils
from PyPDF2 import PdfFileMerger
from modeles.fiplofIngestionModel import FiplofIngestionModel
from models.Commune import Commune
from models.District import District
from models.Fokontany import Fokontany
from models.Hameau import Hameau
from models.Parcelled import Parcelled
from models.Demande import Demande
from models.Projet import Projet
from models.Personne import Personne
from models.AvoirDemande import AvoirDemande
from models.BlobPersonne import BlobPersonne
from models.Pointscardinaux import Pointscardinaux
from models.Limiteparcelle import Limiteparcelle
from models.RoleCrl import RoleCrl
import json

BASE_DIR = os.path.dirname(__file__)
PLUGIN_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
print("PYTHONPATH =", sys.path)
print("MODELS DIR =", os.listdir(r"C:\Fiplof_interco\models"))

if PLUGIN_DIR not in sys.path:
    sys.path.append(PLUGIN_DIR)

import psycopg2
import psycopg2.extras
import json
from shapely.geometry import shape

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class ListeDossierExterneRun(QDialog):
    def __init__(self, connection):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)       
        self._models = {}
        
        self.progressBar = QtGui.QProgressBar(self.ui.groupBoxDossier)
        self.progressBar.setRange(0, 0)
        self.progressBar.setFixedHeight(25)
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat(u" Chargement des donn\u00e9es...")
        self.progressBar.setStyleSheet("""
            QProgressBar { border: 1px solid #ccc; border-radius: 4px; text-align: center; }
            QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4CAF50, stop:1 #8BC34A); }
        """)
        self.progressBar.hide()
        self.ui.verticalLayout_3.insertWidget(2, self.progressBar)

        self._initDateDemande = self.ui.dateDemande.date()
        self._initDateDecision = self.ui.dateEditDateDecision.date()
        self._initDateDebutAff = self.ui.dateEditDebutAffichage.date()
        self._initDateFinAff = self.ui.dateEditFinAffichage.date()
        self._initDateRL = self.ui.dateEditRL.date()
        
        try:
            self.initDB()
            self.initActions()
        except Exception as e:
            print(e)
        QtCore.QTimer.singleShot(0, self.loadDataAfterShow)
       

    def initDB(self):
        self.cur = self.connection.cursor()
        self._ensureJsonTryParseFunction()

    def _ensureJsonTryParseFunction(self):
        try:
            cur = self.connection.cursor()
            cur.execute("""
                CREATE OR REPLACE FUNCTION json_try_parse(p_text text)
                RETURNS json AS $$
                BEGIN
                    RETURN p_text::json;
                EXCEPTION WHEN OTHERS THEN
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql IMMUTABLE;
            """)
            cur.close()
            self.connection.commit()
        except Exception:
            self.connection.rollback()
        
        

    def initActions(self):
        print("********************initActions**************************")
        self.ui.checkBoxFkt.stateChanged.connect(
            lambda s: self.ui.comboBoxFokontany.setEnabled(s == 2))
        self.ui.checkBoxHameau.stateChanged.connect(
            lambda s: self.ui.comboBoxHameau.setEnabled(s == 2))
        self.ui.checkBoxParcelle.stateChanged.connect(
            lambda s: self.ui.lineEditNumeroParcelle.setEnabled(s == 2))
        self.populateComboBoxes()
        self.ui.checkBoxCocherTous.stateChanged.connect(self.onCheckAllToggled)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercherDossiers)
        self.ui.pushButtonTransformerDemande.clicked.connect(self.enregistrerDemande)
        self.connect(self.ui.tableWidget_dossier,
                     QtCore.SIGNAL("itemClicked(QTableWidgetItem*)"),
                     self.onDossierItemClicked)

    def loadDataAfterShow(self):
        QtGui.QApplication.processEvents()
        self.progressBar.show()
        QtGui.QApplication.processEvents()
        self.showAllDossiers()
        self.progressBar.hide()

    def populateComboBoxes(self):
        try:
            cur = self.connection.cursor()
            for col, combo in [('fokontany', self.ui.comboBoxFokontany),
                               ('hameau', self.ui.comboBoxHameau)]:
                cur.execute("""
                    SELECT DISTINCT json_extract_path_text(d, 'localite', %s) AS val
                    FROM (
                        SELECT payload
                        FROM fiplof_raw_ingestion
                        WHERE payload IS NOT NULL
                    ) r,
                     json_array_elements(
                         COALESCE(json_try_parse(r.payload)->'demandes', '[]'::json)
                     ) d
                    WHERE json_extract_path_text(d, 'localite', %s) IS NOT NULL
                      AND json_extract_path_text(d, 'localite', %s) != ''
                    ORDER BY val
                """, (col, col, col))
                combo.clear()
                combo.addItem("")
                for row in cur:
                    combo.addItem(row[0])
            cur.close()
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Erreur population comboBoxes:", str(e))

    def _buildSearchQuery(self):
        conditions = [
            "r.statut IN ('DONE', 'PARTIAL_SUCCESS')",
            "(r.traitement_statut IS NULL OR r.traitement_statut != 'SUCCESS')",
            "json_extract_path(d, 'demande') IS NOT NULL",
            "json_extract_path(d, 'parcelle') IS NOT NULL",
            "json_extract_path_text(d, 'parcelle', 'code_parcelle') IS NOT NULL",
            "json_extract_path_text(d, 'parcelle', 'code_parcelle') != ''",
            "json_extract_path_text(d, 'localite', 'commune') IS NOT NULL",
            "json_extract_path_text(d, 'localite', 'commune') != ''",

        ]
        params = []

        if self.ui.checkBoxFkt.isChecked():
            v = str(self.ui.comboBoxFokontany.currentText())
            if v:
                conditions.append("json_extract_path_text(d, 'localite', 'fokontany') = %s")
                params.append(v)

        if self.ui.checkBoxHameau.isChecked():
            v = str(self.ui.comboBoxHameau.currentText())
            if v:
                conditions.append("json_extract_path_text(d, 'localite', 'hameau') = %s")
                params.append(v)

        if self.ui.checkBoxParcelle.isChecked():
            v = str(self.ui.lineEditNumeroParcelle.text()).strip()
            if v:
                conditions.append("json_extract_path_text(d, 'parcelle', 'code_parcelle') LIKE %s")
                params.append('%' + v + '%')

        if self.ui.groupBoxDemande.isChecked():
            d = self.ui.dateDemande.date()
            if d != self._initDateDemande:
                conditions.append("json_extract_path_text(d, 'demande', 'date_dmd') = %s")
                params.append(str(d.toString("yyyy-MM-dd")))

        if self.ui.groupBoxDecision.isChecked():
            v = str(self.ui.lineEditNumeroDecision.text()).strip()
            if v:
                conditions.append("json_extract_path_text(d, 'demande', 'num_decision') LIKE %s")
                params.append('%' + v + '%')
            d = self.ui.dateEditDateDecision.date()
            if d != self._initDateDecision:
                conditions.append("json_extract_path_text(d, 'demande', 'date_decision') = %s")
                params.append(str(d.toString("yyyy-MM-dd")))

        if self.ui.groupBoxAffichage.isChecked():
            d1 = self.ui.dateEditDebutAffichage.date()
            d2 = self.ui.dateEditFinAffichage.date()
            if d1 != self._initDateDebutAff:
                conditions.append("COALESCE(json_extract_path_text(d, 'demande', 'date_debut_aff'),'') >= %s")
                params.append(str(d1.toString("yyyy-MM-dd")))
            if d2 != self._initDateFinAff:
                conditions.append("COALESCE(json_extract_path_text(d, 'demande', 'date_fin_aff'),'') <= %s")
                params.append(str(d2.toString("yyyy-MM-dd")))

        if self.ui.groupBoxdateRL.isChecked():
            d = self.ui.dateEditRL.date()
            if d != self._initDateRL:
                conditions.append("json_extract_path_text(d, 'rl', 'date_rl') = %s")
                params.append(str(d.toString("yyyy-MM-dd")))

        base = """
            SELECT r.id, r.inbound_dossier_id,
                   json_extract_path_text(d, 'parcelle', 'code_parcelle') AS code_parcelle,
                   json_extract_path_text(d, 'parcelle', 'contenance') AS contenance,
                   json_extract_path_text(d, 'localite', 'fokontany') AS fokontany,
                   json_extract_path_text(d, 'localite', 'hameau') AS hameau,
                   json_extract_path_text(d, 'demande', 'date_dmd') AS date_dmd,
                   json_extract_path_text(d, 'demande', 'num_decision') AS num_decision,
                   json_extract_path_text(d, 'demande', 'date_decision') AS date_decision,
                   json_extract_path_text(d, 'demande', 'date_debut_aff') AS date_debut_aff,
                   json_extract_path_text(d, 'demande', 'date_fin_aff') AS date_fin_aff,
                   json_extract_path_text(d, 'rl', 'date_rl') AS date_rl,
                   json_extract_path_text(d, 'demande', 'duree_occupation') AS duree_occupation,
                   r.valid_parcelle, r.traitement_parcelle_valide
            FROM (
                SELECT id, inbound_dossier_id, payload,
                       statut, traitement_statut, created_at,
                       valid_parcelle, traitement_parcelle_valide
                FROM fiplof_raw_ingestion
                WHERE payload IS NOT NULL
            ) r,
                 json_array_elements(
                     COALESCE(json_try_parse(r.payload)->'demandes', '[]'::json)
                 ) d
            WHERE """
        return base + " AND ".join(conditions) + " ORDER BY r.created_at DESC", params

    def rechercherDossiers(self):
        QtGui.QApplication.processEvents()
        self.progressBar.show()
        self._setListModel(self.ui.listView_principale, [])
        self._setListModel(self.ui.listView_consors, [])
        self._setListModel(self.ui.listView_CRL, [])
        self._setListModel(self.ui.listView_coordonees, [])
        self.ui.tableWidget_dossier.setRowCount(0)
        QtGui.QApplication.processEvents()
        import time
        t_start = time.time()
        try:
            query, params = self._buildSearchQuery()
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            self.connection.commit()

            demandes = []
            for row in rows:
                code_parcelle = row.get('code_parcelle', '')
                valid_parcelle = row.get('valid_parcelle', '') or ''
                traitement_parcelle_valide = row.get('traitement_parcelle_valide', '') or ''

                # Filtrer comme dans BatchDemandeRun.showIngestionDetails
                if code_parcelle and valid_parcelle and code_parcelle not in valid_parcelle:
                    continue
                if traitement_parcelle_valide and code_parcelle in traitement_parcelle_valide:
                    continue

                demandes.append({
                    'code_parcelle': code_parcelle,
                    'contenance': row.get('contenance', ''),
                    'fokontany': row.get('fokontany', ''),
                    'hameau': row.get('hameau', ''),
                    'date_dmd': row.get('date_dmd', ''),
                    'num_decision': row.get('num_decision', ''),
                    'date_decision': row.get('date_decision', ''),
                    'date_debut_aff': row.get('date_debut_aff', ''),
                    'date_fin_aff': row.get('date_fin_aff', ''),
                    'date_rl': row.get('date_rl', ''),
                    'duree_occupation': row.get('duree_occupation', ''),
                    'batch': str(row['id']),
                })
            self.alimenterTableauDossier(demandes)
            print("Recherche: %.1fs | %d resultats" % (time.time() - t_start, len(demandes)))
        except Exception as e:
            self.connection.rollback()
            print("Erreur recherche:", str(e))
        finally:
            self.progressBar.hide()

    def showAllDossiers(self):
        self.rechercherDossiers()

    def onDossierItemClicked(self, item):
        row = item.row()
        self.ui.tableWidget_dossier.selectRow(row)
        self.loadDemandeursForRow(row)

    def _setListModel(self, listview, items):
        lw = QtGui.QListWidget()
        for t in items:
            lw.addItem(t)
        listview.setModel(lw.model())
        listview.update()
        self._models[id(listview)] = lw

    def loadDemandeursForRow(self, row):
        table = self.ui.tableWidget_dossier
        item_parcelle = table.item(row, 2)
        item_batch = table.item(row, 1)
        if not item_parcelle or not item_batch:
            return
        code_parcelle = str(item_parcelle.text() or '')
        batch_str = str(item_batch.text() or '')
        try:
            batch_id = int(batch_str)
        except ValueError:
            return
        try:
            cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT payload FROM fiplof_raw_ingestion WHERE id = %s", (batch_id,))
            row_payload = cur.fetchone()
            cur.close()
            if not row_payload:
                return
            payload = row_payload['payload']
            data = payload if isinstance(payload, dict) else json.loads(payload)
        except Exception as e:
            print("Erreur chargement payload:", str(e))
            return
        demande_item = None
        for d in data.get('demandes', []):
            pc = d.get('parcelle', {}).get('code_parcelle', '')
            if pc == code_parcelle:
                demande_item = d
                break
        if not demande_item:
            return
        principales = []
        consors = []
        for dmdr in demande_item.get('demandeurs', []):
            p = dmdr.get('personne', {})
            nom = "%s %s" % (p.get('prenom', ''), p.get('nom', ''))
            if dmdr.get('dmdr_principale', True):
                principales.append(nom.strip())
            else:
                consors.append(nom.strip())
        print("-> proprietaire:", principales, consors)
        self._setListModel(self.ui.listView_principale, principales)
        self._setListModel(self.ui.listView_consors, consors)
        rl = demande_item.get('rl', {})
        membres = []
        for m in rl.get('membres_crl', []):
            p = m.get('personne', m)
            role = m.get('role', '')
            prenom = p.get('prenom', '')
            nom = p.get('nom', '')
            ligne = ("%s: %s %s" % (role, prenom, nom)).strip(": ")
            membres.append(ligne)
        print("-> CRL:", membres)
        self._setListModel(self.ui.listView_CRL, membres)
        geom = demande_item.get('parcelle', {}).get('geometry', {})
        coords = []
        if geom and 'coordinates' in geom:
            coords_list = geom['coordinates']
            if isinstance(coords_list[0], (list, tuple)):
                for pt in coords_list:
                    if isinstance(pt[0], (list, tuple)):
                        for p in pt:
                            coords.append("%s, %s" % (p[0], p[1]))
                    else:
                        coords.append("%s, %s" % (pt[0], pt[1]))
            else:
                coords.append("%s, %s" % (coords_list[0], coords_list[1]))
        print("-> coords:", coords)
        self._setListModel(self.ui.listView_coordonees, coords)

    def alimenterTableauDossier(self, demandes_found):
        n = len(demandes_found)
        table = self.ui.tableWidget_dossier
        table.setUpdatesEnabled(False)
        table.setColumnCount(13)
        table.setRowCount(n)

        # Sélection de ligne entière
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        # Style pour la ligne sélectionnée
        table.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #B8D4E8;
                color: black;
            }
        """)

        # En-têtes
        headers = [u"", u"Batch", u"Parcelle", u"Contenance", u"Fokontany", u"Hameau",
                   u"Date Dmd", u"N\u00b0 D\u00e9cision", u"Date D\u00e9cision",
                   u"D\u00e9but Aff", u"Fin Aff", u"Date RL", u"Occupation"]
        for i, h in enumerate(headers):
            item = table.horizontalHeaderItem(i)
            if item:
                item.setText(h)
            else:
                table.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(h))

        # Largeurs de colonnes fixes
        largeurs = {
            0: 50,   # Checkbox
            1: 140,  # Batch
            2: 180,  # Parcelle
            3: 90,   # Contenance
            4: 140,  # Fokontany
            5: 140,  # Hameau
            6: 120,  # Date demande
            7: 130,  # Numéo décision
            8: 120,  # Date décision
            9: 120,  # Date début affichage
            10: 120, # Date fin affichage
            11: 120, # Date RL
            12: 110, # Occupation
        }
        for col, larg in largeurs.items():
            table.setColumnWidth(col, larg)

        for row, demande in enumerate(demandes_found):
            # Checkbox
            checkbox = QtGui.QCheckBox()
            checkbox.stateChanged.connect(
                lambda state, r=row: self.onCheckboxDossierClicked(state, r))
            widget = QtGui.QWidget()
            layout = QtGui.QHBoxLayout(widget)
            layout.addWidget(checkbox)
            layout.setAlignment(QtCore.Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(row, 0, widget)

            # Données
            table.setItem(row, 1, QtGui.QTableWidgetItem(str(demande.get('batch', ''))))
            table.setItem(row, 2, QtGui.QTableWidgetItem(str(demande.get('code_parcelle', ''))))
            table.setItem(row, 3, QtGui.QTableWidgetItem(str(demande.get('contenance', ''))))
            table.setItem(row, 4, QtGui.QTableWidgetItem(str(demande.get('fokontany', ''))))
            table.setItem(row, 5, QtGui.QTableWidgetItem(str(demande.get('hameau', ''))))
            table.setItem(row, 6, QtGui.QTableWidgetItem(str(demande.get('date_dmd', ''))))
            table.setItem(row, 7, QtGui.QTableWidgetItem(str(demande.get('num_decision', ''))))
            table.setItem(row, 8, QtGui.QTableWidgetItem(str(demande.get('date_decision', ''))))
            table.setItem(row, 9, QtGui.QTableWidgetItem(str(demande.get('date_debut_aff', ''))))
            table.setItem(row, 10, QtGui.QTableWidgetItem(str(demande.get('date_fin_aff', ''))))
            table.setItem(row, 11, QtGui.QTableWidgetItem(str(demande.get('date_rl', ''))))
            table.setItem(row, 12, QtGui.QTableWidgetItem(str(demande.get('duree_occupation', ''))))

        table.setUpdatesEnabled(True)
        table.repaint()

    def onCheckboxDossierClicked(self, state, current_row):
        self.ui.tableWidget_dossier.selectRow(current_row)

    def onCheckAllToggled(self, state):
        table = self.ui.tableWidget_dossier
        any_checked = any(
            table.cellWidget(row, 0).findChild(QtGui.QCheckBox).isChecked()
            for row in range(table.rowCount())
            if table.cellWidget(row, 0)
        )
        new_state = not any_checked
        for row in range(table.rowCount()):
            w = table.cellWidget(row, 0)
            if w:
                cb = w.findChild(QtGui.QCheckBox)
                if cb:
                    cb.blockSignals(True)
                    cb.setChecked(new_state)
                    cb.blockSignals(False)


    def enregistrerDemande(self):
        QtGui.QApplication.processEvents()
        self.progressBar.show()
        QtGui.QApplication.processEvents()
        try:
            checked = []
            for row in range(self.ui.tableWidget_dossier.rowCount()):
                w = self.ui.tableWidget_dossier.cellWidget(row, 0)
                if w and w.findChild(QtGui.QCheckBox) and w.findChild(QtGui.QCheckBox).isChecked():
                    batch_item = self.ui.tableWidget_dossier.item(row, 1)
                    parcelle_item = self.ui.tableWidget_dossier.item(row, 2)
                    if batch_item and parcelle_item:
                        checked.append((batch_item.text(), parcelle_item.text()))

            if not checked:
                QtGui.QMessageBox.warning(self, u"Attention", u"Veuillez cocher au moins une demande.")
                return

            # Grouper par batch_id
            par_batch = {}
            for batch_id, code_parcelle in checked:
                par_batch.setdefault(batch_id, []).append(code_parcelle)

            total_ok, total_err = 0, 0
            traite_ok = []
            for batch_id, codes in par_batch.items():
                try:
                    bid = int(batch_id)
                except ValueError:
                    for c in codes:
                        print(u"Batch invalide:", batch_id, u"pour", c)
                        total_err += 1
                    continue

                model = FiplofIngestionModel()
                model.setConnection(self.connection)
                ingestions = model.getIngestionsWithPayload(bid)
                if not ingestions:
                    for c in codes:
                        print(u"Batch introuvable:", bid, u"pour", c)
                        total_err += 1
                    continue

                payload = ingestions[0].get('payload', {})
                if isinstance(payload, basestring):
                    try:
                        payload = json.loads(payload)
                    except:
                        payload = {}
                demandes = payload.get('demandes', [])
                if not demandes:
                    for c in codes:
                        print(u"Aucune demande dans le batch", bid, u"pour", c)
                        total_err += 1
                    continue

                # Récupérer les codes valides et déjà traités pour ce batch
                valid_parcelle = ingestions[0].get('valid_parcelle', '') or ''
                codes_valides = []
                if valid_parcelle and valid_parcelle != '[]':
                    try:
                        codes_valides = json.loads(valid_parcelle)
                        if isinstance(codes_valides, basestring):
                            codes_valides = [codes_valides]
                    except:
                        codes_valides = []

                traitement_existant = ingestions[0].get('traitement_parcelle_valide', '') or ''
                codes_deja_traites = []
                if traitement_existant and traitement_existant != '[]':
                    try:
                        codes_deja_traites = json.loads(traitement_existant)
                        if isinstance(codes_deja_traites, basestring):
                            codes_deja_traites = [codes_deja_traites]
                    except:
                        codes_deja_traites = []

                batch_ok = []
                for item in demandes:
                    parcelle = item.get('parcelle', {})
                    code = parcelle.get('code_parcelle', '')
                    if code in codes and code not in codes_deja_traites:
                        try:
                            ok = self._traiterDemande(item, bid)
                            if ok:
                                total_ok += 1
                                traite_ok.append((batch_id, code))
                                batch_ok.append(code)
                            else:
                                total_err += 1
                        except Exception as e:
                            print(u"Erreur parcelle", code, ":", str(e))
                            total_err += 1

                if batch_ok:
                    tous_codes = codes_deja_traites + batch_ok
                    valide_json = json.dumps(tous_codes)
                    # SUCCESS seulement si toutes les parcelles valides sont traitées
                    tout_traite = set(tous_codes) >= set(codes_valides)
                    statut = "SUCCESS" if tout_traite else "PARTIAL_SUCCESS"
                    FiplofIngestionModel.updateTraitementStatut(
                        self.connection, bid, statut, valide_json, json.dumps([])
                    )
                    self.connection.commit()

            if not traite_ok:
                self.connection.rollback()

            if total_ok:
                table = self.ui.tableWidget_dossier
                for row in range(table.rowCount() - 1, -1, -1):
                    w = table.cellWidget(row, 0)
                    if w and w.findChild(QtGui.QCheckBox) and w.findChild(QtGui.QCheckBox).isChecked():
                        b = table.item(row, 1)
                        p = table.item(row, 2)
                        if b and p and (b.text(), p.text()) in traite_ok:
                            table.removeRow(row)

            msg = u"Traitement termine\nReussies: %d\nEchecs: %d" % (total_ok, total_err)
            if total_err:
                QtGui.QMessageBox.warning(self, u"Resultat", msg)
            else:
                QtGui.QMessageBox.information(self, u"Succes", msg)
        except Exception as e:
            print("Erreur enregistrerDemande:", str(e))
            self.connection.rollback()
        finally:
            self.progressBar.hide()

    def _traiterDemande(self, item, batch_id):
        """Traite une demande issue du JSON et insere dans les tables metier"""
        try:
            demande = item.get("demande") or {}
            parcelle = item.get('parcelle', {})
            localite = item.get('localite', {})
            rl = item.get("rl") or {}

            code_parcelle = parcelle.get('code_parcelle', '')
            geometry = parcelle.get('geometry', {})
            geom_hex = self.geojson_to_wkb_hex(geometry)
            if not geom_hex:
                print("Geometrie invalide pour", code_parcelle)
                return False

            region = localite.get("region", "").upper() if localite.get("region") else ""
            district = localite.get("district", "").strip().upper()
            commune = localite.get("commune", "").upper() if localite.get("commune") else ""
            fokontany = localite.get("fokontany", "").upper() if localite.get("fokontany") else ""
            hameau = localite.get("hameau", "").upper() if localite.get("hameau") else ""

            commune_obj = Commune.findByName(self.connection, commune)
            fokontany_obj = Fokontany.findByName(self.connection, fokontany)
            hameau_obj = Hameau.findByName(self.connection, hameau)
            district_obj = District.getByName(self.connection, district)
            if not district_obj or not hasattr(district_obj, 'codedistrict') or not district_obj.codedistrict:
                print(u"District invalide pour", code_parcelle)
                return False

            categorie = demande.get("categorie") or ""
            consistance = demande.get("consistance") or ""
            id_parcelle = Parcelled.insert_parcelle_d_by_interrop(self.connection, {
                "parcelle": code_parcelle,
                "geom": geom_hex,
                "consistance": consistance,
                "region": region,
                "district": district,
                "commune": commune,
                "id_commune": commune_obj.idcommune if commune_obj else None,
                "fkt": fokontany,
                "id_hameau": hameau_obj.idhameau if hameau_obj else None,
                "categorie": categorie,
            })
            if not id_parcelle:
                print("Echec insertion parcelle", code_parcelle)
                return False

            id_projet = Projet.getFirstProjetId(self.connection)
            if not id_projet:
                return False

            date_dmd = demande.get("date_dmd") or None
            num_decision = demande.get("num_decision") or ""
            date_decision = demande.get("date_decision") or None
            date_debut_aff = demande.get("date_debut_aff") or None
            date_fin_aff = demande.get("date_fin_aff") or None
            duree_occupation = demande.get("duree_occupation") or 0
            origine = demande.get("origine") or ""

            code_district = district_obj.codedistrict
            num_demande = Demande.creationNum(self.connection, code_district, commune)

            date_rl = rl.get("date_rl", "")
            avis_crl = rl.get("avis_crl", False)
            obs_crl = rl.get("obs_crl", "")

            id_demande = Demande.insert(self.connection, {
                "numdemande": num_demande,
                "gid": id_parcelle,
                "datedemande": date_dmd,
                "datedecision": date_decision,
                "numdecision": num_decision,
                "datereconnaissance": date_rl,
                "region": region,
                "district": district,
                "commune": commune,
                "fokontany": fokontany,
                "idfokontany": fokontany_obj.idfokontany if fokontany_obj else None,
                "idcommune": commune_obj.idcommune if commune_obj else None,
                "consistance": consistance,
                "idprojet": id_projet,
                "code_parcelle": code_parcelle,
                "categorie": categorie,
                "debut_affichage": date_debut_aff,
                "fin_affichage": date_fin_aff,
                "origine": origine,
                "duree_occupation": duree_occupation,
                "avis_crl": avis_crl,
                "texte_crl": obs_crl,
            })
            if not id_demande:
                return False

            Demande.incrementCptDemande(self.connection, commune)
            Parcelled.updateNumDemande(self.connection, id_parcelle, num_demande)

            for d in item.get("demandeurs") or []:
                personne = d.get("personne") or {}
                smat = personne.get("situation_matrimoniale", 0)
                sm = self.map_situation_matrimoniale(smat)
                p = Personne()
                p.nompersonne = personne.get("nom", "")
                p.prenompersonne = personne.get("prenom", "")
                p.sexepersonne = personne.get("sexe", "")
                p.datenaissancepersonne = personne.get("date_naissance")
                p.lieunaissancepersonne = personne.get("lieu_naissance", "")
                p.nevers = personne.get("ne_vers")
                p.numactenaissancepersonne = personne.get("num_acte_naissance", "")
                p.dateactenaissancepersonne = personne.get("date_acte_naissance")
                p.numcipersonne = personne.get("cin", "")
                p.datecipersonne = personne.get("date_cin")
                p.lieucipersonne = personne.get("lieu_cin", "")
                p.nompere = personne.get("nompere", "")
                p.nommere = personne.get("nommere", "")
                p.situationmatrimoniale = sm
                p.adressepersonne = personne.get("adresse", "")
                id_personne = Personne.insert(self.connection, p)
                if id_personne:
                    avoir = AvoirDemande()
                    avoir.idpersonne = id_personne
                    avoir.iddemande = id_demande
                    avoir.idparcelle = id_parcelle
                    avoir.representant = d.get("dmdr_principale", True)
                    AvoirDemande.insert(self.connection, avoir)
                    photos = personne.get("photos") or []
                    liste_photos = [{"type": ph.get("type", ""), "base64": ph.get("base64", "")} for ph in photos]
                    BlobPersonne.insertPhotos(self.connection, id_personne, liste_photos)

            for v in item.get("voisins") or []:
                repere = v.get("repere", "")
                description = v.get("description", "")
                pc = Pointscardinaux.findByPosition(self.connection, repere)
                if pc:
                    lp = Limiteparcelle()
                    lp.idpointscardinaux = pc.idpointscardinaux
                    lp.idparcelle = id_parcelle
                    lp.description = description
                    lp.path_file = None
                    Limiteparcelle.insert(self.connection, lp)

            # CRL members
            rl = item.get("rl") or {}
            for m in rl.get("membres_crl") or []:
                try:
                    pdata = m.get("personne", m)
                    role_lib = m.get("role", "")
                    is_titulaire = m.get("titulaire", True)
                    is_president = m.get("president", False)
                    if not role_lib:
                        continue
                    role_crl_model = RoleCrl(self.connection)
                    role = role_crl_model.find_or_create_by_lib(role_lib)
                    if not role:
                        print(u"Role CRL '%s' introuvable et creation echouee" % role_lib)
                        continue
                    p = Personne()
                    p.nompersonne = pdata.get("nom", "")
                    p.prenompersonne = pdata.get("prenom", "")
                    p.sexepersonne = pdata.get("sexe", "")
                    p.datenaissancepersonne = pdata.get("date_naissance")
                    p.lieunaissancepersonne = pdata.get("lieu_naissance", "")
                    p.nevers = pdata.get("ne_vers")
                    p.numactenaissancepersonne = pdata.get("num_acte_naissance", "")
                    p.dateactenaissancepersonne = pdata.get("date_acte_naissance")
                    p.numcipersonne = pdata.get("cin", "")
                    p.datecipersonne = pdata.get("date_cin")
                    p.lieucipersonne = pdata.get("lieu_cin", "")
                    p.nompere = pdata.get("nompere", "")
                    p.nommere = pdata.get("nommere", "")
                    p.situationmatrimoniale = 0
                    p.adressepersonne = pdata.get("adresse", "")
                    id_personne = Personne.insert(self.connection, p)
                    if not id_personne:
                        continue
                    data = [id_demande, int(role[0]), id_personne, is_titulaire, is_president]
                    role_crl_model.insert_role(data)
                except Exception as e:
                    print(u"Erreur insertion CRL: %s" % str(e))

            return True
        except Exception as e:
            print(u"Erreur _traiterDemande:", str(e))
            return False


    def validerDemande(self):

        try:

            # =====================================================
            # RECUPERER ID BATCH SELECTIONNE
            # =====================================================

            print('DEBUG : DEBUT RECUP2RATION BATCH')

            selected_rows = self.ui.tableWidgetBath.selectionModel().selectedRows()

            if not selected_rows:

                QtGui.QMessageBox.warning(
                    self,
                    "Attention",
                    "Veuillez sélectionner un batch."
                )
                return

            row_batch = selected_rows[0].row()

            # colonne 1 = ID
            item_id = self.ui.tableWidgetBath.item(row_batch, 1)

            if not item_id:

                QtGui.QMessageBox.warning(
                    self,
                    "Attention",
                    "ID batch introuvable."
                )
                return

            batch_id = item_id.text()

            print("BATCH ID =", batch_id)

            # =====================================================
            # RECUPERER CODE PARCELLE
            # =====================================================

            if not batch_id:

                QtGui.QMessageBox.warning(
                    self,
                    "Attention",
                    "Veuillez sélectionner un batch."
                )
                return

            liste_parcelles = []

            table = self.ui.tableWidgetDemande

            for row in range(table.rowCount()):

                # Checkbox colonne 0
                checkbox = table.cellWidget(row, 0)

                if checkbox and checkbox.isChecked():

                    # colonne 1 = code parcelle
                    item_code = table.item(row, 1)

                    if item_code:

                        code_parcelle = item_code.text()

                        liste_parcelles.append(code_parcelle)

            # =====================================================
            # VERIFICATION
            # =====================================================

            if not liste_parcelles:

                QtGui.QMessageBox.warning(
                    self,
                    "Attention",
                    "Veuillez cocher au moins une demande."
                )
                return

            # =====================================================
            # AFFICHAGE TEST
            # =====================================================

            print("Batch sélectionné :", batch_id)

            print("Parcelles sélectionnées :")

            for code in liste_parcelles:

                print(code)

            # =====================================================
            # ICI TRAITEMENT / INSERTION
            # =====================================================

            # exemple :
            # model.validerDemandes(batch_id, liste_parcelles)

            QtGui.QMessageBox.information(
                self,
                "Succès",
                "Validation effectuée."
            )

        except Exception as e:

            print("Erreur validation :", str(e))   
   
   
    def onCheckboxClicked(self, state, current_row):

        if state == QtCore.Qt.Checked:

            for i, checkbox in enumerate(self.batch_checkboxes):

                if i != current_row:

                    checkbox.blockSignals(True)
                    checkbox.setChecked(False)
                    checkbox.blockSignals(False)

        # Sélectionner la ligne cochée
        self.ui.tableWidgetBath.selectRow(current_row)

    def count_list_text(self, value):
        try:
            if isinstance(value, basestring):
                value = ast.literal_eval(value)

            return len(value) if isinstance(value, list) else 0

        except:
            return 0    
            
    def validerDemandes(self):
        print("+++++++++++++++++++++++++++++++++++++++s :")
        """Traite le batch des demandes sélectionnées dans tableWidgetDemande"""
        erreurs = []
        traitement_statut = ""
        traitement_parcelle_valide = []
        traitement_parcelle_refuse = []
        
        try:
            # Récupérer les demandes sélectionnées depuis tableWidgetDemande
            try:
                selected_demandes = self.getSelectedDemandes()
                
                if not selected_demandes:
                    QtGui.QMessageBox.warning(self, "Attention", u"Veuillez sélectionner au moins une demande dans le tableau")
                    return
                codes_parcelles = [d['code_parcelle'] for d in selected_demandes]
                print("DEBUG: Codes parcelles :", codes_parcelles)
            except Exception as e:
                erreur_msg = "Erreur lors de la récupération des demandes sélectionnées : " + str(e)
                erreurs.append(erreur_msg)
                print(erreur_msg)
                QtGui.QMessageBox.warning(self, "Erreur", erreur_msg)
                return

            # Récupérer le batch concerné depuis tableWidgetBath
            try:
                selected_batch = self.ui.tableWidgetBath.selectionModel().selectedRows()
                if not selected_batch:
                    QtGui.QMessageBox.warning(
                        self,
                        "Attention",
                        "Veuillez sélectionner un batch."
                    )
                    return
      
                row_batch = selected_batch[0].row()
                item_id = self.ui.tableWidgetBath.item(row_batch, 1)
                
                if not item_id:
                    erreur_msg = "Impossible de récupérer l'ID du batch sélectionné"
                    erreurs.append(erreur_msg)
                    print(erreur_msg)
                    QtGui.QMessageBox.warning(self, "Erreur", erreur_msg)
                    return
                    
                try:
                    batch_id = int(item_id.text())
                except ValueError:
                    erreur_msg = "L'ID du batch n'est pas un nombre valide : " + item_id.text()
                    erreurs.append(erreur_msg)
                    print(erreur_msg)
                    QtGui.QMessageBox.warning(self, "Erreur", erreur_msg)
                    return
                    
                print("DEBUG: batch_id :", batch_id)   
                print("DEBUG: codes_parcelles :", codes_parcelles)  
            except Exception as e:
                erreur_msg = "Erreur lors de la récupération du batch sélectionné : " + str(e)
                erreurs.append(erreur_msg)
                print(erreur_msg)
                QtGui.QMessageBox.warning(self, "Erreur", erreur_msg)
                return
                          
            success_count = 0
            model = FiplofIngestionModel()
            model.setConnection(self.connection)
            
            try:
                print("DEBUG: avant getIngestionsWithPayload :", batch_id)  
                ingestions = model.getIngestionsWithPayload(batch_id)           

                if not ingestions:
                    erreur_msg = "Batch ID " + str(batch_id) + " introuvable dans la base de données"
                    erreurs.append(erreur_msg)
                    print(erreur_msg)
                    QtGui.QMessageBox.warning(self, "Erreur", erreur_msg)
                    return
            except Exception as e:
                erreur_msg = "Erreur lors de la récupération des ingestions (batch_id: " + str(batch_id) + ") : " + str(e)
                erreurs.append(erreur_msg)
                print(erreur_msg)
                QtGui.QMessageBox.warning(self, "Erreur", erreur_msg)
                return

            # Premier résultat
            ingestion = ingestions[0]
            payload = ingestion.get('payload', {})

            try:
                if isinstance(payload, str):
                    payload = json.loads(payload)
            except Exception as e:
                erreur_msg = "Erreur lors du parsing du JSON payload (batch_id: " + str(batch_id) + ") : " + str(e)
                erreurs.append(erreur_msg)
                print(erreur_msg)
                payload = {}

            # Liste des demandes
            demandes = payload.get('demandes', [])

            print("DEBUG: Nombre demandes :", len(demandes))
            
            if not demandes:
                erreur_msg = "Aucune demande trouvée dans le payload du batch " + str(batch_id)
                erreurs.append(erreur_msg)
                print(erreur_msg)
            
            # =========================
            # Recherche des parcelles sélectionnées
            # =========================
            for code_parcelle in codes_parcelles:
                demande_trouvee = None
                erreur_parcelle = None
                
                try:
                    # Recherche de la demande correspondant au code_parcelle
                    for item in demandes:  
                        parcelle = item.get('parcelle', {})
                        if parcelle.get('code_parcelle') == code_parcelle:
                            demande_trouvee = item
                            break
                    
                    if not demande_trouvee:
                        erreur_msg = "Parcelle '" + code_parcelle + "' non trouvée dans les demandes du batch " + str(batch_id)
                        erreurs.append(erreur_msg)
                        traitement_parcelle_refuse.append(code_parcelle)
                        print(erreur_msg)
                        continue
                        
                    print("Demande trouvée pour " + code_parcelle)

                    # DEMANDE INFORMATIONS
                    print("DEBUG : DEMANDE INFORMATIONS ")
                    demande = demande_trouvee.get("demande") or {}
                    date_dmd = demande.get("date_dmd") or None
                    num_decision = demande.get("num_decision") or ""
                    date_decision = demande.get("date_decision") or None
                    date_debut_aff = demande.get("date_debut_aff") or None
                    date_fin_aff = demande.get("date_fin_aff") or None
                    categorie = demande.get("categorie") or ""
                    consistance = demande.get("consistance") or ""
                    duree_occupation = demande.get("duree_occupation") or 0
                    origine = demande.get("origine") or ""

                    # Recuperation parcelle
                    print("DEBUG : Recuperation parcelle ")
                    parcelle = demande_trouvee.get('parcelle', {})
                    parcelle_code = parcelle.get('code_parcelle','')
                    contenance = parcelle.get('contenance','')
                    geometry = parcelle.get('geometry',{})
                    
                    try:
                        geom_hex = self.geojson_to_wkb_hex(geometry)
                        print("DEBUG : geom_hex ")
                        print(geom_hex)                       
                        print("DEBUG : FINgeom_hex ")
                    except Exception as e:
                        erreur_msg = "Erreur lors de la conversion de la géométrie pour parcelle '" + code_parcelle + "' : " + str(e)
                        erreurs.append(erreur_msg)
                        traitement_parcelle_refuse.append(code_parcelle)
                        print(erreur_msg)
                        continue

                    #----------------------------------------------------------------------------------------
                    # LOCALITE
                    #---------------------------------------------------------------------------------------
                    print("DEBUG : LOCALITE ")
                    localite = demande_trouvee.get('localite', {})
                    region = localite.get("region", "").upper() if localite.get("region") else ""
                    district = localite.get("district", "")
                    district = district.strip().upper()
                    commune = localite.get("commune", "").upper() if localite.get("commune") else ""
                    fokontany = localite.get("fokontany", "").upper() if localite.get("fokontany") else ""
                    hameau = localite.get("hameau", "").upper() if localite.get("hameau") else ""
                    print("DEBUG :district", district)
                    
                    try:
                        print("DEBUG : Recherche district avec valeur :", district)
                        commune_obj = Commune.findByName(self.connection, commune)
                        fokontany_obj = Fokontany.findByName(self.connection, fokontany)
                        hameau_obj = Hameau.findByName(self.connection, hameau)
                        district_obj = District.getByName(self.connection, district)

                        print("COMMUNE :", commune_obj)
                        print("FOKONTANY :", fokontany_obj)
                        print("HAMEAU :", hameau_obj)
                        print("DISTRICT :", district_obj)
                        print("DEBUG : district_obj.codedistrict :", district_obj.codedistrict if district_obj else None)
                        
                        if not district_obj:
                            erreur_msg = "District '" + district + "' non trouvé dans la base de données pour parcelle '" + code_parcelle + "'"
                            erreurs.append(erreur_msg)
                            traitement_parcelle_refuse.append(code_parcelle)
                            print(erreur_msg)
                            continue
                            
                        if not hasattr(district_obj, 'codedistrict') or not district_obj.codedistrict:
                            erreur_msg = "District '" + district + "' trouvé mais sans code_district valide pour parcelle '" + code_parcelle + "'"
                            erreurs.append(erreur_msg)
                            traitement_parcelle_refuse.append(code_parcelle)
                            print(erreur_msg)
                            continue
                    except Exception as e:
                        erreur_msg = "Erreur lors de la recherche des localités pour parcelle '" + code_parcelle + "' (commune: " + commune + ", district: " + district + ") : " + str(e)
                        erreurs.append(erreur_msg)
                        traitement_parcelle_refuse.append(code_parcelle)
                        print(erreur_msg)
                        continue

                    # RL
                    rl = item.get("rl") or {}
                    date_rl = rl.get("date_rl", "")
                    avis_crl = rl.get("avis_crl", False)
                    obs_crl = rl.get("obs_crl", "")
                    membres = rl.get("membres_crl") or []

                    #----------------------------------------------------------------------------------------
                    # DEBUT INSERTION PARCELLE
                    #----------------------------------------------------------------------------------------  
                    try:
                        id_parcelle = Parcelled.insert_parcelle_d_by_interrop(self.connection, {
                            "parcelle": parcelle_code,
                            "geom": geom_hex,
                            "consistance": consistance,
                            "region": region,
                            "district": district,
                            "commune": commune,
                            "id_commune": commune_obj.idcommune if commune_obj else None,
                            "fkt": fokontany,
                            "id_hameau": hameau_obj.idhameau if hameau_obj else None,
                            "categorie": categorie
                        })
                        print("DEBUG: PARCELLE ID")
                        print(id_parcelle)
                        print("DEBUG : FIN LOCALITE ")
                    except Exception as e:
                        erreur_msg = "Erreur lors de l'insertion de la parcelle '" + code_parcelle + "' : " + str(e)
                        erreurs.append(erreur_msg)
                        traitement_parcelle_refuse.append(code_parcelle)
                        print(erreur_msg)
                        continue
                    #----------------------------------------------------------------------------------------
                    # FIN INSERTION PARCELLE
                    #----------------------------------------------------------------------------------------
                    
                    #----------------------------------------------------------------------------------------
                    # DEBUT INSERTION DEMANDE
                    #----------------------------------------------------------------------------------------  
                    try:
                        print("id_projet a vérifier:")
                        id_projet = Projet.getFirstProjetId(self.connection)
                        print("id_projet :", id_projet)
                        
                        if not id_projet:
                            erreur_msg = "Impossible de récupérer l'ID du projet pour parcelle '" + code_parcelle + "'"
                            erreurs.append(erreur_msg)
                            traitement_parcelle_refuse.append(code_parcelle)
                            print(erreur_msg)
                            continue
                            
                        print("codedistrict a vérifier:")
                        print("DEBUG : district_obj :", district_obj)
                        print("DEBUG : type(district_obj) :", type(district_obj))
                        print("DEBUG : dir(district_obj) :", dir(district_obj))
                        if hasattr(district_obj, 'codedistrict'):
                            print("DEBUG : district_obj.codedistrict :", district_obj.codedistrict)
                        else:
                            print("DEBUG : district_obj n'a pas d'attribut codedistrict")
                        code_district = district_obj.codedistrict if district_obj else None
                        print("code_district :", code_district)                        
                        commune = commune.strip().upper()
                        
                        try:
                            num_demande = Demande.creationNum(self.connection, code_district, commune)
                            print("num_demande+++++++++++++++++++++++ :", num_demande)  
                        except Exception as e:
                            erreur_msg = "Erreur lors de la création du numéro de demande pour parcelle '" + code_parcelle + "' (district: " + str(code_district) + ", commune: " + commune + ") : " + str(e)
                            erreurs.append(erreur_msg)
                            traitement_parcelle_refuse.append(code_parcelle)
                            print(erreur_msg)
                            continue
                            
                        id_demande = Demande.insert(self.connection, {
                            "numdemande": num_demande,
                            "gid": id_parcelle,
                            "datedemande": date_dmd,
                            "datedecision": date_decision,
                            "numdecision": num_decision,
                            "datereconnaissance": date_rl,
                            "region": region,
                            "district": district,
                            "commune": commune,
                            "fokontany": fokontany,
                            "idfokontany": fokontany_obj.idfokontany if fokontany_obj else None,
                            "idcommune": commune_obj.idcommune if commune_obj else None,
                            "consistance": consistance,
                            "idprojet": id_projet,
                            "code_parcelle": parcelle_code,
                            "categorie": categorie,
                            "debut_affichage": date_debut_aff,
                            "fin_affichage": date_fin_aff,
                            "origine": origine,
                            "duree_occupation": duree_occupation,
                            "avis_crl": avis_crl,
                            "texte_crl": obs_crl,
                        })
                        print('DEBUG :FINdemande_a_insere')
                        print(id_demande)        
                        
                        if id_demande:
                            print('DEBUG :DEBUT incrementCptDemande')
                            Demande.incrementCptDemande(self.connection, commune)
                            print('DEBUG :FIN incrementCptDemande')
                            print('DEBUG :DEBUT mise a jour dum dedmande dans parcelle')
                            Parcelled.updateNumDemande(self.connection, id_parcelle, num_demande)
                            print('DEBUG :FIN mise a jour du dedmande dans parcelle')
                        else:
                            erreur_msg = "L'insertion de la demande a retourné None pour parcelle '" + code_parcelle + "'"
                            erreurs.append(erreur_msg)
                            traitement_parcelle_refuse.append(code_parcelle)
                            print(erreur_msg)
                            continue
                    except Exception as e:
                        erreur_msg = "Erreur lors de l'insertion de la demande pour parcelle '" + code_parcelle + "' : " + str(e)
                        erreurs.append(erreur_msg)
                        traitement_parcelle_refuse.append(code_parcelle)
                        print(erreur_msg)
                        continue

                    #----------------------------------------------------------------------------------------
                    # FIN INSERTION DEMANDE
                    #---------------------------------------------------------------------------------------- 
                    
                    #----------------------------------------------------------------------------------------
                    # DEBUT PERSONNE
                    #----------------------------------------------------------------------------------------                        
                    print("DEBUG : DEMANDEURS ")
                    demandeurs = item.get("demandeurs") or []
                    
                    for idx, d in enumerate(demandeurs):
                        try:
                            personne = d.get("personne") or {}
                            demandeur_principale = d.get("dmdr_principale", True)
                            photos = personne.get("photos") or []
                            liste_photos = []
                            for p in photos:
                                liste_photos.append({
                                    "type": p.get("type", ""),
                                    "base64": p.get("base64", "")
                                })
                            
                            print("DEBUG : DEBUT INSERTION PERSONNE")
                            smat = personne.get("situation_matrimoniale", 0)
                            sm = self.map_situation_matrimoniale(smat)

                            personne_obj = Personne()
                            personne_obj.nompersonne = personne.get("nom", "")
                            personne_obj.prenompersonne = personne.get("prenom", "")
                            personne_obj.sexepersonne = personne.get("sexe", "")
                            personne_obj.datenaissancepersonne = personne.get("date_naissance")
                            personne_obj.lieunaissancepersonne = personne.get("lieu_naissance", "")
                            personne_obj.nevers = personne.get("ne_vers")
                            personne_obj.numactenaissancepersonne = personne.get("num_acte_naissance", "")
                            personne_obj.dateactenaissancepersonne = personne.get("date_acte_naissance")
                            personne_obj.numcipersonne = personne.get("cin", "")
                            personne_obj.datecipersonne = personne.get("date_cin")
                            personne_obj.lieucipersonne = personne.get("lieu_cin", "")
                            personne_obj.nompere = personne.get("nompere", "")
                            personne_obj.nommere = personne.get("nommere", "")
                            personne_obj.situationmatrimoniale = sm
                            personne_obj.adressepersonne = personne.get("adresse", "")
                            
                            id_personne = Personne.insert(self.connection, personne_obj)

                            print("FIN : INSERT DEMANDEUR", id_personne)
                            
                            if not id_personne:
                                erreur_msg = "L'insertion de la personne " + str(idx + 1) + " a échoué pour parcelle '" + code_parcelle + "'"
                                erreurs.append(erreur_msg)
                                print(erreur_msg)
                                continue
                                
                            print("DEBUG : AVOIR DEBUT DEMANDE")
                            avoir = AvoirDemande()
                            avoir.idpersonne = id_personne
                            avoir.iddemande = id_demande
                            avoir.idparcelle = id_parcelle
                            avoir.representant = demandeur_principale

                            bool_avoir = AvoirDemande.insert(self.connection, avoir)
                            print("DEBUG : AVOIR FIN DEMANDE", bool_avoir)

                            # blob personne
                            print("DEBUG : BLOB PERSONNE DEBUT")
                            id_blob_personne = BlobPersonne.insertPhotos(self.connection, id_personne, liste_photos)
                            print("DEBUG : BLOB PERSONNE FIN", id_blob_personne)
                        except Exception as e:
                            erreur_msg = "Erreur lors de l'insertion du demandeur " + str(idx + 1) + " pour parcelle '" + code_parcelle + "' : " + str(e)
                            erreurs.append(erreur_msg)
                            print(erreur_msg)
                            continue
                    #----------------------------------------------------------------------------------------
                    # FIN DEMANDEURS
                    #---------------------------------------------------------------------------------------- 

                    #----------------------------------------------------------------------------------------
                    # DEBUT VOISINS
                    #---------------------------------------------------------------------------------------- 
                    voisins = item.get("voisins") or []
                    for idx, v in enumerate(voisins):
                        try:
                            repere = v.get("repere", "")
                            description = v.get("description", "")
                            point_cardinal = Pointscardinaux.findByPosition(self.connection, repere)
                            print("DEBUG : POINT CARDINAL", point_cardinal)
                            
                            if not point_cardinal:
                                erreur_msg = "Point cardinal non trouvé pour repère '" + repere + "' pour parcelle '" + code_parcelle + "'"
                                erreurs.append(erreur_msg)
                                print(erreur_msg)
                                continue
                                
                            lp = Limiteparcelle()
                            lp.idpointscardinaux = point_cardinal.idpointscardinaux
                            lp.idparcelle = id_parcelle
                            lp.description = description
                            lp.path_file = None
                            bool_limite_parcelle = Limiteparcelle.insert(self.connection, lp)
                            print("DEBUG: Limite Parcelle insertion", bool_limite_parcelle)
                        except Exception as e:
                            erreur_msg = "Erreur lors de l'insertion du voisin " + str(idx + 1) + " pour parcelle '" + code_parcelle + "' : " + str(e)
                            erreurs.append(erreur_msg)
                            print(erreur_msg)
                            continue

                    #----------------------------------------------------------------------------------------
                    # DEBUT CRL
                    #----------------------------------------------------------------------------------------
                    for m in membres:
                        try:
                            pdata = m.get("personne", m)
                            role_lib = m.get("role", "")
                            is_titulaire = m.get("titulaire", True)
                            is_president = m.get("president", False)
                            if not role_lib:
                                continue
                            role_crl_model = RoleCrl(self.connection)
                            role = role_crl_model.find_or_create_by_lib(role_lib)
                            if not role:
                                erreur_msg = "Role CRL '%s' introuvable et creation echouee" % role_lib
                                erreurs.append(erreur_msg)
                                print(erreur_msg)
                                continue
                            p = Personne()
                            p.nompersonne = pdata.get("nom", "")
                            p.prenompersonne = pdata.get("prenom", "")
                            p.sexepersonne = pdata.get("sexe", "")
                            p.datenaissancepersonne = pdata.get("date_naissance")
                            p.lieunaissancepersonne = pdata.get("lieu_naissance", "")
                            p.nevers = pdata.get("ne_vers")
                            p.numactenaissancepersonne = pdata.get("num_acte_naissance", "")
                            p.dateactenaissancepersonne = pdata.get("date_acte_naissance")
                            p.numcipersonne = pdata.get("cin", "")
                            p.datecipersonne = pdata.get("date_cin")
                            p.lieucipersonne = pdata.get("lieu_cin", "")
                            p.nompere = pdata.get("nompere", "")
                            p.nommere = pdata.get("nommere", "")
                            p.situationmatrimoniale = 0
                            p.adressepersonne = pdata.get("adresse", "")
                            id_personne = Personne.insert(self.connection, p)
                            if not id_personne:
                                continue
                            data = [id_demande, int(role[0]), id_personne, is_titulaire, is_president]
                            role_crl_model.insert_role(data)
                        except Exception as e:
                            erreur_msg = "Erreur lors de l'insertion CRL pour parcelle '" + code_parcelle + "' : " + str(e)
                            erreurs.append(erreur_msg)
                            print(erreur_msg)
                    #----------------------------------------------------------------------------------------
                    # FIN CRL
                    #----------------------------------------------------------------------------------------

                    success_count += 1
                    traitement_parcelle_valide.append(code_parcelle)

                    #----------------------------------------------------------------------------------------
                    # FIN VOISINS
                    #---------------------------------------------------------------------------------------- 
                    
                except Exception as e:
                    erreur_msg = "Erreur non gérée lors du traitement de la parcelle '" + code_parcelle + "' : " + str(e)
                    erreurs.append(erreur_msg)
                    traitement_parcelle_refuse.append(code_parcelle)
                    print(erreur_msg)
                    continue

            # Affichage du récapitulatif
            message = "=== RÉCAPITULATIF DU TRAITEMENT ===\n\n"
            message += "Batch ID: " + str(batch_id) + "\n"
            message += "Demandes traitées avec succès: " + str(success_count) + "\n"
            message += "Parcelles validées: " + str(len(traitement_parcelle_valide)) + "\n"
            message += "Parcelles refusées: " + str(len(traitement_parcelle_refuse)) + "\n"
            
            if erreurs:
                message += "\n=== ERREURS (" + str(len(erreurs)) + ") ===\n"
                for i, erreur in enumerate(erreurs, 1):
                    message += str(i) + ". " + erreur + "\n"
            
            if traitement_parcelle_valide:
                message += "\n=== PARCELLES VALIDÉES ===\n"
                for p in traitement_parcelle_valide:
                    message += "- " + p + "\n"
                    
            if traitement_parcelle_refuse:
                message += "\n=== PARCELLES REFUSÉES ===\n"
                for p in traitement_parcelle_refuse:
                    message += "- " + p + "\n"
            
            if erreurs:
                QtGui.QMessageBox.warning(self, "Traitement terminé avec erreurs", message)
            else:
                QtGui.QMessageBox.information(self, "Succès", message)
                
            # Mise à jour du statut de traitement
            print("DEBUG : DEBUT  TEST traitement_parcelle_valide")

            if traitement_parcelle_valide or traitement_parcelle_refuse:
                if erreurs:
                    traitement_statut = "PARTIAL_SUCCESS"
                else:
                    traitement_statut = "SUCCESS"
                    
                valide_json = json.dumps([str(p) for p in traitement_parcelle_valide])
                refuse_json = json.dumps([str(p) for p in traitement_parcelle_refuse])
                FiplofIngestionModel.updateTraitementStatut(self.connection, batch_id,
                                    traitement_statut, valide_json, refuse_json)
            self.connection.commit()
            print("FIN : DEBUT  TEST traitement_parcelle_valide")

        except Exception as e:
            self.connection.rollback()
            erreur_msg = "Erreur critique lors du traitement global : " + str(e)
            erreurs.append(erreur_msg)
            print(erreur_msg)
            QtGui.QMessageBox.critical(self, "Erreur critique", erreur_msg)
    
    def geojson_to_wkb_hex(self, geometry):

        print("DEBUG : geojson_to_wkb_hex ", geometry)

        try:

            if not geometry:
                return None

            geojson_geom = {
                "type": geometry.get("type"),
                "coordinates": geometry.get("coordinates")
            }

            geom = shape(geojson_geom)

            # Python 2 / ancienne shapely
            return geom.wkb.encode('hex')

        except Exception as e:

            print("Erreur conversion geometry:", str(e))

            return None

    def showIngestionDetails(self, item):
        """Affiche les détails d'une ingestion dans une fenêtre séparée"""
        try:
            # Vérifier si l'item n'est pas None
            if item is None:
                return
                
            # Récupérer l'ID de l'ingestion
            row = item.row()
            
            # Récupérer l'item ID avec vérification
            id_item = self.ui.tableWidgetBath.item(row, 1)  # Colonne 1 = ID
            if id_item is None:
                return
                
            ingestion_id = str(id_item.text())
            
            # Récupérer les détails depuis la base
            model = FiplofIngestionModel()
            model.setConnection(self.connection)
            
            # Récupérer l'ingestion spécifique
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM fiplof_raw_ingestion WHERE id = %s", [ingestion_id])
            result = cursor.fetchone()
            cursor.close()
            if result:
                try:
                    # Parser le payload JSON
                    payload_data = None
                    demandes_found = []
                    
                    if result.get('payload'):
                        try:
                            import json
                            payload_data = json.loads(result['payload'])
                             
                            # Rechercher les demandes où code_parcelle est dans valid_parcelle
                            if 'demandes' in payload_data:
                                for demande in payload_data['demandes']:
                                    if 'demande' in demande and 'parcelle' in demande:
                                        code_parcelle = demande['parcelle'].get('code_parcelle', '')
                                        valid_parcelle = result.get('valid_parcelle', '')
                                        
                                        # Vérifier si code_parcelle est dans valid_parcelle
                                        if code_parcelle and valid_parcelle and code_parcelle in valid_parcelle:
                                            demandes_found.append({
                                                'code_parcelle': code_parcelle,
                                                'contenance': demande['parcelle'].get('contenance', ''),
                                                'date_dmd': demande['demande'].get('date_dmd', ''),
                                                'num_decision': demande['demande'].get('num_decision', ''),
                                                'date_decision': demande['demande'].get('date_decision', ''),
                                                'date_debut_aff': demande['demande'].get('date_debut_aff', ''),
                                                'date_fin_aff': demande['demande'].get('date_fin_aff', ''),
                                                'date_rl': demande['demande'].get('date_rl', ''),
                                                'duree_occupation': demande['demande'].get('duree_occupation', '')
                                            })
                        
                        except Exception as e:
                            print("Erreur lors du parsing du payload:", str(e))
                    
                    # Créer le message d'affichage
                    message = "Détails de l'Ingestion #" + str(result['id']) + "\n\n"
                    message += "Source: " + str(result.get('source_systeme', '')) + "\n"
                    message += "Statut: " + str(result.get('statut', '')) + "\n"
                    message += "Date: " + str(result.get('created_at', '')) + "\n"
                    message += "Validations: " + str(result.get('valid_parcelle', '')) + "\n"
                    message += "Erreurs: " + str(result.get('error_parcelle', '')) + "\n\n"
                    
                    # Ajouter les demandes trouvées dans le tableau tableWidgetDemande
                    if demandes_found:
                        message += "Demandes trouvées (" + str(len(demandes_found)) + "):\n"
                        for i, demande in enumerate(demandes_found, 1):
                            message += "\n" + str(i) + ". " + demande['code_parcelle'] + "\n"
                            message += "   Contenance: " + str(demande['contenance']) + "\n"
                            message += "   Date demande: " + str(demande['date_dmd']) + "\n"
                            message += "   Num décision: " + str(demande['num_decision']) + "\n"
                            message += "   Date décision: " + str(demande['date_decision']) + "\n"
                            message += "   Date début aff: " + str(demande['date_debut_aff']) + "\n"
                            message += "   Date fin aff: " + str(demande['date_fin_aff']) + "\n"
                            message += "   Date RL: " + str(demande['date_rl']) + "\n"
                            message += "   Durée occupation: " + str(demande['duree_occupation']) + "\n"
                        
                        # Alimenter le tableau tableWidgetDemande avec les demandes trouvées
                        self.alimenterTableauDemandes(demandes_found)
                    else:
                        message += "\nAucune demande trouvée avec code_parcelle dans valid_parcelle"
                        # Vider le tableau tableWidgetDemande si aucune demande trouvée
                        self.viderTableauDemandes()
                    
                    #QtGui.QMessageBox.information(self, "Détails de l'Ingestion", message)
                    
                except Exception as e:
                    print("Erreur lors de la création de la fenêtre de détails:", str(e))
                    QtGui.QMessageBox.critical(self, "Erreur", "Impossible d'afficher les détails: " + str(e))
                
        except Exception as e:
            print("Erreur lors de l'affichage des détails:", str(e))
            
    def onCheckboxClicked(self, state, row):
        """Gère le clic sur checkbox pour sélectionner la ligne et récupérer l'ID"""
        try:
            # Si la checkbox est cochée, décocher toutes les autres
            if state == 2:  # Qt.Checked
                # Parcourir toutes les lignes et décocher les autres checkboxes
                for i in range(self.ui.tableWidgetBath.rowCount()):
                    if i != row:  # Ne pas décocher la ligne actuelle
                        checkbox_widget = self.ui.tableWidgetBath.cellWidget(i, 0)
                        if checkbox_widget:
                            checkbox_layout = checkbox_widget.layout()
                            if checkbox_layout and checkbox_layout.count() > 0:
                                checkbox = checkbox_layout.itemAt(0).widget()
                                if checkbox and checkbox.isChecked():
                                    checkbox.blockSignals(True)
                                    checkbox.setChecked(False)
                                    checkbox.blockSignals(False)
                
                # Désélectionner toutes les lignes
                self.ui.tableWidgetBath.clearSelection()
                # Sélectionner uniquement la ligne cochée
                self.ui.tableWidgetBath.selectRow(row)
                
                # Récupérer l'ID de la ligne
                id_item = self.ui.tableWidgetBath.item(row, 1)  # Colonne 1 = ID
                if id_item:
                    # Afficher les détails de l'ingestion
                    self.showIngestionDetails(id_item)
            else:  # Qt.Unchecked
                # Désélectionner la ligne
                self.ui.tableWidgetBath.clearSelection()
                    
        except Exception as e:
            print("Erreur lors du clic sur checkbox:", str(e))
            
    def onRowSelectionChanged(self):
        """Gère le changement de sélection de ligne"""
        try:
            selected_items = self.ui.tableWidgetBath.selectedItems()
            if selected_items:
                # Afficher les détails de l'ingestion sélectionnée
                self.showIngestionDetails(selected_items[0])
        except Exception as e:
            print("Erreur lors de la sélection de ligne:", str(e))
            
    def alimenterTableauDemandes(self, demandes_found):
        """Alimente le tableau tableWidgetDemande avec les demandes trouvées"""
        try:
            # Vider d'abord le tableau
            self.viderTableauDemandes()
            
            # Configurer les colonnes si ce n'est pas déjà fait
            if self.ui.tableWidgetDemande.columnCount() == 0:
                headers = [u"S\u00e9lection", u"Code Parcelle", u"Contenance", u"Date Dmd", u"Num D\u00e9cision", u"Date D\u00e9cision", u"Date D\u00e9but Aff", u"Date Fin Aff", u"Date RL", u"Dur\u00e9e Occupation"]
                self.ui.tableWidgetDemande.setColumnCount(len(headers))
                self.ui.tableWidgetDemande.setHorizontalHeaderLabels(headers)
                
                # Style pour les données : police moderne et espacement
                data_font = QtGui.QFont()
                data_font.setPointSize(9)
                data_font.setFamily("Segoe UI")
                self.ui.tableWidgetDemande.setFont(data_font)
                
                # Style pour l'entête : police en gras et moderne (comme tableWidgetBath)
                header_font = QtGui.QFont()
                header_font.setBold(True)
                header_font.setPointSize(14)
                header_font.setFamily("Segoe UI")
                self.ui.tableWidgetDemande.horizontalHeader().setFont(header_font)
                
                # Appliquer un style moderne et élégant
                      
                # Ajuster les largeurs de colonnes avec de meilleurs ratios
                self.ui.tableWidgetDemande.setColumnWidth(0, 60)   # Sélection (checkbox)
                self.ui.tableWidgetDemande.setColumnWidth(1, 220)  # Code Parcelle (encore plus grand)
                self.ui.tableWidgetDemande.setColumnWidth(2, 80)   # Contenance
                self.ui.tableWidgetDemande.setColumnWidth(3, 100)  # Date Dmd
                self.ui.tableWidgetDemande.setColumnWidth(4, 100)  # Num Décision
                self.ui.tableWidgetDemande.setColumnWidth(5, 100)  # Date Décision
                self.ui.tableWidgetDemande.setColumnWidth(6, 100)  # Date Début Aff
                self.ui.tableWidgetDemande.setColumnWidth(7, 100)  # Date Fin Aff
                self.ui.tableWidgetDemande.setColumnWidth(8, 100)  # Date RL
                self.ui.tableWidgetDemande.setColumnWidth(9, 120)  # Durée Occupation
                self.ui.tableWidgetDemande.horizontalHeader().setStretchLastSection(True)
                
                # Activer les fonctionnalités modernes
                self.ui.tableWidgetDemande.setAlternatingRowColors(True)
                self.ui.tableWidgetDemande.setShowGrid(True)
                self.ui.tableWidgetDemande.verticalHeader().setVisible(False)
                self.ui.tableWidgetDemande.horizontalHeader().setHighlightSections(True)
                self.ui.tableWidgetDemande.horizontalHeader().setSortIndicatorShown(True)
            
            # Ajouter chaque demande trouvée
            for i, demande in enumerate(demandes_found):
                self.ui.tableWidgetDemande.insertRow(i)
                
                # Checkbox dans la première colonne
                checkbox = QtGui.QCheckBox()
                checkbox.setChecked(False)
                # Connecter le signal de clic sur la checkbox
                checkbox.stateChanged.connect(lambda state, row=i: self.onDemandeCheckboxClicked(state, row))
                # Centrer la checkbox dans la cellule
                checkbox_layout = QtGui.QHBoxLayout()
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(QtCore.Qt.AlignCenter)
                checkbox_widget = QtGui.QWidget()
                checkbox_widget.setLayout(checkbox_layout)
                self.ui.tableWidgetDemande.setCellWidget(i, 0, checkbox_widget)
                
                # Ajouter les données dans les colonnes (décalées de 1)
                self.ui.tableWidgetDemande.setItem(i, 1, QtGui.QTableWidgetItem(str(demande.get('code_parcelle', ''))))
                self.ui.tableWidgetDemande.setItem(i, 2, QtGui.QTableWidgetItem(str(demande.get('contenance', ''))))
                self.ui.tableWidgetDemande.setItem(i, 3, QtGui.QTableWidgetItem(str(demande.get('date_dmd', ''))))
                self.ui.tableWidgetDemande.setItem(i, 4, QtGui.QTableWidgetItem(str(demande.get('num_decision', ''))))
                self.ui.tableWidgetDemande.setItem(i, 5, QtGui.QTableWidgetItem(str(demande.get('date_decision', ''))))
                self.ui.tableWidgetDemande.setItem(i, 6, QtGui.QTableWidgetItem(str(demande.get('date_debut_aff', ''))))
                self.ui.tableWidgetDemande.setItem(i, 7, QtGui.QTableWidgetItem(str(demande.get('date_fin_aff', ''))))
                self.ui.tableWidgetDemande.setItem(i, 8, QtGui.QTableWidgetItem(str(demande.get('date_rl', ''))))
                self.ui.tableWidgetDemande.setItem(i, 9, QtGui.QTableWidgetItem(str(demande.get('duree_occupation', ''))))
                
                # Centrer les données (sauf la checkbox)
                for col in range(1, 10):
                    item = self.ui.tableWidgetDemande.item(i, col)
                    if item:
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
            
            print("Tableau tableWidgetDemande alimenté avec " + str(len(demandes_found)) + " demandes")
            
        except Exception as e:
            print("Erreur lors de l'alimentation du tableau tableWidgetDemande:", str(e))
    
    def viderTableauDemandes(self):
        """Vide le tableau tableWidgetDemande"""
        try:
            self.ui.tableWidgetDemande.setRowCount(0)
            print("Tableau tableWidgetDemande vidé")
        except Exception as e:
            print("Erreur lors du vidage du tableau tableWidgetDemande:", str(e))
    
    def onCocherTousClicked(self, state):
        """Gère le clic sur la checkbox 'Cocher tout'"""
        try:
            # Parcourir toutes les lignes du tableau
            for row in range(self.ui.tableWidgetDemande.rowCount()):
                # Récupérer la checkbox de la ligne
                checkbox_widget = self.ui.tableWidgetDemande.cellWidget(row, 0)
                if checkbox_widget:
                    checkbox_layout = checkbox_widget.layout()
                    if checkbox_layout and checkbox_layout.count() > 0:
                        checkbox = checkbox_layout.itemAt(0).widget()
                        if checkbox:
                            # Bloquer le signal pour éviter la récursion
                            checkbox.blockSignals(True)
                            checkbox.setChecked(state == 2)  # Qt.Checked
                            checkbox.blockSignals(False)
                            
                            # Colorer ou décolorer la ligne
                            if state == 2:  # Qt.Checked
                                for col in range(1, 10):  # Colonnes 1 à 9
                                    item = self.ui.tableWidgetDemande.item(row, col)
                                    if item:
                                        item.setBackground(QtGui.QColor("#E3F2FD"))  # Bleu clair
                                        item.setForeground(QtGui.QColor("#1565C0"))  # Texte bleu foncé
                            else:  # Qt.Unchecked
                                for col in range(1, 10):  # Colonnes 1 à 9
                                    item = self.ui.tableWidgetDemande.item(row, col)
                                    if item:
                                        item.setBackground(QtGui.QColor("#ffffff"))  # Blanc
                                        item.setForeground(QtGui.QColor("#000000"))  # Texte noir
            
            if state == 2:
                print("Toutes les lignes ont été cochées et colorées")
            else:
                print("Toutes les lignes ont été décochées et décolorées")
                
        except Exception as e:
            print("Erreur lors du clic sur 'Cocher tout':", str(e))
    
    def onDemandeCheckboxClicked(self, state, row):
        """Gère le clic sur checkbox dans tableWidgetDemande"""
        try:
            # Colorer la ligne entière quand la checkbox est cochée
            if state == 2:  # Qt.Checked
                # Colorer la ligne en bleu clair
                for col in range(1, 10):  # Colonnes 1 à 9 (pas la checkbox)
                    item = self.ui.tableWidgetDemande.item(row, col)
                    if item:
                        item.setBackground(QtGui.QColor("#E3F2FD"))  # Bleu clair
                        item.setForeground(QtGui.QColor("#1565C0"))  # Texte bleu foncé
                print("Ligne " + str(row) + " sélectionnée et colorée dans tableWidgetDemande")
            else:  # Qt.Unchecked
                # Remettre la couleur par défaut
                for col in range(1, 10):  # Colonnes 1 à 9 (pas la checkbox)
                    item = self.ui.tableWidgetDemande.item(row, col)
                    if item:
                        item.setBackground(QtGui.QColor("#ffffff"))  # Blanc
                        item.setForeground(QtGui.QColor("#000000"))  # Texte noir
                print("Ligne " + str(row) + " désélectionnée et décolorée dans tableWidgetDemande")
                
        except Exception as e:
            print("Erreur lors du clic sur checkbox de demande:", str(e))
    
    def getSelectedDemandes(self):
        """Retourne la liste des demandes sélectionnées dans tableWidgetDemande"""
        try:
            selected_demandes = []
            for row in range(self.ui.tableWidgetDemande.rowCount()):
                # Récupérer la checkbox de la ligne
                checkbox_widget = self.ui.tableWidgetDemande.cellWidget(row, 0)
                if checkbox_widget:
                    checkbox_layout = checkbox_widget.layout()
                    if checkbox_layout and checkbox_layout.count() > 0:
                        checkbox = checkbox_layout.itemAt(0).widget()
                        if checkbox and checkbox.isChecked():
                            # Récupérer les données de la ligne
                            code_parcelle_item = self.ui.tableWidgetDemande.item(row, 1)
                            if code_parcelle_item:
                                selected_demandes.append({
                                    'row': row,
                                    'code_parcelle': code_parcelle_item.text(),
                                    'contenance': self.ui.tableWidgetDemande.item(row, 2).text() if self.ui.tableWidgetDemande.item(row, 2) else '',
                                    'date_dmd': self.ui.tableWidgetDemande.item(row, 3).text() if self.ui.tableWidgetDemande.item(row, 3) else '',
                                    'num_decision': self.ui.tableWidgetDemande.item(row, 4).text() if self.ui.tableWidgetDemande.item(row, 4) else '',
                                    'date_decision': self.ui.tableWidgetDemande.item(row, 5).text() if self.ui.tableWidgetDemande.item(row, 5) else '',
                                    'date_debut_aff': self.ui.tableWidgetDemande.item(row, 6).text() if self.ui.tableWidgetDemande.item(row, 6) else '',
                                    'date_fin_aff': self.ui.tableWidgetDemande.item(row, 7).text() if self.ui.tableWidgetDemande.item(row, 7) else '',
                                    'date_rl': self.ui.tableWidgetDemande.item(row, 8).text() if self.ui.tableWidgetDemande.item(row, 8) else '',
                                    'duree_occupation': self.ui.tableWidgetDemande.item(row, 9).text() if self.ui.tableWidgetDemande.item(row, 9) else ''
                                })
            
            print("Demandes sélectionnées: " + str(len(selected_demandes)))
            return selected_demandes
            
        except Exception as e:
            print("Erreur lors de la récupération des demandes sélectionnées:", str(e))
            return []
    
    def fermer(self):
        """Ferme la fenêtre"""
        self.close()
    
    def map_situation_matrimoniale(self,value):

        if not value:
            return 0

        v = value.strip().lower()

        if v == "celibataire":
            return 0

        if v == "marie":
            return 1

        if v == "veuf":
            return 2

        return 0

