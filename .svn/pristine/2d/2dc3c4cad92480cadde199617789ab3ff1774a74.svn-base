#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2

from AreaConvert import AreaConvert
from .RechercheDomainesPublic import Ui_Dialog


class RecherchePropositionDomaine(QDialog):
    def __init__(self, connection,canvas, parent, edition = 0):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.tool = parent.tool
        self.iddomaine = None
        self.idsDomaine = []
        self.senderName = self.sender().objectName()
        self.edition = edition
        self.parent = parent
        self.registry = parent.registry
        if edition == 2:
            self.tool = parent.tool
        self.activateChangeOngeom = None
        self.ui.tableWidget.setSelectionBehavior(1)
        #self.filenamepreview = ""
        self.initDB()
        self.initActions()
        #self.initPreview()

    def initActions(self):
        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.checkBoxNumDemande.stateChanged.connect(self.updateFieldsStatus)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnDetail.clicked.connect(self.ouvrirPropositionDomaine)

    def showAll(self):
        data = []
        donnees = []
        surfacem2 = 0
        try:
            self.cur.execute("SELECT iddomainepublique, nom, ST_Area(geom) FROM domainepublique")
            data = self.cur.fetchall()
        except StandardError as e:
            print(e)
        for dt in data:
            tempData = []
            tempData.append(dt[0])
            tempData.append(dt[1])
            surfacem2 = round(dt[2], 2)
            print surfacem2
            tempData.append(surfacem2)
            donnees.append(tempData)

        self.showInTable(donnees)

    def showInTable(self, data):
        self.idsDomaine[:] = []
        #self.gids[:] = []
        print data
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.idsDomaine.append(data[i][0])
            j = 1
            while j < len(data[i]):
                if j == 1:
                    self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(str(data[i][j])))
                elif j == 2:
                    print data[i][j]
                    self.ui.tableWidget.setItem(rowPosition, j , QtGui.QTableWidgetItem(float(data[i][j])))
                j = j + 1
            i = i + 1

    def readInput(self):
        data = {}
        data['nom'] = "%" + str(self.ui.lineEditNom.text()) + "%"
        self.rechercher(data)


    def rechercher(self, data):
        data2 = []
        donnees = []
        surfacem2 = 0
        listeParams = []
        listeParams[:] = []
        flag = 0
        SQL = "SELECT iddomainepublique, nom, ST_Area(geom) FROM domainepublique "
        if self.ui.checkBoxNumDemande.isChecked():
            flag = 1
            SQL = SQL + " WHERE nom LIKE %s "
            listeParams.append(data['nom'])

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
        self.ui.lineEditNom.setEnabled(self.ui.checkBoxNumDemande.isChecked())

    def selectionLigne(self, row):
        print row
        print self.idsDomaine[row]
        ID = self.idsDomaine[row]
        #self.numDemande = self.ui.tableWidget.item(row, 1).text()
        print ID
        self.iddomaine = ID
        canvas = self.canvas
        vtlayer = self.registry.mapLayersByName("Proposition de domaine publique")[0]
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

    def ouvrirPropositionDomaine(self):
        if self.edition == 2:
            self.activateChangeOngeom = self.parent.parent.ui.actionEnregistrer
        from .PropositionDomaineRun import PropositionDoaminePublique
        if self.senderName == "actionConsultation_2":
            proposition = PropositionDoaminePublique(self.connection, self.canvas, self, 0)
            proposition.exec_()
        else:
            proposition = PropositionDoaminePublique(self.connection,self.canvas, self, self.edition)
            proposition.exec_()

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
        vtlayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
        self.canvas.setCurrentLayer(vtlayer)
