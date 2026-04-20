# -*- coding: utf-8 -*-
from Etats.codegenerator.QrCodeGenerator import QrCodeGenerator
from PyQt4 import QtGui, Qt
from PyQt4.Qt import QApplication
from .OriginalCertificat import Ui_Dialog
from .CertificatFoncierRun import CertificatFoncierRun
from PgCrud import PgSql
from Configuration import DbConfig
import psycopg2
import psycopg2.extras
from Utilisateur import AccesManager
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import QMessageBox
from models.ProjetCouche import ProjetCouche
import globalvars

class OriginalCertificatRun(QtGui.QDialog):
    def __init__(self, canvas,parent):
        config = DbConfig.DbConfig()
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        appStyle = """  
                QTableWidget 
                {

        	        alternate-background-color: #00bfff;
             	    background-color: white;
                }
                """
        self.setStyleSheet(appStyle)

        self.parent = parent
        self.isprint = self.parent.isprint
        self.canvas = canvas
        self.geomid = None
        self.idCF = 0
        self.setupFieldsStatus()
        self.connection = psycopg2.connect(database=config.db_name, user=config.db_user, password=config.db_pass,
                                           host=config.db_host)
        

        self.pgsql = PgSql.Table(self.connection, "certificat")
        self.pgsql.addColumn("certificat.idcertificat", "ID_CERTIFICAT", alias="idcertificat", readonly=True)
        self.pgsql.addColumn("numerocertificat", "NUM CERTIFICAT", readonly=True)
        self.pgsql.addColumn("certificat.datereconnaissance", "DATE RECONNAISSANCE", alias="datereconnaissance", readonly=True)
        self.pgsql.addColumn("typecertificat", "TYPE CERTIFICAT", readonly=True)
        self.pgsql.addColumn("gid", "Geometrie ID", readonly=True)
        cursor = self.connection.cursor()
        ordonable = False
        try:
            cursor.execute("SELECT CAST(TRIM(SPLIT_PART(numerocertificat,'-','4')) as integer) FROM certificat")
            ordonable = True
        except Exception as err:
            self.connection.rollback()
            pass
        cursor.close()
        if ordonable:
            self.pgsql.addColumn("CAST(TRIM(SPLIT_PART(numerocertificat,'-','4')) as integer)","ordre", alias="ordre")
        else:
            self.pgsql.addColumn("TRIM(SPLIT_PART(numerocertificat,'-','4'))", "ordre", alias="ordre")
        self.pgsql.join("parcelle_d", "parcelle_d.idcertificat=certificat.idcertificat", "LEFT")
        self.pgsql.join("proprietaireparcelle", "parcelle_d.gid=proprietaireparcelle.idparcelle", "LEFT")
        self.pgsql.join("personne", "proprietaireparcelle.idpersonne=personne.idpersonne", "LEFT")

        self.pgsql.fillComboWithSql(self.ui.comboBoxType, "SELECT DISTINCT typecertificat from certificat",
                                    "typecertificat", "typecertificat")
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.init_actions()
        

    def init_actions(self):
        manager = AccesManager.AccessManager(self, self.connection)
        manager.activate_widget("KARATANY/PRINT", self.ui.pushButtonPrint)

        self.ui.checkBoxNumeroCertificat.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxNomProprietaire.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxDateCreation.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxType.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxFokontany.stateChanged.connect(self.setupFieldsStatus)
        self.ui.pushButtonFermer.clicked.connect(self.close)
        self.ui.pushButtonAfficherTous.clicked.connect(lambda: self.fillTable(True))
        self.ui.pushButtonRechercher.clicked.connect(lambda: self.fillTable(False))
        self.ui.lineEditNumeroCertificat.textEdited.connect(lambda: self.fillTable(False))
        self.ui.lineEditNomProprietaire.textEdited.connect(lambda: self.fillTable(False))
        self.ui.dateEditCreation.dateChanged.connect(lambda: self.fillTable(False))
        self.ui.comboBoxType.currentIndexChanged.connect(lambda: self.fillTable(False))

        self.ui.pushButtonDetails.clicked.connect(self.details)
        self.ui.pushButtonPrint.clicked.connect(self.doprint)
        self.ui.tableWidget.cellClicked.connect(self.cellSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.details)

    def setupFieldsStatus(self):
        self.ui.lineEditNumeroCertificat.setEnabled(self.ui.checkBoxNumeroCertificat.isChecked())
        self.ui.lineEditNomProprietaire.setEnabled(self.ui.checkBoxNomProprietaire.isChecked())
        self.ui.dateEditCreation.setEnabled(self.ui.checkBoxDateCreation.isChecked())
        self.ui.comboBoxType.setEnabled(self.ui.checkBoxType.isChecked())
        self.ui.comboBoxFokontany.setEnabled(self.ui.checkBoxFokontany.isChecked())

    def fillTable(self, search_all):
        conditions = []
        if self.isprint == 0:
            conditions.append(PgSql.Condition("certificat.isprint", 0))
        else:
            conditions.append(PgSql.Condition("certificat.isprint", 1))
        if search_all:
            self.pgsql.fillTable(self.ui.tableWidget, conditions,"ordre")
        else:

            if self.ui.checkBoxNumeroCertificat.isChecked():
                conditions.append(
                    PgSql.Condition("certificat.numerocertificat", self.ui.lineEditNumeroCertificat.text(), True)
                )
            if self.ui.checkBoxDateCreation.isChecked():
                conditions.append(PgSql.Condition("datecreation", self.ui.dateEditCreation.text()))
            if self.ui.checkBoxNomProprietaire.isChecked():
                conditions.append(
                    PgSql.Condition("UPPER(personne.nompersonne)", str(self.ui.lineEditNomProprietaire.text()).upper(), True)
                )
            if self.ui.checkBoxType.isChecked():
                conditions.append(PgSql.Condition("typecertificat", self.ui.comboBoxType.currentText()))
            self.pgsql.fillTable(self.ui.tableWidget, conditions,"ordre")

    def cellSelected(self, row, column):
        cellid = self.ui.tableWidget.item(row, 4).text()
        if cellid == "None":
            return
        canvas = self.canvas
        clayer = self.parent.registry.mapLayersByName("Certificats")[0]
        self.canvas.setCurrentLayer(clayer)
        self.geomid = cellid
        for layer in canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
        canvas.refresh()
        clayer.select(int(cellid))
        canvas.zoomToSelected(clayer)

    def details(self):
        indexes = self.ui.tableWidget.selectedIndexes()
        if len(indexes) == 0:
            return
        idcertificat = self.ui.tableWidget.item(indexes[0].row(), 0).text()
        dialog = CertificatFoncierRun(self.connection, str(idcertificat))
        dialog.exec_()

    def updateCFWhenPrint(self):
        self.isprint = 1
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE certificat SET isprint=(%s)   WHERE idcertificat = (%s)",
                           (int(self.isprint), int(self.idCF)))
            self.connection.commit()
        except Exception as e:
            print(e.message)
            self.connection.rollback()
        cursor.close()

    def doprint(self):

        indexes = self.ui.tableWidget.selectedIndexes()
        if len(indexes) == 0:
            return
        for i in indexes:
            if i.column() != 0:
                continue
            idcertificat = self.ui.tableWidget.item(i.row(), 0).text()
            self.idCF = idcertificat
            wkt = self.getGeomWkt(self.idCF)
            geom = QgsGeometry.fromWkt(wkt)

            #if self.checkEmpietement(geom):
                #QMessageBox.critical(None, u"Empiètement", u"Impréssion impossible: empiètement sur couche plof detectée!")
                #return

            QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
            try:
                from .PrintCertificatFoncier import PrintCertificatFoncier
                qrCodeGenerator = QrCodeGenerator()
                p = PrintCertificatFoncier(self.connection, str(idcertificat))
                p.setCodeImageGenerator(qrCodeGenerator)
                p.doprint()
                QApplication.restoreOverrideCursor()
                self.updateCFWhenPrint()
            except Exception as e:
                print(e)

    def getGeomWkt(self, idCF):
        cur = self.connection.cursor()
        try:
            cur.execute ("SELECT ST_AsText(pd.geom) FROM parcelle_d pd WHERE pd.idcertificat = %s", (str(idCF),))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print (err)

    def loadShapeFromFile(self, filename, label, strokeColor, fillColor):
        if filename is None or filename == "":
            return None
        layer = QgsVectorLayer(filename, label, "ogr")
        crs = QgsCoordinateReferenceSystem(globalvars.EPSG_SCR, QgsCoordinateReferenceSystem.EpsgCrsId)
        layer.setCrs(crs)
        if not layer.isValid():
            return None
        QgsMapLayerRegistry.instance().addMapLayer(layer)

        return layer

    def loadCouchesTitres(self):
        layers = []
        couches = ProjetCouche.find_by_projet_commune(self.connection, globalvars.id_projet_commune)
        couchesTitres = filter(lambda couche: (couche.type_couche == 'S'), couches)
        for couche in couchesTitres:
            if couche.plofpaps != 1:
                if couche.plofpaps != 2:  # non limite administrative
                    layer = self.loadShapeFromFile(couche.fichier, couche.libelle, couche.couleur_bg,
                                                   couche.remplissage)
                #self.addLabelToLayer(layer, couche.label_name)
                layers.append(layer)
        return layers

    def checkEmpietement(self, geom):
        print "in check empietement"
        empietement_plof = False
        try:
            titres = self.loadCouchesTitres()
        except Exception as err:
            print (err)
        try :
            for lay in titres:
                print "LOADIND COUCHES TITRES"
                if(lay is not None):
                    for elem in lay.getFeatures():
                        geomTitre = elem.geometry()

                        if geom.intersects(geomTitre):
                            intersect = geomTitre.intersection(geom)
                            intersection_geometry = QgsGeometry(intersect)
                            print "Area of intersection **********************"
                            print intersection_geometry.area()
                            if intersection_geometry.area() >= float(0.001):
                                empietement_plof = True
                                break
                        if geomTitre.within(geom) or geom.within(geomTitre):
                            empietement_plof = True
                            break
        except Exception as err:
            print (err)

        return empietement_plof
