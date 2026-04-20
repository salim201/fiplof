#coding: utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2
from models.ProjetCouche import ProjetCouche

from .CreationPropositionDomainePublic import Ui_Dialog


class PropositionDoaminePublique(QDialog):
    def __init__(self, connection,canvas, parent, edit = None):
        self.connection = connection
        self.initDB()
        QDialog.__init__(self)
        from Configuration import DbConfig
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.parent = parent
        self.tool = parent.tool
        self.iddomaine = parent.iddomaine
        self.filenamepreview = ""
        self.edit = edit
        self.initDB()
        self.initActions()
        self.ui.btnAide.hide()
        #self.initPreview()
        self.readData()
        if edit == 0:
            self.ui.btnCreer.hide()
            self.disableAll()
        elif edit == 1:
            self.ui.btnCreer.setText(u"Modifier les informations")
        elif edit == 2:
            self.ui.btnCreer.setText(u"Modifier la géométrie")
            self.tool = parent.tool

        self.db_config = DbConfig.DbConfig()

        self.raster_path, self.layer_raster, self.layer_shape, self.rect = None, None, None, None
        # self.id_projet = self.parent.id_projet
        self.init_layers()
        self.load_raster()
        self.init_canvas()

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
            u'outline_width': u'0.3', u'outline_color': u'255,228,196,255', u'offset_unit': u'MM',
            u'color': u'0,255,169,255', u'outline_style': u'solid', u'style': u'b_diagonal',
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
        uri.setDataSource("public", "domainepublique", "geom", "iddomainepublique=%s" % (self.iddomaine,))
        uri.setKeyColumn("gid")
        layer = QgsVectorLayer(uri.uri(), "Domainepublique", "postgres")
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
        if self.edit == 0 or self.edit == 1 or self.edit is None:
            self.ui.btnCreer.clicked.connect(self.readInput)
        else:
            self.ui.btnCreer.clicked.connect(self.editGeom)

    def readInput(self):
        data = {}
        #data['type'] = unicode(self.ui.comboBoxType.currentText()).encode('utf-8')
        data['nom'] = unicode(self.ui.lineEditNom.text()).encode('utf-8')
        #data['lineEditNomPropriete'] = unicode(self.ui.lineEditNom.text()).encode('utf-8')
        data['observation'] = unicode(self.ui.textEditObservation.toPlainText()).encode('utf-8')
        self.writeData(data)

    def writeData(self, data):
        try:
            self.cur.execute('UPDATE domainepublique SET nom = %s, observation = %s WHERE iddomainepublique = %s', (data['nom'], data['observation'], self.iddomaine))
            self.connection.commit()

            if self.edit == 1:
                self.parent.showAll()
                QMessageBox.information(self, u"Proposition domaine publique", u"Modification de proposition de domaine publique reussi")
            elif self.edit == 2:
                QMessageBox.information(self, u"Proposition domaine publique", u"Modification de proposition de domaine publique reussi")
            else:
                QMessageBox.information(self, u"Proposition domaine publique", u"Création de proposition de domaine publique reussi")
            self.refreshCanvas()
            self.close()
            #self.close()
        except StandardError as e:
            self.connection.rollback()
            print(e)

    def preview(self): ####----utile pour afficher la geometrie ---####
        print "preview"
        sql = "SELECT ST_AsPNG(" \
                "ST_AsRaster(" \
                "ST_Buffer(geom, 10),200,200,ARRAY['8BUI', '8BUI', '8BUI'], ARRAY[118,154,118], ARRAY[0,0,0]" \
                ")) png " \
                "from domainepublique WHERE iddomainepublique=%s"
            #        cursor = connection.cursor()
        #print sql
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #print "apres creation cursor"
        cursor.execute("SET bytea_output TO escape")
        #print "excute voaloany"
        cursor.execute(sql, (self.iddomaine,))
        #print "Avant ouverture du fichier"
        row = cursor.fetchone()
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
            self.cur.execute("SELECT nom, observation FROM domainepublique WHERE iddomainepublique = %s ", (self.iddomaine,))
            data = self.cur.fetchone()
            self.useData(data)
        except StandardError as e:
            print e

    def useData(self, data):
        if data[0] is not None:
            self.ui.lineEditNom.setText(str(data[0]).strip())
        if data[1] is not None:
            self.ui.textEditObservation.setText(str(data[1]).strip())

    def editGeom(self):
        # Ecriture dans le journal
        from Projet.journalRunn import journal
        journal = journal(self.connection)
        journal.inserToJournal(globalvars.id_user, self.iddomaine, u"Proposition aire à statuts specifiques",
                               u"Edition de la géometrie d'une proposition d'un aire à statuts specifique")
        # fin ecritude dans le journal
        self.close()
        try:
            self.parent.close()
        except:
            pass
        self.canvas.setMapTool(self.tool)
        self.parent.activateChangeOngeom.setEnabled(True)

    def disableAll(self):
        self.ui.lineEditNom.setEnabled(False)
        self.ui.textEditObservation.setEnabled(False)


    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()


