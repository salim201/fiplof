# -*- coding: utf-8 -*-

import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtGui

from .VoirListeContribuable import Ui_Dialog


class VoirListeContribuableRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        print "construction voir liste contribuable"
        self.initDB()
        from .ContribuableRun import ContribuableRun
        self.contribuable = ContribuableRun(self.connection)
        print "fin construction liste contribuable"
        self.disableAll()

        self.initActions()
        self.idContribuable = []
        self.selectedId = None
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        #self.fromConsort = False
        #self.idcontribuable = []

    def initActions(self):
        self.ui.btnVoir.clicked.connect(self.voirContribuable)
        self.ui.btnModifier.clicked.connect(self.modifierContribuable)
        #self.ui.btnRechercher.clicked.connect(self.showAll)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.checkBoxNumActe.stateChanged.connect(self.updateFieldsState)
        self.ui.checkCIN.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxPrenom.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNom.stateChanged.connect(self.updateFieldsState)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.btnSelectionner.clicked.connect(self.selectContribuable)
        self.ui.btnAjouter.clicked.connect(self.ajoutContribuable)
        self.contribuable.ui.btnOk.clicked.connect(self.enregContribuable)
        #self.ui.tableWidget.cellClicked.connect(self.getIdSelected)

    def voirContribuable(self):
        self.contribuable.estConsultation(1)
        self.contribuable.ui.btnConsorts.show()
        self.contribuable.exec_()

    def modifierContribuable(self):
        self.contribuable.estConsultation(0)
        self.contribuable.ui.btnOk.clicked.connect(self.enregConsorts)
        self.contribuable.ui.btnConsorts.show()
        self.contribuable.exec_()

    def initDB(self):
        self.cur = self.connection.cursor()

    def showAll(self):
         #self.cur.execute("SELECT idcertificat, numerodemande, datereconnaissance FROM certificat")
        self.cur.execute("SELECT idcontribuable, nom, prenom, cin FROM contribuable ORDER BY nom ASC")
        data = self.cur.fetchall()
        self.showInTable(data)
        # rint len(data[0])


    def showInTable(self, data):
        self.idContribuable[:] = []
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.idContribuable.append(data[i][0])
            j = 1
            while j < len(data[i]):
                self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(data[i][j]).encode('utf-8')))
                j = j + 1

            i = i + 1

    def selectionLigne(self, row):
        self.selectedId = self.idContribuable[row]
        self.contribuable.getContribuableById(self.selectedId)

        #print numDemande
        #canvas = qgis.utils.iface.mapCanvas()
        #cLayer = canvas.currentLayer()
        #mc = qgis.utils.iface.mapCanvas()
        #for layer in mc.layers():
            #if layer.type() == layer.VectorLayer:
                #layer.removeSelection()

        #mc.refresh()
        #cLayer.select(int(ID))
        #        cLayer.select(496)

        #canvas.zoomToSelected(cLayer)

    def readInput(self):
        data = {}
        data['nom'] = str(self.ui.lineEditNom.text()).upper()
        data['prenoms'] = str(self.ui.lineEditPrenom.text()).upper()
        data['cin'] = str(self.ui.lineEditCIN1.text()) + str(self.ui.lineEditCIN2.text()) + str(self.ui.lineEditCIN3.text()) + str(self.ui.lineEditCIN4.text())
        data['numacte'] = str(self.ui.lineEditNumActe.text())
        self.rechercher(data)

    def rechercher(self, data):
        flag = 0
        listeParams = []
        SQL = "SELECT idcontribuable, nom, prenom, cin FROM contribuable "
        if self.ui.checkBoxNom.isChecked():
            if data['nom'] != '':
                data['nom'] = "%" + data['nom'] + "%"
                SQL = SQL + "WHERE UPPER(nom) LIKE %s "
                listeParams.append(data['nom'])
                flag = 1
        if self.ui.checkBoxPrenom.isChecked():
            if flag == 1:
                if data['prenoms'] != '':
                    data['prenoms'] = "%s" + data['prenoms'] + "%"
                    SQL = SQL + " AND UPPER(prenom) LIKE %s "
                    listeParams.append(data['prenoms'])
            else:
                if data['prenoms'] != '':
                    data['prenoms'] = "%s" + data['prenoms'] + "%"
                    SQL = SQL + " WHERE UPPER(prenom) LIKE %s "
                    listeParams.append(data['prenoms'])
                    flag = 1
        if self.ui.checkCIN.isChecked():
            if flag == 1:
                if data['cin'] != '':
                    data['cin'] = "%s" + data['cin'] + "%"
                    SQL = SQL + " AND cin LIKE %s "
                    listeParams.append(data['cin'])
            else:
                if data['cin'] != '':
                    data['cin'] = "%s" + data['cin'] + "%"
                    SQL = SQL + " WHERE cin LIKE %s "
                    listeParams.append(data['cin'])
                    flag = 1
        if self.ui.checkBoxNumActe.isChecked():
            if flag == 1:
                if data['numacte'] != '':
                    data['numacte'] = "%s" + data['numacte'] + "%"
                    SQL = SQL + " AND numactenaissance LIKE %s "
                    listeParams.append(data['numacte'])
            else:
                if data['numacte'] != '':
                    data['numacte'] = "%s" + data['numacte'] + "%"
                    SQL = SQL + " WHERE numactenaissance LIKE %s "
                    listeParams.append(data['numacte'])
                    flag = 1

        if flag == 1:
            params = tuple(listeParams)
            self.cur.execute(SQL, params)
            results = self.cur.fetchall()
            print results
            self.showInTable(results)

        else:
            self.cur.execute(SQL)
            results = self.cur.fetchall()
            self.showInTable(results)


    def updateFieldsState(self):
        self.ui.lineEditNom.setEnabled(self.ui.checkBoxNom.isChecked())
        if self.ui.checkBoxNom.isChecked() != True:
            self.ui.lineEditNom.clear()
        self.ui.lineEditPrenom.setEnabled(self.ui.checkBoxPrenom.isChecked())
        if self.ui.checkBoxPrenom.isChecked() != True:
            self.ui.lineEditPrenom.clear()
        self.ui.lineEditCIN1.setEnabled(self.ui.checkCIN.isChecked())
        self.ui.lineEditCIN2.setEnabled(self.ui.checkCIN.isChecked())
        self.ui.lineEditCIN3.setEnabled(self.ui.checkCIN.isChecked())
        self.ui.lineEditCIN4.setEnabled(self.ui.checkCIN.isChecked())
        if self.ui.checkCIN.isChecked():
            self.ui.lineEditCIN1.clear()
            self.ui.lineEditCIN2.clear()
            self.ui.lineEditCIN3.clear()
            self.ui.lineEditCIN4.clear()
        self.ui.lineEditNumActe.setEnabled(self.ui.checkBoxNumActe.isChecked())
        if self.ui.checkBoxNumActe.isChecked():
            self.ui.lineEditNumActe.clear()

    def disableAll(self):
        self.ui.lineEditNom.setDisabled(True)
        self.ui.lineEditPrenom.setDisabled(True)
        self.ui.lineEditNumActe.setDisabled(True)
        self.ui.lineEditCIN1.setDisabled(True)
        self.ui.lineEditCIN2.setDisabled(True)
        self.ui.lineEditCIN3.setDisabled(True)
        self.ui.lineEditCIN4.setDisabled(True)

    def selectContribuable(self):
        return self.selectedId

    def isFromConsort(self, value = False):
        if value:
            self.contribuable.ui.btnConsorts.hide()
            self.contribuable.ui.btnRecherche.hide()
            self.ui.btnAjouter.hide()
            self.ui.btnVoir.hide()
            self.ui.btnModifier.hide()
        else:
            self.contribuable.ui.btnConsorts.show()
            self.contribuable.ui.btnRecherche.show()

    def enregConsorts(self):
        self.contribuable.writeConsorts()
        self.contribuable.close()

    def ajoutContribuable(self):
        self.contribuable.estConsultation(2)
        self.contribuable.ui.btnConsorts.hide()
        #self.contribuable.ui.btnOk.clicked.connect(self.enregContribuable)
        self.contribuable.exec_()

    def enregContribuable(self):
        if self.contribuable.writeContribuable():
            self.contribuable.close()
            self.showAll()


    def __del__(self):
        self.cur.close()