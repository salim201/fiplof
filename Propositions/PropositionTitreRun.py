#coding: utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time, os
import globalvars, sys, psycopg2
from models.ProjetCouche import ProjetCouche

from AreaConvert import AreaConvert
from .CreationPropositionTitre import Ui_Dialog


class PropositionTitre(QDialog):
    def __init__(self, connection,canvas, parent, edit = None):
        self.connection = connection
        QDialog.__init__(self)
        from Configuration import DbConfig
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.edit = edit
        self.setWindowTitle(u"Création de proposition de titre")
        self.filenamepreview = ""
        self.canvas = canvas
        self.idtitre = parent.idtitre
        self.parent = parent
        self.registry = parent.registry
        self.ui.btnAide.hide()
        #print parent.layers
        self.idsFokontany = []
        self.idOccupant = []
        self.initDB()
        self.initActions()
        if edit == 0:
            self.ui.btnCreer.hide()
            self.setWindowTitle(u"Consultation d'une proposition de titre")
            self.ui.lineEditNom.hide()
            self.ui.label_13.hide()
            self.disableAll()
        elif edit == 1:
            self.ui.btnCreer.setText(u"Modifier les informations")
        elif edit == 2:
            self.ui.btnCreer.setText(u"Modifier la géométrie")
            self.tool = parent.tool
        from Certificat.ListeConsistanceRun import ListeConsistanceRun
        self.listeConsist = ListeConsistanceRun(self.connection)
        self.fillConsistance()
        self.calculAire()
        self.fillTerritoitre()
        #self.initPreview()
        self.readData()
        self.db_config = DbConfig.DbConfig()

        self.raster_path, self.layer_raster, self.layer_shape, self.rect = None, None, None, None
        # self.id_projet = self.parent.id_projet
        self.init_layers()
        self.load_raster()
        self.init_canvas()
        vtlayer = self.registry.mapLayersByName("Proposition de titre")[0]
        self.canvas.setCurrentLayer(vtlayer)

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
            u'outline_width': u'0.3', u'outline_color': u'255,0,174,255', u'offset_unit': u'MM',
            u'color': u'58,226,206,255', u'outline_style': u'solid', u'style': u'b_diagonal',
            u'joinstyle': u'bevel', u'outline_width_unit': u'MM', u'border_width_map_unit_scale': u'0,0',
            u'offset': u'0,0', u'offset_map_unit_scale': u'0,0'
        }
        self.cv = QgsMapCanvas()
        # self.idparcelle;
        # add canvas  ad form
        self.ui.horizontalLayoutGeom.addWidget(self.cv)
        self.cv.show()
        uri = QgsDataSourceURI()
        uri.setConnection(
            self.db_config.db_host,
            self.db_config.db_port,
            self.db_config.db_name,
            self.db_config.db_user,
            self.db_config.db_pass
        )
        uri.setDataSource("public", "titrefoncier", "geom", "gid=%s" % (self.idtitre,))
        uri.setKeyColumn("gid")
        layer = QgsVectorLayer(uri.uri(), "Titrefoncier", "postgres")
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
        #self.ui.btnCreer.clicked.connect(self.readInput)
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.ui.btnListe.clicked.connect(self.ouvrirListeConsistance)
        self.ui.btnListe_2.clicked.connect(self.ouvrirListeFokontany)
        self.ui.btnAjouter.clicked.connect(self.ajoutOccupant)
        #self.ui.btnCreer.clicked.connect(self.creerPropositionTitre)
        if self.edit == 0 or self.edit == 1 or self.edit is None:
            self.ui.btnCreer.clicked.connect(self.readInput)
        else:
            self.ui.btnCreer.clicked.connect(self.editGeom)


    def readInput(self):
        data = {}
        data['type'] = str(self.ui.comboBoxType.currentText()).encode('utf-8')
        data['numero'] = str(self.ui.lineEditNumTitre.text()).encode('utf-8')
        data['lineEditNomPropriete'] = str(self.ui.lineEditNomPropriete.text()).encode('utf-8')
        data['consistance'] = str(self.ui.comboBoxConsistance.currentText()).encode('utf-8')
        data['observation'] = str(self.ui.textEditObservation.toPlainText()).encode('utf-8')
        self.writeData(data)

    def writeData(self, data):
        try:
            self.cur.execute('UPDATE titrefoncier SET numerotitre = %s, typetitre = %s, nompropriete = %s, consistance = %s, observation = %s WHERE gid = %s', (data['numero'], data['type'], data['lineEditNomPropriete'], data['consistance'], data['observation'], self.idtitre))
            self.connection.commit()
            #self.close()
        except StandardError as e:
            self.connection.rollback()
            print(e)
        self.creerPropositionTitre()

    def ouvrirListeConsistance(self):
        #Requete pour recuperer la liste des consistances
        SQL = "SELECT libelleconsistance FROM consistance"
        self.cur.execute(SQL)
        data = self.cur.fetchall()
        self.listeConsist.setData(data)
        self.listeConsist.show()
        result = self.listeConsist.exec_()

    def fillConsistance(self):
        self.ui.comboBoxConsistance.clear()
        try:
            self.cur.execute("SELECT * FROM consistance")
            data = self.cur.fetchall()
            for value in data:
                self.ui.comboBoxConsistance.addItem(value[1])
        except StandardError as e:
            print(e)

    def calculAire(self):
        try:
            self.cur.execute("SELECT ST_Area(geom) FROM titrefoncier WHERE gid = %s ", (self.idtitre,))
            surface = self.cur.fetchone()
            print "affichage de la surface"
            surfacem2 = round(surface[0], 2)
            self.ui.lineEditSurfaceM2.setText(str(surfacem2))
            ac = AreaConvert()
            # Area = ac.convertArea(float(data[4]), 'sqmeter', 'Ha')
            Area = ac.convertArea(float(surface[0]), 'sqmeter', 'Ha')
            print "fin affichage"
            print Area
            # Afficher la surface
            print "surface en Ha"
            print Area['Ha']
            self.ui.lineEditSurfaceHa.setText(str(Area['Ha']))
            self.ui.lineEditSurfaceCa.setText(str(Area['Ca']))
            self.ui.lineEditSurfaceA.setText(str(Area['a']))
        except StandardError as e:
            print(e)

    def fillTerritoitre(self):
        # Recuperer le nom de la commune
        try:
            self.cur.execute("SELECT nomcommune, codecommune FROM commune WHERE idcommune = %s", (globalvars.id_commune, ))
            com = self.cur.fetchone()
            self.ui.comboBoxCommune.addItem(com[0])
            if self.ui.comboBoxCommune.count() > 0:
                self.ui.comboBoxCommune.setCurrentIndex(0)
        except StandardError as e:
            print e
        # Recuperer le district
        try:
            self.cur.execute("SELECT d.nomdistrict, d.iddistrict, d.codedistrict FROM district d, commune c WHERE d.iddistrict = c.iddistrict AND c.idcommune = %s", (globalvars.id_commune, ))
            dist = self.cur.fetchone()
            self.ui.comboBoxDistrict.addItem(dist[0])
        except StandardError as e:
            print e
        # Region
        #try:
         #   self.cur.execute("SELECT r.nomregion FROM region r, district d WHERE d.idregion = r.idregion AND d.iddistrict = %s", (dist[1],))
          #  reg = self.cur.fetchone()
           # self.ui.comboBoxRegion.addItem(reg[0])
        #except StandardError as e:
        #    print e
        try:
            self.cur.execute("SELECT nomfokontany, idfokontany, codefokontany FROM fokontany WHERE idcommune = %s", (globalvars.id_commune,))
            fkts = self.cur.fetchall()
            for fkt in fkts:
                self.ui.comboBoxFokontany.addItem(fkt[0], fkt[1])
                self.idsFokontany.append(fkt[1])
        except StandardError as e:
            print e

    def ouvrirListeFokontany(self):
        from Parametres.FokontanyRun import FokontanyRun
        fkt = FokontanyRun(self.connection)
        fkt.exec_()

    def ajoutOccupant(self):
        if len(str(self.ui.lineEditNom.text()).strip()) > 0:
            rowposition = self.ui.tableWidget.rowCount()
            print rowposition
            self.ui.tableWidget.insertRow(rowposition)
            nom = unicode(self.ui.lineEditNom.text()).encode('utf-8')
            try:
                self.ui.tableWidget.setItem(rowposition, 0, QTableWidgetItem(nom))
            except StandardError as e:
                print e

            try:
                self.cur.execute("INSERT INTO occupant(nom) VALUES(%s) returning idoccupant ", (nom, ))
                self.connection.commit()
                id = self.cur.fetchone()
                self.idOccupant.append(id[0])
            except StandardError as e:
                self.connection.rollback()
                print(e)

    def creerPropositionTitre(self):
        i = 0
        print self.idOccupant
        print self.idtitre
        while i < len(self.idOccupant):
            try:
                self.cur.execute("INSERT INTO occupant_titrefoncier(idtitrefoncier, idoccupant) VALUES(%s, %s)",(self.idtitre, self.idOccupant[i]))
                self.connection.commit()
                print "Enregistrement"
            except StandardError as e:
                self.connection.rollback()
                print(e)
            i = i + 1
        if self.edit == 0:
            QMessageBox.information(self, u"Proposition titre", u"Création de proposition de titre reussi")
        elif self.edit == 1:
            QMessageBox.information(self, u"Proposition titre", u"Modification de la proposition de titre reussi")
            self.parent.showAll()
            self.refreshCanvas()
        #self.parent.close()
        self.close()

    def preview(self): ####----utile pour afficher la geometrie ---####
        print "preview"
        sql = "SELECT ST_AsPNG(" \
                "ST_AsRaster(" \
                "ST_Buffer(geom, 10),200,200,ARRAY['8BUI', '8BUI', '8BUI'], ARRAY[118,154,118], ARRAY[0,0,0]" \
                ")) png " \
                "from titrefoncier WHERE gid=%s"
            #        cursor = connection.cursor()
        #print sql
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #print "apres creation cursor"
        row = []
        try:
            cursor.execute("SET bytea_output TO escape")
            #print "excute voaloany"
            cursor.execute(sql, (self.idtitre,))
            #print "Avant ouverture du fichier"
            row = cursor.fetchone()
        except StandardError as e:
            print e

        filename = "preview.png"
        try:
            #print "ouverture fichier"
            f = open(filename, "wb")
            f.write(row['png'])
            f.close()
        except StandardError as e:
            print e
        cursor.close()
        return filename

    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)

    def refreshCanvas(self):

        for layer in self.canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()

        self.canvas.refresh()

    def initPreview(self):
        self.filenamepreview = self.preview()
        os.chdir(self.resolve(".."))
        dr = os.getcwd()
        sys.path.append(os.path.dirname(dr))
        self.ui.labelGeom.setPixmap(QtGui.QPixmap(self.filenamepreview))

    def readData(self):
        try:
            self.cur.execute("SELECT numerotitre, nompropriete, observation, typetitre FROM titrefoncier WHERE gid = %s ", (self.idtitre,))
            data = self.cur.fetchone()
            self.useData(data)
        except StandardError as e:
            print e

    def useData(self, data):
        if data[0] is not None:
            self.ui.lineEditNumTitre.setText(str(data[0]).strip())
        if data[2] is not None:
            self.ui.textEditObservation.setText(str(data[2]).strip())
        if data[1] is not None:
            self.ui.lineEditNomPropriete.setText(str(data[1]).strip())
        if data[3] is not None:
            self.ui.comboBoxType.setCurrentIndex(self.ui.comboBoxType.findText(str(data[3]).strip()))
        try:
            self.cur.execute("SELECT occ.nom FROM occupant occ, occupant_titrefoncier ot, titrefoncier t "
                             "WHERE occ.idoccupant = ot.idoccupant AND t.gid = ot.idtitrefoncier AND t.gid = %s ",
                             (self.idtitre,))
            occupants = self.cur.fetchall()
            for occupant in occupants:
                nom = occupant[0]
                rowposition = self.ui.tableWidget.rowCount()
                print rowposition
                self.ui.tableWidget.insertRow(rowposition)
                #nom = unicode(self.ui.lineEditNom.text()).encode('utf-8')
                try:
                    self.ui.tableWidget.setItem(rowposition, 0, QTableWidgetItem(nom))
                except StandardError as e:
                    print e

        except StandardError as e:
            print(e)

    def editGeom(self):
        # Ecriture dans le journal
        from Projet.journalRunn import journal
        journal = journal(self.connection)
        journal.inserToJournal(globalvars.id_user, self.idtitre, u"Proposition titre foncier",
                               u"Edition de la géometrie d'une proposition d'un aire à statuts specifique")
        # fin ecritude dans le journal
        self.close()
        try:
            self.parent.close()
        except:
            pass
        self.parent.parent.parent.setCurrLayerIndicator(1)
        self.canvas.setMapTool(self.tool)
        self.parent.activateChangeOngeom.setEnabled(True)

    def disableAll(self):
        self.ui.comboBoxType.setEnabled(False)
        self.ui.lineEditNumTitre.setEnabled(False)
        self.ui.lineEditNomPropriete.setEnabled(False)
        self.ui.comboBoxConsistance.setEnabled(False)
        self.ui.lineEditSurfaceM2.setEnabled(False)
        self.ui.lineEditSurfaceHa.setEnabled(False)
        self.ui.lineEditSurfaceA.setEnabled(False)
        self.ui.lineEditSurfaceCa.setEnabled(False)
        self.ui.comboBoxFokontany.setEnabled(False)
        self.ui.comboBoxCommune.setEnabled(False)
        self.ui.comboBoxDistrict.setEnabled(False)
        self.ui.tableWidget.setEnabled(False)
        self.ui.btnListe.setEnabled(False)
        self.ui.btnListe_2.setEnabled(False)
        self.ui.btnAjouter.setEnabled(False)
        self.ui.btnEnlever.setEnabled(False)


    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()


