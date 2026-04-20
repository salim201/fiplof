#coding: utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2
from psycopg2.extensions import *
from models.ProjetCouche import ProjetCouche

from AreaConvert import AreaConvert
from .suivi import Ui_Dialog

class Suivi(QDialog):
    def __init__(self, connection, parent):
        self.connection = connection
        QDialog.__init__(self)
        from Configuration import DbConfig
        self.db_config = DbConfig.DbConfig()
        #self.setFixedHeight(663)
        #self.setFixedWidth(1154)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.initMasks()
        self.ui.radioButtonAucun.setChecked(True)
        self.ui.radioButtonSRI.setChecked(True)
        self.ui.tableWidgetBatiment.setSelectionMode(1)
        self.ui.tableWidgetBatiment.setSelectionBehavior(1)
        self.ui.tableWidgetLimites.setSelectionBehavior(1)
        self.ui.tableWidgetLimites.setSelectionMode(1)
        self.ui.tableWidgetConsorts.setSelectionMode(1)
        self.ui.tableWidgetConsorts.setSelectionBehavior(1)
        self.canvas = parent.canvas
        self.cv = None
        self.tool = parent.tool
        self.senderName = self.sender().objectName()
        self.idConsorts = []
        self.idparcelle = None
        self.idConsorts = None

        self.limitesParcelle = []
        self.infosBatiments = []

        self.codesFokontany = []
        self.limitesParcelle = []
        self.infosBatiments = []
        self.idPointCardinaux = []
        self.idCategories = []
        self.idCategoriesBatiment = []
        self.idConsistances = []
        self.singleIdConsistance = None
        self.idConsistancesBatiment = []
        self.idFokontany = []
        self.singleIdFokontany = None
        self.idHameau = []
        self.singleIdHameau = None
        self.codesHameau = []

        self.registry = parent.registry

        self.idContribuable = None
        if self.idContribuable == None:
            self.ui.btnConsorts.setEnabled(False)

        self.initDB()
        self.firstId = self.getFirstId()
        self.currId = self.firstId
        self.nbrparcelle = self.getNbrParcelle()
        self.getDataFromDB(self.currId)
        from .VoirListeContribuableRun import VoirListeContribuableRun
        self.listeContribuable = VoirListeContribuableRun(self.connection)
        from Personnes.ListePersonnePqueRun import ListePersonnePqueRun
        self.listePersonne = ListePersonnePqueRun(self.connection)
        from Fiplof.Saisie.EditionConsortsRun import EditionConsorts
        self.listeConsorts = EditionConsorts(self.connection, None, 2, self)

        from .ContribuableRun import ContribuableRun
        self.contribuable = ContribuableRun(self.connection)
        self.initActions()

        self.fillComboCategorieParcelle()
        self.fillComboCategorieBatiment()
        self.fillComboConsistance()
        self.fillComboPosition()

        self.fillTerritoire()
        self.fillHameau()

        self.raster_path, self.layer_raster, self.layer_shape, self.rect = None, None, None, None
        #self.id_projet = self.parent.id_projet

    def init_layers(self):
        couches = ProjetCouche.find_by_projet_commune(self.connection, globalvars.id_projet_commune)
        for couche in couches:
            if couche.type_couche == 'R':
                self.raster_path = couche.fichier
                break

    def load_raster(self):
        if self.raster_path is None:
            return
        fileInfo = QFileInfo(self.raster_path)
        baseName = fileInfo.baseName()
        layer = QgsRasterLayer(self.raster_path, baseName)
        if not layer.isValid():
            print("Layer " + self.raster_path + " is not valid raster")
            return None
        # QgsMapLayerRegistry.instance().addMapLayer(layer)
        self.layer_raster = layer

    def init_canvas(self):
        style = {
            u'outline_width': u'0.3',
            u'outline_color': u'244,0,0,255',
            u'offset_unit': u'MM',
            u'color': u'227,26,28,255',
            u'outline_style': u'solid',
            u'style': u'b_diagonal',
            u'joinstyle': u'bevel',
            u'outline_width_unit': u'MM',
            u'border_width_map_unit_scale': u'0,0',
            u'offset': u'0,0',
            u'offset_map_unit_scale': u'0,0'
        }
        self.cv = QgsMapCanvas()
        #self.idparcelle;
        # add canvas  ad form
        self.ui.horizontalLayout_.addWidget(self.cv)
        self.cv.show()
        uri = QgsDataSourceURI()
        uri.setConnection(
            self.db_config.db_host,
            self.db_config.db_port,
            self.db_config.db_name,
            self.db_config.db_user,
            self.db_config.db_pass
        )
        uri.setDataSource("public", "parcelle_d", "geom", "gid=%s" % (self.currId,))
        uri.setKeyColumn("gid")
        layer = QgsVectorLayer(uri.uri(), "Fiscalite", "postgres")
        if not layer.isValid():
            return
        crs = QgsCoordinateReferenceSystem(globalvars.EPSG_SCR, QgsCoordinateReferenceSystem.EpsgCrsId)
        layer.setCrs(crs)
        symbol_layer = QgsFillSymbolV2.createSimple(style)
        layer.rendererV2().setSymbol(symbol_layer)
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        QgsMapLayerRegistry.instance().addMapLayer(self.layer_raster)
        # self.cv.setLayerSet([QgsMapCanvasLayer(self.layer_raster)])
        self.cv.setLayerSet([QgsMapCanvasLayer(layer), QgsMapCanvasLayer(self.layer_raster)])
        self.cv.setExtent(layer.extent())

    def initActions(self):
        self.ui.btnSuivant.clicked.connect(self.nextData)
        self.ui.btnPrecedent.clicked.connect(self.previousData)
        self.ui.btnAjouterBat.clicked.connect(self.addOneBat)
        self.ui.btnSupprimerBat.clicked.connect(self.deleteOneBat)
        self.ui.btnSupprimerLimite.clicked.connect(self.deleteLimite)
        self.ui.btnAjoutLimite.clicked.connect(self.addLimite)
        self.ui.btnEnregistrer.clicked.connect(self.readInput)
        #self.ui.btnRrechercherContribuable.clicked.connect(self.ouvrirListeContribuable)
        self.ui.btnRrechercherContribuable.clicked.connect(self.ouvrirListePersonne)
        self.ui.btnConsorts.clicked.connect(self.ouvrirListeConsorts)
        self.listePersonne.ui.btnSelectionner.clicked.connect(self.setIdContribuable)
        self.listeContribuable.ui.btnSelectionner.clicked.connect(self.getContribuableInfo)
        self.listeConsorts.ui.pushButton_4.clicked.connect(self.enregConsorts)
        self.ui.tableWidgetConsorts.cellClicked.connect(self.selectionLigneConsort)
        self.ui.btnVoirConsorts.clicked.connect(self.showConsort)
        self.ui.btnModifierConsorts.clicked.connect(self.editConsort)

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
        vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        self.canvas.setCurrentLayer(vtlayer)

    def getDataFromDB(self, idparcelle = None, direction = None):
        self.clearAll()
        self.idparcelle = idparcelle
        try:
            self.cur.execute("SELECT numero, codeparcelle, idhameau, has_data, conversion, numdemande, srisraparcelle, etatparcelle_d FROM parcelle_d pd WHERE estfiscalite = 1 AND  gid = %s AND id_commune = %s", (idparcelle, globalvars.id_commune))
            data = self.cur.fetchone()
            #print "Donnees fiscales"
            if data is not None:
                self.zoomToSelLayer()
                self.init_layers()
                self.load_raster()
                self.init_canvas()
                self.getSurface()
                self.useData(data)
            else:
                if direction == 1:
                    self.nextData()
                elif direction == -1:
                    self.previousData()
            #self.useData(data)
        except StandardError as e:
            print (e)
            self.connection.rollback()

    def ouvrirListePersonne(self):
        self.listePersonne.exec_()

    def enregConsorts(self):
        self.idConsorts = self.listeConsorts.getProprioPhysique()
        print "ids des consorts = " + str(self.idConsorts)
        self.listeConsorts.close()

    def setIdContribuable(self):
        self.idContribuable = self.listePersonne.getIdPersonne()
        print "id contribuable = " + str(self.idContribuable)
        if self.idContribuable is not None:
            self.getContribuableById(self.idContribuable)
        self.listePersonne.close()

    def getNbrParcelle(self):
        try:
            self.cur.execute("SELECT MAX(gid) FROM parcelle_d WHERE estfiscalite = 1")
            nbrParcelle = self.cur.fetchone()
            return nbrParcelle[0]
        except StandardError as e:
            self.connection.rollback()
            print(e)

    def getFirstId(self):
        try:
            self.cur.execute("SELECT MIN(gid) FROM parcelle_d WHERE estfiscalite = 1")
            minId = self.cur.fetchone()
            return minId[0]
        except StandardError as e:
            self.connection.rollback()
            print(e)

    def nextData(self):
        print self.currId
        print self.nbrparcelle
        if self.currId < self.nbrparcelle:
            self.currId = self.currId + 1
        self.getDataFromDB(self.currId, 1)

    def previousData(self):
        print self.currId
        print self.nbrparcelle
        if self.currId > self.firstId:
            self.currId = self.currId - 1
        self.getDataFromDB(self.currId, -1)

    def fillTerritoire(self):
        self.ui.comboBoxFokontany.clear()
        self.codesFokontany[:] = []
        self.idFokontany[:] = []
        # Fokontany
        try:
            self.cur.execute("SELECT nomfokontany, idfokontany, codefokontany FROM fokontany WHERE idcommune = %s",
                             (globalvars.id_commune,))
            fkts = self.cur.fetchall()
            for fkt in fkts:
                self.ui.comboBoxFokontany.addItem(fkt[0])
                self.idFokontany.append(fkt[1])
                self.codesFokontany.append(fkt[2])
        except StandardError as e:
            print e

        self.fillHameau()

    def fillHameau(self):
        self.idHameau[:] = []
        self.ui.comboBoxHameau.clear()
        self.codesHameau[:] = []
        idFokontany = self.idFokontany[self.ui.comboBoxFokontany.currentIndex()]
        try:
            self.cur.execute("SELECT idhameau, codehameau, nomhameau FROM hameau WHERE idfokontany = %s", (idFokontany,))
            hmx = self.cur.fetchall()
            for hm in hmx:
                self.idHameau.append(hm[0])
                self.ui.comboBoxHameau.addItem(hm[2])
                self.codesHameau.append(hm[1])
        except StandardError as e:
            print e

    def useData(self, data):
        if data[0] is not None:
            self.ui.lineEditNumero.setText(data[0])
        if data[1] is not None:
            self.ui.lineEditCode.setText(data[1])
        if data[2] is not None:
            try:
                self.cur.execute("SELECT h.nomhameau, f.nomfokontany FROM hameau h, fokontany f WHERE h.idfokontany = f.idfokontany AND idhameau = %s", (data[2],))
                hm = self.cur.fetchone()
                print hm
                self.ui.comboBoxFokontany.setCurrentIndex(self.ui.comboBoxFokontany.findText(str(hm[1].strip())))
                self.ui.comboBoxHameau.setCurrentIndex(self.ui.comboBoxHameau.findText(str(hm[0]).strip()))

            except StandardError as e:
                print (e)
                self.connection.rollback()
        #if data[4] is True:
        if data[4] is not None:
            #self.ui.convertirDemande.show()
            self.etatConversion = data[4]
            if data[4] == 1: # deja converti en demande
                self.ui.lineEditNumDemande.setText(str(data[5]).strip())
            elif data[4] == 2: # deja converti en CF
                try:
                    self.cur.execute("SELECT c.numerocertificat FROM certificat c, parcelle_d p WHERE p.idcertificat = c.idcertificat AND p.gid = %s", (self.currId,))
                    numCF = self.cur.fetchone()
                    self.ui.lineEditNumCertificat.setText(str(numCF[0]).strip())
                except StandardError as e:
                    self.connection.rollback()
                    print(e)
        #traitement contribuable
        try:
            self.cur.execute("SELECT idpersonne FROM contribuables_parcelle WHERE idparcelle = %s AND contribuable = %s",(self.currId, True))
            dataPersonne = self.cur.fetchone()
            print "Data Personne = " + str (dataPersonne)
            if dataPersonne is not None:
                self.idContribuable = dataPersonne[0]
                self.getContribuableById(dataPersonne[0])
                print "idContribuable = " + str(dataPersonne[0])
        except StandardError as e:
            print (e)
            self.connection.rollback()
        #if data[2] is not None:
            #self.getContribuableById(data[2])
        if data[6] is not None:
            if data[6] == "sri":
                self.ui.radioButtonSRI.setChecked(True)
            elif data[6] == "sra":
                self.ui.radioButtonSRA.setChecked(True)
        if data[7] is not None:
            if data[7] == 0:
                self.ui.radioButtonAucun.setChecked(True)
            elif data[7] == 1:
                self.ui.radioButtonTitree.setChecked(True)
            elif data[7] == 2:
                self.ui.radioButtonCadastre.setChecked(True)
            elif data[7] == 3:
                self.ui.radioButtonCertifie.setChecked(True)

        # afficher les limites de la parcelle ##
        try:
            self.cur.execute("SELECT pc.idpointscardinaux, pc.position, l.description FROM limitesparcelle l, pointscardinaux pc WHERE l.idpointscardinaux = pc.idpointscardinaux AND l.idparcelle = %s", (self.currId,))
            limites = self.cur.fetchall()
            print limites
            self.showInTable(limites)
        except StandardError as e:
            self.connection.rollback()
            print(e)
        # afficher les batiments sur la parcelle ##
        try:
            self.cur.execute("SELECT b.codebatiment,c.libelleconsistance, b.surfacebatiment, b.nbpiecebatiment, b.idparcelle  FROM batiment b, consistance c WHERE b.idconsistance = c.idconsistance AND b.idparcelle = %s", (self.currId,))
            bats = self.cur.fetchall()
            self.infosBatiments[:] = []
            for bat in bats:
                if bat not in self.infosBatiments:
                    self.infosBatiments.append(bat)
            print self.infosBatiments
            self.showInTableBatiment(bats)
        except StandardError as e:
            self.connection.rollback()
            print(e)

        self.fillInfoBatFromTable()

    def getContribuableById(self, id):
        self.ui.btnConsorts.setEnabled(True)
        #print self.idContribuable
        self.listeConsorts.setIdContribuableToPass(self.idContribuable)
        self.listeConsorts.setIdParcelle(self.currId)
        self.listeConsorts.proprietairePhysiques()
        self.cur.execute("SELECT * FROM personne WHERE idpersonne = %s", (id,))
        data = self.cur.fetchone()
        print data
        self.fillFields(data)

    def fillFields(self, data):
        self.idContribuable = data[0]
        if data[1]:
            self.ui.lineEditNomContribuable.setText(data[1])
        if data[2]:
            self.ui.lineEditPrenomContribuable.setText(data[2])
        if data[13]:
            self.ui.lineEditAdresse.setText(data[13])
        if data[4]:
            self.ui.dateEditNaissance.setDate(data[4])
        if data[6]:
            self.ui.lineEditLieuNaissance.setText(data[6])
        if data[7]:
            self.ui.tabCIN.setCurrentIndex(0)
            self.ui.lineEditCIN1.setText(data[7][0:3])
            self.ui.lineEditCIN2.setText(data[7][3:6])
            self.ui.lineEditCIN3.setText(data[7][6:9])
            self.ui.lineEditCIN4.setText(data[7][9:len(data[7])])
            if data[8]:
                self.ui.dateEditCIN.setDate(data[8])
            if data[9]:
                self.ui.lineEditLieuCIN.setText(data[9])
        if data[10]:
            self.ui.tabCIN.setCurrentIndex(1)
            self.ui.lineEditNumActeNaissance.setText(data[10])
            if data[11]:
                self.ui.dateEditActeNaissance.setDate(data[11])
            if data[12]:
                self.ui.lineEditLieuActeNaissance.setText(data[12])
        if data[3]:
            if data[3] == "masculin":
                self.ui.radioButtonHomme.setChecked(True)
            if data[3] == "feminin":
                self.ui.radioButtonFemme.setChecked(True)

    def clearAll(self):
        self.ui.lineEditNumero.clear()
        self.ui.lineEditCode.clear()
        self.ui.checkBoxAlloueParcelle.setChecked(False)
        self.ui.plainTextEditObservation.clear()
        self.ui.lineEditSurfaceM2.clear()
        self.ui.lineEditSurfaceHa.clear()
        self.ui.tableWidgetBatiment.setRowCount(0)
        self.ui.tableWidgetLimites.setRowCount(0)
        self.ui.tableWidgetConsorts.setRowCount(0)
        self.ui.lineEditNomContribuable.clear()
        self.ui.lineEditPrenomContribuable.clear()
        self.ui.lineEditAdresse.clear()
        self.ui.lineEditLieuNaissance.clear()
        self.ui.lineEditCIN1.clear()
        self.ui.lineEditCIN2.clear()
        self.ui.lineEditCIN3.clear()
        self.ui.lineEditCIN4.clear()
        self.ui.lineEditLieuCIN.clear()
        self.ui.lineEditNumActeNaissance.clear()
        self.ui.lineEditLieuActeNaissance.clear()
        self.ui.lineEditNumDemande.clear()
        self.ui.lineEditNumCertificat.clear()
        #disable some lineEdit
        self.ui.lineEditNumCertificat.setEnabled(False)
        self.ui.lineEditNumDemande.setEnabled(False)
        if self.cv is not None:
            self.ui.horizontalLayout_.removeWidget(self.cv)

    def fillComboCategorieParcelle(self):
        self.idCategories[:] = []
        self.ui.comboBoxCategorieParcelle.clear()
        self.cur.execute("SELECT * FROM categorie")
        results = self.cur.fetchall()
        for result in results:
            self.ui.comboBoxCategorieParcelle.addItem(unicode(result[1]), result[0])
            self.idCategories.append(result[0])

    def fillComboCategorieBatiment(self):
        self.idCategoriesBatiment[:] = []
        self.ui.comboBoxCategorieBatiment.clear()
        self.cur.execute("SELECT * FROM categorie")
        results = self.cur.fetchall()
        for result in results:
            self.ui.comboBoxCategorieBatiment.addItem(unicode(result[1]), result[0])
            self.idCategoriesBatiment.append(result[0])

    def fillComboConsistance(self):
        self.idConsistances[:] = []
        self.idConsistancesBatiment[:] = []
        self.ui.comboBoxConsistanceParcelle.clear()
        self.ui.comboBoxConsistanceBatiment.clear()
        self.cur.execute("SELECT * FROM consistance WHERE parcelleoubatiment = 'parcelle'")
        results = self.cur.fetchall()
        for result in results:
            self.ui.comboBoxConsistanceParcelle.addItem(str(result[1]), result[0])
            self.idConsistances.append(result[0])

        self.cur.execute("SELECT * FROM consistance WHERE parcelleoubatiment = 'batiment'")
        results = self.cur.fetchall()
        for result in results:
            self.ui.comboBoxConsistanceBatiment.addItem(str(result[1]), result[0])
            self.idConsistancesBatiment.append(result[0])

    def fillComboPosition(self):
        self.ui.positionComboBox.clear()
        self.cur.execute("SELECT * FROM pointscardinaux")
        results = self.cur.fetchall()
        for result in results:
            self.idPointCardinaux.append(result[0])
            self.ui.positionComboBox.addItem(str(result[1]), result[0])

    def getSurface(self):
        SQL = "SELECT ST_Area(geom) FROM parcelle_d WHERE gid = %s;"
        param = (self.currId,)
        try:
            self.cur.execute(SQL, param)
            data = self.cur.fetchone()
            print "affichage de la surface"
            ac = AreaConvert()
            self.areaSqm = round(data[0], 2)
            Area = ac.convertArea(data[0], 'sqmeter', 'Ha')
            print "fin affichage"
            #print Area
            self.areaHa = ac.convertAreaToHa(data[0])
            #self.areaHa = str(Area['Ha'])+ " Ha " + str(Area['a']) + " a " + str(Area['Ca']) + " Ca "
            print self.areaHa
            self.ui.lineEditSurfaceM2.setText(str(self.areaSqm))
            self.ui.lineEditSurfaceHa.setText(str(self.areaHa).strip())
            print "Apres affichage"
        except StandardError as e:
            print e

    def showInTable(self, data):
        self.ui.tableWidgetLimites.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetLimites.rowCount()
            self.ui.tableWidgetLimites.insertRow(rowPosition)
            #self.idPersonnePhysiques.append(data[i][0])
            j = 1
            while j < len(data[i]) :
                self.ui.tableWidgetLimites.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def showInTableBatiment(self, data):
        self.ui.tableWidgetBatiment.setRowCount(0)

        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidgetBatiment.rowCount()
            self.ui.tableWidgetBatiment.insertRow(rowPosition)
            # self.idPersonnePhysiques.append(data[i][0])
            j = 0
            while j < len(data[i]) - 1:
                if j == 0:
                    self.ui.tableWidgetBatiment.setItem(rowPosition, j, QTableWidgetItem(unicode(data[i][j])))
                else:
                    self.ui.tableWidgetBatiment.setItem(rowPosition, j + 1, QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def zoomToSelLayer(self):
        vtlayer = self.registry.mapLayersByName("Fiscalite")[0]
        self.canvas.setCurrentLayer(vtlayer)
        cLayer = self.canvas.currentLayer()
        for layer in self.canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
        self.canvas.refresh()
        cLayer.select(int(self.currId))
        self.canvas.zoomToSelected(cLayer)

    def readInput(self, edition = None):
        data = {}

        data['categorieparcelle'] = self.idCategories[self.ui.comboBoxCategorieParcelle.currentIndex()]
        if self.ui.radioButtonSRI.isChecked():
            data['srisra'] = "sri"
        elif self.ui.radioButtonSRA.isChecked():
            data['srisra'] = "sra"

        if self.ui.lineEditCode.text() != "":
            data['code'] = unicode(self.ui.lineEditCode.text()).encode('utf-8')
        data['obs'] = unicode(self.ui.plainTextEditObservation.toPlainText()).encode('utf-8')

        if self.ui.radioButtonTitree.isChecked():
            data['numtitre'] = unicode(self.ui.lineEditNumero.text()).encode('utf-8')
            data['etatparcelle'] = 1
            self.writeData(data, 0, edition)
        elif self.ui.radioButtonCadastre.isChecked() or self.ui.radioButtonAucun.isChecked():
            if self.ui.radioButtonCadastre.isChecked():
                data['etatparcelle'] = 2
            elif self.ui.radioButtonAucun.isChecked():
                data['etatparcelle'] = 0
            data['numparcelle'] = unicode(self.ui.lineEditNumero.text()).encode('utf-8')
            self.writeData(data, 1, edition)
        elif self.ui.radioButtonCertifie.isChecked():
            data['etatparcelle'] = 3
            data['numcertificat'] = unicode(self.ui.lineEditNumero.text()).encode('utf-8')
            self.writeData(data, 2, edition)

    def fillTableBatiment(self):
        rowPosition = self.ui.tableWidgetBatiment.rowCount()
        self.ui.tableWidgetBatiment.insertRow(rowPosition)
        infoBatiment = []
        infoBatiment.append(unicode(self.ui.lineEditCode.text()).encode('utf-8'))
        infoBatiment.append(self.idCategoriesBatiment[self.ui.comboBoxCategorieBatiment.currentIndex()])
        infoBatiment.append(self.idConsistancesBatiment[self.ui.comboBoxConsistanceBatiment.currentIndex()])
        if self.ui.lineEditSurfaceBatiment.text() == "":
            infoBatiment.append(0)
        else:
            infoBatiment.append(float(self.ui.lineEditSurfaceBatiment.text()))
        if self.ui.lineEditNbrPieces.text() == "":
            infoBatiment.append(0)
        else:
            infoBatiment.append(int(self.ui.lineEditNbrPieces.text()))
        self.ui.tableWidgetBatiment.setItem(rowPosition, 0, QTableWidgetItem(self.ui.lineEditCode.text()))
        self.ui.tableWidgetBatiment.setItem(rowPosition, 1, QTableWidgetItem(self.ui.comboBoxCategorieBatiment.currentText()))
        self.ui.tableWidgetBatiment.setItem(rowPosition, 2, QTableWidgetItem(self.ui.comboBoxConsistanceBatiment.currentText()))
        self.ui.tableWidgetBatiment.setItem(rowPosition, 3, QTableWidgetItem(self.ui.lineEditSurfaceBatiment.text()))
        self.ui.tableWidgetBatiment.setItem(rowPosition, 4, QTableWidgetItem(self.ui.lineEditNbrPieces.text()))

        self.ui.lineEditCode.clear()
        self.ui.lineEditSurfaceBatiment.clear()
        self.ui.lineEditNbrPieces.clear()
        self.ui.comboBoxConsistanceBatiment.setCurrentIndex(0)
        self.ui.comboBoxCategorieBatiment.setCurrentIndex(0)

        self.infosBatiments.append(infoBatiment)
        print self.infosBatiments

    def fillInfoBatFromTable(self):
        i = 0
        infoBatiment = []
        while i < self.ui.tableWidgetBatiment.rowCount():
            j = 0
            while j < 5:
                item = self.ui.tableWidgetBatiment.item(i, j)
                if item is not None:
                    itemData = str(item.data(0).toString())
                    infoBatiment.append(itemData)
                j = j + 1
            i = i + 1
        #print self.infosBatiments

    def deleteOneBat(self):
        if self.ui.tableWidgetBatiment.currentRow() == -1:
            QMessageBox.critical(self, u"Suppression d'un batiment", u"Veuillez au moins séléctionner une ligne dans le tableau")
        else:
            row = self.ui.tableWidgetBatiment.currentRow()
            codeBat = self.ui.tableWidgetBatiment.item(row, 0).data(0).toString()
            #self.ui.tableWidgetBatiment.removeRow(row)
            try:
                self.cur.execute("DELETE FROM batiment WHERE codebatiment = %s", (str(codeBat),))
                self.connection.commit()
                # afficher les batiments sur la parcelle ##
                try:
                    self.cur.execute(
                        "SELECT b.codebatiment,c.libelleconsistance, b.surfacebatiment, b.nbpiecebatiment, b.idparcelle  FROM batiment b, consistance c WHERE b.idconsistance = c.idconsistance AND b.idparcelle = %s",
                        (self.currId,))
                    bats = self.cur.fetchall()
                    self.infosBatiments[:] = []
                    for bat in bats:
                        if bat not in self.infosBatiments:
                            self.infosBatiments.append(bat)
                    print self.infosBatiments
                    self.showInTableBatiment(bats)
                except StandardError as e:
                    self.connection.rollback()
                    print(e)
                #self.showInTableBatiment()
            except StandardError as e:
                self.connection.rollback()
                print(e)

    def addOneBat(self):
        rowPosition = self.ui.tableWidgetBatiment.rowCount()
        infoBatiment = []
        infoBatiment[:] = []
        infoBatiment.append(str(self.ui.lineEditCodeBatiment.text()).encode('utf-8'))
        infoBatiment.append(self.idCategoriesBatiment[self.ui.comboBoxCategorieBatiment.currentIndex()])
        infoBatiment.append(self.idConsistancesBatiment[self.ui.comboBoxConsistanceBatiment.currentIndex()])
        if self.ui.lineEditSurfaceBatiment.text() == "":
            infoBatiment.append(0)
        else:
            infoBatiment.append(float(self.ui.lineEditSurfaceBatiment.text()))
        if self.ui.lineEditNbrPieces.text() == "":
            infoBatiment.append(0)
        else:
            infoBatiment.append(int(self.ui.lineEditNbrPieces.text()))

        if self.currId is not None:
            infoBatiment.append(self.currId)


        #self.infosBatiments.append(infoBatiment)

        try:
            self.cur.execute(
                "INSERT INTO public.batiment (codebatiment, idparcelle, idconsistance, surfacebatiment, nbpiecebatiment ) VALUES (%s, %s, %s, %s, %s)",
                (infoBatiment[0], infoBatiment[5], infoBatiment[2],
                 infoBatiment[3], infoBatiment[4]))
            self.connection.commit()
            self.ui.tableWidgetBatiment.insertRow(rowPosition)
            self.ui.tableWidgetBatiment.setItem(rowPosition, 0, QTableWidgetItem(self.ui.lineEditCode.text()))
            self.ui.tableWidgetBatiment.setItem(rowPosition, 1,
                                                QTableWidgetItem(self.ui.comboBoxCategorieBatiment.currentText()))
            self.ui.tableWidgetBatiment.setItem(rowPosition, 2,
                                                QTableWidgetItem(self.ui.comboBoxConsistanceBatiment.currentText()))
            self.ui.tableWidgetBatiment.setItem(rowPosition, 3,
                                                QTableWidgetItem(self.ui.lineEditSurfaceBatiment.text()))
            self.ui.tableWidgetBatiment.setItem(rowPosition, 4, QTableWidgetItem(self.ui.lineEditNbrPieces.text()))

            self.ui.lineEditCode.clear()
            self.ui.lineEditSurfaceBatiment.clear()
            self.ui.lineEditNbrPieces.clear()
            self.ui.comboBoxConsistanceBatiment.setCurrentIndex(0)
            self.ui.comboBoxCategorieBatiment.setCurrentIndex(0)
            # afficher les batiments sur la parcelle ##
            try:
                self.cur.execute(
                    "SELECT b.codebatiment,c.libelleconsistance, b.surfacebatiment, b.nbpiecebatiment, b.idparcelle  FROM batiment b, consistance c WHERE b.idconsistance = c.idconsistance AND b.idparcelle = %s",
                    (self.currId,))
                bats = self.cur.fetchall()
                self.infosBatiments[:] = []
                for bat in bats:
                    if bat not in self.infosBatiments:
                        self.infosBatiments.append(bat)
                print self.infosBatiments
                self.showInTableBatiment(bats)
            except StandardError as e:
                self.connection.rollback()
                print(e)
            #self.showInTableBatiment()
        except psycopg2.Error as e:
            print "Info batiment " + str(e)
            if e.pgcode == "23505":
                QMessageBox.critical(self, u"Erreur", u"Le code batiment existe déjà")
                self.connection.rollback()
        #print self.infosBatiments

    def addLimite(self):
        limiteparcelle = []
        limiteparcelle.append(self.idPointCardinaux[self.ui.positionComboBox.currentIndex()])
        #self.limitesParcelle.append(self.ui.positionComboBox.itemData(1))
        #print self.idsPositions
        rowPosition = self.ui.tableWidgetLimites.rowCount()
        # idpersonnes.append(data[i][0])
        #self.listeIdConsorts.append(self.currData[0])
        #print self.listeIdConsorts
        if self.ui.descriptionLineEdit.text() != "":
            limiteparcelle.append(unicode(self.ui.descriptionLineEdit.text()).encode('utf-8'))
            self.limitesParcelle.append(limiteparcelle)
            try:
                self.cur.execute("INSERT INTO limitesparcelle(idpointscardinaux, idparcelle, description) VALUES(%s, %s, %s)",
                                 (limiteparcelle[0], self.currId, limiteparcelle[1]))
                self.connection.commit()
                self.ui.tableWidgetLimites.insertRow(rowPosition)
                self.ui.tableWidgetLimites.setItem(rowPosition, 0, QTableWidgetItem(self.ui.positionComboBox.currentText()))
                self.ui.tableWidgetLimites.setItem(rowPosition, 1, QTableWidgetItem(self.ui.descriptionLineEdit.text()))
            except psycopg2.Error as e:
                print(e)
                if e.pgcode == "23505":
                    QMessageBox.critical(self, u"Erreur", u"La combinaison position et parcelle existe déjà")
                    self.connection.rollback()
        else:
            QMessageBox.critical(self, "Erreur", u"Le champ description doit être renseigné")

        #print self.limitesParcelle

        self.ui.descriptionLineEdit.clear()

    def deleteLimite(self):
        if self.ui.tableWidgetLimites.currentRow() == -1:
            QMessageBox.critical(self, u"Suppression d'une limire", u"Veuillez au moins séléctionner une ligne dans le tableau")
        else:
            row = self.ui.tableWidgetLimites.currentRow()
            position = self.ui.tableWidgetLimites.item(row, 0).data(0).toString()
            try:
                self.cur.execute("SELECT idpointscardinaux FROM pointscardinaux WHERE position = %s", (str(position),))
                idPointCardinal = self.cur.fetchone()
                print idPointCardinal
                self.ui.tableWidgetLimites.removeRow(row)
                try:
                    self.cur.execute("DELETE FROM limitesparcelle WHERE idpointscardinaux = %s and idparcelle = %s",
                                     (idPointCardinal[0], self.idparcelle))
                    self.connection.commit()
                    # afficher les limites sur la parcelle ##
                    try:
                        self.cur.execute(
                            "SELECT pc.idpointscardinaux, pc.position, l.description FROM limitesparcelle l, pointscardinaux pc WHERE l.idpointscardinaux = pc.idpointscardinaux AND l.idparcelle = %s",
                            (self.currId,))
                        limites = self.cur.fetchall()
                        print limites
                        self.showInTable(limites)
                        for limite in limites:
                            if limite not in self.infosBatiments:
                                self.limitesParcelle.append(limite)
                        print self.limitesParcelle
                        self.showInTable(limites)
                    except StandardError as e:
                        self.connection.rollback()
                        print(e)
                        # self.showInTableBatiment()
                except StandardError as e:
                    self.connection.rollback()
                    print(e)
            except StandardError as e:
                self.connection.rollback()
                print(e)

            print position



    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEditNumero.setValidator(validatorNum)
        self.ui.lineEditCode.setValidator(validatorAlphaNum)
        self.ui.lineEditAdresse.setValidator(validatorAlphaNum)
        self.ui.lineEditLieuNaissance.setValidator(validatorAlpha)
        self.ui.lineEditCIN1.setValidator(validatorNum)
        self.ui.lineEditCIN2.setValidator(validatorNum)
        self.ui.lineEditCIN3.setValidator(validatorNum)
        self.ui.lineEditCIN4.setValidator(validatorNum)
        self.ui.lineEditLieuCIN.setValidator(validatorAlphaNum)
        self.ui.lineEditNumActeNaissance.setValidator(validatorNum)
        self.ui.lineEditLieuActeNaissance.setValidator(validatorAlphaNum)
        #self.ui.lineEditNumParcelle.setValidator(validatorAlphaNum)
        self.ui.lineEditSurfaceM2.setValidator(validatorNum)
        self.ui.lineEditSurfaceHa.setValidator(validatorNum)
        self.ui.lineEditNbrPieces.setValidator(validatorNum)
        self.ui.lineEditSurfaceBatiment.setValidator(validatorNum)
        #self.ui.lineEditCIN.setMaxLength(3)
        self.ui.lineEditCIN1.setMaxLength(3)
        self.ui.lineEditCIN2.setMaxLength(3)
        self.ui.lineEditCIN3.setMaxLength(3)
        self.ui.lineEditCIN4.setMaxLength(3)

    def writeData(self, data, value, edition = None):
        idHameauC = None
        if self.ui.comboBoxHameau.currentIndex() != -1:
            idHameauC = self.idHameau[self.ui.comboBoxHameau.currentIndex()]
        else:
            QMessageBox.critical(self, "Erreur sur hameau", u"Veuillez séléctionner un Hameau ")
        if idHameauC is not None:
            try:
                if value == 0: # Parcelle titree
                    self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idhameau = %s, has_data = TRUE, srisraparcelle = %s, etatparcelle_d = %s WHERE gid = %s",(data['numtitre'], data['code'], data['categorieparcelle'],idHameauC, data['srisra'],data['etatparcelle'], self.currId))
                    self.connection.commit()
                elif value == 1: # parcelle cadastree
                    self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idhameau = %s, has_data = TRUE, srisraparcelle = %s, etatparcelle_d = %s WHERE gid = %s",(data['numparcelle'], data['code'], data['categorieparcelle'],idHameauC, data['srisra'],data['etatparcelle'], self.currId))
                    self.connection.commit()
                elif value == 2: # parcelle certifiee
                    self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idhameau = %s, has_data = TRUE, srisraparcelle = %s, etatparcelle_d = %s WHERE gid = %s",(data['numcertificat'], data['code'], data['categorieparcelle'], idHameauC, data['srisra'],data['etatparcelle'], self.currId))
                    self.connection.commit()

                i = 0
                try:
                    #print "TAKING CARE OF THE PERSONS"
                    if self.idConsorts is not None:
                        self.cur.execute("DELETE FROM contribuables_parcelle WHERE idparcelle = %s ", (self.idparcelle,))
                        self.connection.commit()
                        consortsDeleted = True

                        for idcons in self.idConsorts:
                            print "id consort = " + str(idcons)
                            try:
                                self.cur.execute("INSERT INTO contribuables_parcelle (idpersonne, idparcelle, contribuable) VALUES (%s, %s, %s)", (idcons, self.idparcelle, False))
                                self.connection.commit()
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()
                    try:
                        if self.idContribuable is not None:
                            print "id contribuable = " + str(self.idContribuable)
                            self.cur.execute("INSERT INTO contribuables_parcelle (idpersonne, idparcelle, contribuable) "
                                                 "VALUES (%s, %s, %s)",(self.idContribuable, self.idparcelle, True) )
                            self.connection.commit()
                    except psycopg2.Error as e:
                        print(e)
                        if e.pgcode == "2305":
                            try:
                                self.cur.execute("UPDATE contribuables_parcelle idpersonne = %s "
                                             "WHERE idparcelle = %s AND contribuable = %s",
                                             (self.idContribuable, self.idparcelle, True))
                                self.connection.commit()
                            except StandardError as e:
                                print (e)
                        self.connection.rollback()

                except StandardError as e:
                    print(e)
                    self.connection.rollback()
                #msgBox = QMessageBox()
                #msgBox.setText("Enregistrement de la parcelle fiplof reussi")
                #msgBox.show()
                #msgBox.exec_()
                print edition
                if not edition:
                    QMessageBox.information(self, u"Parcelle avec données", "Enregistrement de la parcelle reussi")
                self.refreshCanvas()
                #self.close()
            except StandardError as e:
                print "Enregistrement parcelle " + str(e)
                self.connection.rollback()

    def refreshCanvas(self):

        for layer in self.canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()

        self.canvas.refresh()

    def ouvrirListeContribuable(self):
        self.listeContribuable.isFromConsort()
        self.listeContribuable.exec_()

    def getContribuableInfo(self):
        idContribuable = self.listeContribuable.selectContribuable()
        self.idContribuable =  idContribuable
        self.getAllConsorts(self.idContribuable)
        self.getContribuableById(idContribuable)
        self.listeContribuable.close()

    def getAllConsorts(self, idcontribuable):
        try:
            self.cur.execute("SELECT nom,prenom, cin,numactenaissance, idcontribuable FROM contribuable  WHERE idcontribuable IN "
                             "(SELECT idconsort FROM contribuableconsorts c WHERE c.idcontribuable = %s)", (idcontribuable,))
            contribuables = self.cur.fetchall()
            print contribuables
            self.fillTableConsorts(contribuables)
        except StandardError as e:
            print e
            self.connection.rollback()

    def fillTableConsorts(self, data):
        self.idConsorts[:] = []
        self.ui.tableWidgetConsorts.setRowCount(0)
        for value in data:
            #print value
            self.idConsorts.append(value[4])
            rowPosition = self.ui.tableWidgetConsorts.rowCount()
            self.ui.tableWidgetConsorts.insertRow(rowPosition)
            j = 0
            while j < len(value) - 1:
                print value[j]
                if value[j] is not None:
                    self.ui.tableWidgetConsorts.setItem(rowPosition, j, QTableWidgetItem(value[j]))
                j = j + 1

    def selectionLigneConsort(self, row):
        self.selectedId = self.idConsorts[row]
        self.contribuable.getContribuableById(self.selectedId)

    def ouvrirListeConsorts(self):
        self.listeConsorts.exec_()

    def showConsort(self):
        if self.selectedId is not None:
            self.contribuable.estConsultation(1)
            self.contribuable.exec_()
        else:
            QMessageBox.critical(self, "Erreur", u"Veuillez séléctionner une ligne dans le tableau")

    def editConsort(self):
        if self.selectedId is not None:
            self.contribuable.estConsultation(0)
            self.contribuable.exec_()
        else:
            QMessageBox.critical(self, "Erreur", u"Veuillez séléctionner une ligne dans le tableau")














