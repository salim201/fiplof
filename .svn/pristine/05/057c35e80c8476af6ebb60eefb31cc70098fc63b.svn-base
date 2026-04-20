import os, os.path, sys, datetime, time
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .ListeConsorts import Ui_Dialog


class ListeConsortsRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.initDB()
        self.setModal(True)
        print "Construction listeConsorts"
        from .VoirListeContribuableRun import VoirListeContribuableRun
        self.listeContribuable = VoirListeContribuableRun(self.connection)

        self.initActions()

        self.listeIdConsorts = []
        self.currData = []

        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        print "fin construction liste consorts ato"

    def initActions(self):
        self.ui.btnRecherche.clicked.connect(self.ouvrirListeContribuable)
        self.listeContribuable.ui.btnSelectionner.clicked.connect(self.getContribuableInfo)
        self.ui.btnAjouter.clicked.connect(self.ajouterLigne)

    def ouvrirListeContribuable(self):
        self.listeContribuable.isFromConsort(True)
        self.listeContribuable.exec_()

    def getContribuableInfo(self):
        idContribuable = self.listeContribuable.selectContribuable()
        print idContribuable
        self.getContribuableById(idContribuable)
        self.listeContribuable.close()

    def getContribuableById(self, id):
        self.cur.execute("SELECT * FROM contribuable WHERE idcontribuable = %s", (id,))
        data = self.cur.fetchone()
        print data
        self.fillFields(data)

    def fillFields(self, data):
        self.currData[:] = []
        self.currData.append(data[0])
        if data[1]:
            self.ui.lineEditNom.setText(data[1])
            self.currData.append(data[1])
        else:
            self.currData.append("")
        if data[9]:
            self.ui.lineEditPrenom.setText(data[9])
            self.currData.append(data[9])
        else:
            self.currData.append("")
        if data[2]:
            self.ui.dateEditDateNaissance.setDate(data[2])
            self.currData.append(data[2])
        else:
            self.currData.append("")
        if data[10]:
            self.ui.lineEditAdresse.setText(data[10])
            self.currData.append(data[10])
        else:
            self.currData.append("")
        if data[3]:
            self.ui.lineEditLieuDeNaissance.setText(data[3])
        if data[4]:
            self.ui.CIN.setCurrentIndex(0)
            self.ui.lineEditCIN1.setText(data[4][0:3])
            self.ui.lineEditCIN2.setText(data[4][3:6])
            self.ui.lineEditCIN3.setText(data[4][6:9])
            self.ui.lineEditCIN4.setText(data[4][9:len(data[4])])
            if data[11]:
                self.ui.dateEditCIN.setDate(data[11])
            if data[17]:
                self.ui.lineEditLieuCIN.setText(data[17])
        if data[12]:
            self.ui.CIN.setCurrentIndex(1)
            self.ui.lineEditNumActeNaissance.setText(data[12])
            if data[13]:
                self.ui.dateEditActeNaissance.setDate(data[13])
            if data[14]:
                self.ui.lineEditLieuActeNaissance.setText(data[14])
        if data[15]:
            if data[15] == "masculin":
                self.ui.radioHomme.setChecked(True)
            if data[15] == "feminin":
                self.ui.radioFemme.setChecked(True)

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def ajouterLigne(self):
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        # idpersonnes.append(data[i][0])
        self.listeIdConsorts.append(self.currData[0])
        print self.listeIdConsorts
        i = 1
        while i < len(self.currData):
            if i == 3:
                self.ui.tableWidget.setItem(rowPosition, i-1, QTableWidgetItem(self.currData[i].strftime('%d/%m/%Y')))
            else:
                self.ui.tableWidget.setItem(rowPosition, i - 1, QTableWidgetItem(self.currData[i]))
            i = i + 1

    def getAllConsortsOfContribuable(self, idcontribuable):
        print "get all consorts"
        print idcontribuable
        self.cur.execute("SELECT c.idcontribuable, c.nom, c.prenom, c.datenaissance, c.adresse FROM contribuableconsorts cc, contribuable c WHERE cc.idcontribuable = %s AND cc.idconsort = c.idcontribuable", (idcontribuable,))
        results = self.cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        #print "Eto izy no tapaka!!!!!"
        print results
        for result in results:
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)

            # idpersonnes.append(data[i][0])
            self.listeIdConsorts.append(result[0])
            print self.listeIdConsorts
            i = 1
            while i < len(result):
                if i == 3:
                    self.ui.tableWidget.setItem(rowPosition, i - 1,
                                                QTableWidgetItem(result[i].strftime('%d/%m/%Y')))
                else:
                    self.ui.tableWidget.setItem(rowPosition, i - 1, QTableWidgetItem(result[i]))
                i = i + 1


    def getIdsConsorts(self):
        return self.listeIdConsorts

