# coding : utf-8
import os, os.path, sys, time, datetime, globalvars
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtGui

from .ListeContribuables import Ui_Dialog


class ListeContribuableRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.initDB()
        self.initActions()
        self.ui.tableWidget.setSelectionMode(1)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.btnImprimerListe.hide()
        self.fillComboFkt()
        self.annee = int(datetime.datetime.now().strftime('%Y'))
        self.ui.lineEditAnnee.setText(datetime.datetime.now().strftime('%Y'))

    def fillComboFkt(self):
        try:
            self.cur.execute("SELECT fkt.idfokontany, fkt.nomfokontany FROM fokontany fkt INNER JOIN commune c ON fkt.idcommune = c.idcommune "
                         "WHERE c.idcommune = %s ", (globalvars.id_commune,))
            fkts = self.cur.fetchall()
            for fkt in fkts:
                self.ui.comboFokontany.addItem(fkt[1], fkt[0])

        except StandardError as e:
            print e
            self.connection.rollback()


    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def initActions(self):
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.btnFermer.clicked.connect(self.close)

    def readInput(self):
        data = {}
        data['fokontany'] = self.ui.comboFokontany.currentText()
        data['annee'] = self.ui.lineEditAnnee.text()
        data['tous'] = self.ui.checkBoxTousParFokontany.isChecked()
        data['groupee'] = self.ui.checkBoxGroupeeParFokontany.isChecked()
        self.chercherContribuable(data)

    def chercherContribuable(self, data):
        flag = 0
        listeParams = []
        #SQL = "SELECT idcontribuable, nom, datenaissance, lieu, cin, hetratany, hetratrano, hetratrano + hetratany FROM contribuable "
        SQL = "SELECT p.idpersonne, CONCAT(p.nompersonne,' ',p.prenompersonne), p.datenaissancepersonne, p.lieunaissancepersonne, p.numcipersonne, ic.hetratany::numeric, ic.hetratrano::numeric, " \
              "ic.hetratany::numeric + hetratrano::numeric " \
              "FROM personne p INNER JOIN impot_contribuable ic ON p.idpersonne = ic.idpersonne " \
              "WHERE ic.annee = %s"
        params = []
        params.append(self.annee)
        t_params = tuple(params)
        self.cur.execute(SQL, t_params)
        results = self.cur.fetchall()
        self.showInTable(results)

    def showInTable(self, data):
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            #self.idContribuable.append(data[i][0])
            j = 1
            while j < len(data[i]):
                if j == 2:
                    self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                else:
                    if data[i][j] is not None:
                        self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(str(data[i][j])))
                j = j + 1

            i = i + 1