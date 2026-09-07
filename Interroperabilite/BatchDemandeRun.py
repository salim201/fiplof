 
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


from BatchDemande import Ui_Gestion
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
class BatchDemandeRun(QDialog):
    def __init__(self, connection):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Gestion()
        self.ui.setupUi(self)       
        
        try:
            self.initDB()
            self.initActions()
        except Exception as e:
            print(e)
       

    def initDB(self):
        self.cur = self.connection.cursor()
        
        

    def initActions(self):
        print("********************initActions**************************")
        #self.setWindowTitle(u"Batch Demande - Interopérabilité")
        #self.ui.pushButton_2.setText( "TRAITER")
        self.ui.pushButton_valider.clicked.connect(self.validerDemandes)
        self.ui.cocherTous.stateChanged.connect(self.onCocherTousClicked)
        self.ui.tableWidgetBath.itemClicked.connect(self.showIngestionDetails)
        self.loadBatch()        
        '''self.ui.pushButton_valider.clicked.connect(        
            self.validerDemandes()
        )'''
        
   
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
   
   
    def loadBatch(self):

        """Charge les données d'ingestion dans le tableau"""

        try:

            model = FiplofIngestionModel()
            model.setConnection(self.connection)

            ingestions = model.getIngestionsWithoutPayload()

            table = self.ui.tableWidgetBath

            table.clearContents()
            table.setRowCount(0)

            table.setColumnCount(8)

            table.setHorizontalHeaderLabels([
                "",
                "ID",
                "Source",
                "Statut",
                "Date",
                "Demande validée",
                "Demande refusée",
                "Traitement"
            ])

            # =========================================================
            # >>> MODIFICATION : STYLE ENTETE
            # =========================================================

            header_font = QtGui.QFont()
            header_font.setBold(True)
            header_font.setPointSize(12)
            header_font.setFamily("Segoe UI")

            table.horizontalHeader().setFont(header_font)

            # =========================================================
            # >>> MODIFICATION : STYLE DONNEES
            # =========================================================

            data_font = QtGui.QFont()
            data_font.setPointSize(10)
            data_font.setFamily("Segoe UI")

            table.setFont(data_font)

            # =========================================================
            # >>> MODIFICATION : UNE SEULE SELECTION
            # =========================================================

            table.setSelectionMode(
                QtGui.QAbstractItemView.SingleSelection
            )

            table.setSelectionBehavior(
                QtGui.QAbstractItemView.SelectRows
            )

            # =========================================================
            # >>> MODIFICATION : STYLE CSS
            # =========================================================

            table.setStyleSheet("""

                QTableWidget {
                    background-color: rgba(255,255,255,240);
                    alternate-background-color: #F8F8F8;
                    gridline-color: #E0E0E0;
                    border: 1px solid #D0D0D0;
                    selection-background-color: #DCEEFF;
                    selection-color: #222222;
                }

                QTableWidget::item {
                    padding: 6px;
                }

                QTableWidget::item:selected {
                    background-color: #DCEEFF;
                    color: #222222;
                    border: none;
                }

                QHeaderView::section {
                    background-color: #90EE90;
                    color: #006600;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 8px;
                    border: 1px solid #008000;
                }

            """)

            # =========================================================
            # >>> MODIFICATION : DECONNECTER AVANT CONNECT
            # =========================================================

            try:
                table.itemSelectionChanged.disconnect()
            except:
                pass

            table.itemSelectionChanged.connect(
                self.onRowSelectionChanged
            )

            # =========================================================
            # >>> MODIFICATION : LISTE DES CHECKBOX
            # =========================================================

            self.batch_checkboxes = []

            # =========================================================
            # >>> CHARGEMENT DES DONNEES
            # =========================================================

            for i, ingestion in enumerate(ingestions):

                demande_validee = self.count_list_text(
                    ingestion.get('valid_parcelle', '')
                )

                demande_refusee = self.count_list_text(
                    ingestion.get('error_parcelle', '')
                )

                table.insertRow(i)

                # =====================================================
                # >>> MODIFICATION : CHECKBOX UNIQUE
                # =====================================================

                checkbox = QtGui.QCheckBox()

                self.batch_checkboxes.append(checkbox)

                checkbox.stateChanged.connect(
                    lambda state, row=i:
                    self.onCheckboxClicked(state, row)
                )

                table.setCellWidget(i, 0, checkbox)

                # =====================================================
                # CREATION ITEMS
                # =====================================================

                values = [
                    str(ingestion.get('id') or ''),
                    ingestion.get('source_systeme') or '',
                    ingestion.get('statut') or '',
                    str(ingestion.get('created_at') or ''),
                    str(demande_validee),
                    str(demande_refusee),
                    str(ingestion.get('traitement_statut') or '')
                ]

                for col, value in enumerate(values, start=1):

                    item = QtGui.QTableWidgetItem(value)

                    # =================================================
                    # >>> MODIFICATION : CENTRAGE
                    # =================================================

                    item.setTextAlignment(
                        QtCore.Qt.AlignCenter
                    )

                    table.setItem(i, col, item)

            # =========================================================
            # >>> MODIFICATION : LARGEUR COLONNES
            # =========================================================

            table_width = table.width()

            total_width = table_width - 20

            table.setColumnWidth(0, int(total_width * 0.05))
            table.setColumnWidth(1, int(total_width * 0.10))
            table.setColumnWidth(2, int(total_width * 0.15))
            table.setColumnWidth(3, int(total_width * 0.12))
            table.setColumnWidth(4, int(total_width * 0.20))
            table.setColumnWidth(5, int(total_width * 0.15))
            table.setColumnWidth(6, int(total_width * 0.15))
            table.setColumnWidth(7, int(total_width * 0.08))

            header = table.horizontalHeader()

            header.setStretchLastSection(True)

        except Exception as e:

            print(
                "Erreur lors du chargement du batch:",
                str(e)
            )

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

