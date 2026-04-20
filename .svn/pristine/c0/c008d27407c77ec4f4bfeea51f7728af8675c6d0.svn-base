#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2

from AreaConvert import AreaConvert
from .RecherchePropositionTitre import Ui_Dialog


class RecherchePropositionTitre(QDialog):
    def __init__(self, connection,canvas, parent, edition = None):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.idtitre = None
        self.idsTitre = []
        self.edition = edition
        self.parent = parent
        self.senderName = self.sender().objectName()
        self.registry = parent.registry
        #self.shape_prop_titre = parent.shape_prop_titre
        if edition == 2:
            self.tool = parent.tool
        self.activateChangeOngeom = None
        self.ui.tableWidget.setSelectionBehavior(1)
        #self.filenamepreview = ""
        #self.senderName = self.sender().objectName()
        self.initDB()
        self.initActions()
        #self.initPreview()

    def initActions(self):
        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.checkBoxNumDemande.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxNomDemandeur.stateChanged.connect(self.updateFieldsStatus)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnDetail.clicked.connect(self.ouvrirPropositionTitre)

    def showAll(self):
        data = []
        donnees = []
        surfacem2 = 0
        try:
            self.cur.execute("SELECT DISTINCT gid, numerotitre, nompropriete, ST_Area(geom) FROM titrefoncier")
            data = self.cur.fetchall()
        except StandardError as e:
            print(e)
        for dt in data:
            tempData = []
            tempData.append(dt[0])
            tempData.append(dt[1])
            tempData.append(dt[2])
            surfacem2 = round(dt[3], 2)
            print surfacem2
            tempData.append(surfacem2)
            donnees.append(tempData)

        self.showInTable(donnees)

    def showInTable(self, data):
        vtlayer = self.registry.mapLayersByName("Proposition de titre")[0]
        self.canvas.setCurrentLayer(vtlayer)
        self.idsTitre[:] = []
        #self.gids[:] = []
        print data
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.idsTitre.append(data[i][0])
            j = 1
            while j < len(data[i]):
                if j == 1 or j == 2:
                    self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(str(data[i][j])))
                elif j == 3:
                    print data[i][j]
                    self.ui.tableWidget.setItem(rowPosition, j , QtGui.QTableWidgetItem(float(data[i][j])))
                j = j + 1
            i = i + 1

    def readInput(self):
        data = {}
        data['numtitre'] = "%" + str(self.ui.lineEditNumTitre.text()) + "%"
        data['nompropriete'] = "%" + str(self.ui.lineEditNomPropriete.text()) + "%"
        self.rechercher(data)


    def rechercher(self, data):
        data2 = []
        donnees = []
        surfacem2 = 0
        listeParams = []
        listeParams[:] = []
        flag = 0
        SQL = "SELECT DISTINCT gid, numerotitre, nompropriete, ST_Area(geom) FROM titrefoncier "
        if self.ui.checkBoxNumDemande.isChecked():
            if flag == 0:
                flag = 1
                SQL = SQL + " WHERE numerotitre LIKE %s "
                listeParams.append(data['nom'])
            else:
                SQL = SQL + " AND numerotitre LIKE %s "
                listeParams.append(data['nom'])
        if self.ui.checkBoxNomDemandeur.isChecked():
            if flag == 0:
                SQL = SQL + " WHERE nompropriete LIKE %s "
                listeParams.append(data['nompropriete'])
                flag = 1
            else:
                SQL = SQL + " AND nompropriete LIKE %s "
                listeParams.append(data['nompropriete'])

        if flag == 1:
            try:
                params = tuple(listeParams)
                self.cur.execute(SQL,params)
                data2 = self.cur.fetchall()
                for dt in data2:
                    tempData = []
                    tempData.append(dt[0])
                    tempData.append(dt[1])
                    surfacem2 = round(dt[2], 2)
                    print surfacem2
                    tempData.append(surfacem2)
                    donnees.append(tempData)

                self.showInTable(donnees)
            except StandardError as e:
                print(e)

        else:
            print "Aucun critere de recherche"


    def updateFieldsStatus(self):
        self.ui.lineEditNumTitre.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.lineEditNomPropriete.setEnabled(self.ui.checkBoxNomDemandeur.isChecked())

    def selectionLigne(self, row):
        print row
        print self.idsTitre[row]
        ID = self.idsTitre[row]
        #self.numDemande = self.ui.tableWidget.item(row, 1).text()
        print ID
        self.idtitre = ID
        canvas = self.canvas

        vtlayer = self.registry.mapLayersByName("Proposition de titre")[0]
        self.canvas.setCurrentLayer(vtlayer)
        cLayer = self.canvas.currentLayer()
        print cLayer
        # cLayer.select(ID)
        # cLayer.setSelectedFeatures([ID])
        # self.cvs.zoomToSelected(cLayer)

        for layer in self.canvas.layers():
            print " in layer loop in "
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()

        self.canvas.refresh()
        cLayer.select(int(ID))
        self.canvas.zoomToSelected(cLayer)

    def ouvrirPropositionTitre(self):
        if self.edition == 2:
            self.activateChangeOngeom = self.parent.parent.ui.actionEnregistrer
            print "Edition de la GEOMETRIE"
        from .PropositionTitreRun import PropositionTitre
        if self.senderName == "actionConsultation":
            proposition = PropositionTitre(self.connection,self.canvas, self, 0)
            proposition.exec_()
        else:
            proposition = PropositionTitre(self.connection,self.canvas, self, self.edition)
            proposition.exec_()

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
