# coding: utf-8
import os, os.path, sys, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from .servitudePassage import Ui_Dialog
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ServitudePassageRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.setModal(True)
        self.connection = connection
        self.initActions()
        self.initDB()

    def initActions(self):
        #self.ui.toolBtnDate.clicked.connect(self.showCalWid) #date inscription
        #self.ui.toolButton_2.clicked.connect(self.showCalWid2)#date levee
        self.ui.btnAjouter.clicked.connect(self.fillTextParcelleGrevee)
        self.ui.btnAjouter_1.clicked.connect(self.fillTextBeneficiaire)
        self.ui.btnEnlever.clicked.connect(self.enleverParcelle)
        self.ui.btnEnlever_1.clicked.connect(self.enleverBeneficiaire)
        #self.btnOk.clicked.connect(self.readInput)

    def initDB(self):
        self.cur = self.connection.cursor()

    def fillTextParcelleGrevee(self):
        if self.ui.lineEditIdentifiant.text() != '':
            rowPosition = self.ui.tableWidgetParcelle.rowCount()
            self.ui.tableWidgetParcelle.insertRow(rowPosition)
            # idpersonnes.append(data[i][0])
            self.ui.tableWidgetParcelle.setItem(rowPosition, 0, QtGui.QTableWidgetItem(_fromUtf8(self.ui.lineEditIdentifiant.text())))

    def fillTextBeneficiaire(self):
        if self.ui.lineEdit_3.text() != '':
            rowPosition = self.ui.tableWidgetBeneficiaire.rowCount()
            self.ui.tableWidgetBeneficiaire.insertRow(rowPosition)
            # idpersonnes.append(data[i][0])
            self.ui.tableWidgetBeneficiaire.setItem(rowPosition, 0,
                                             QtGui.QTableWidgetItem(_fromUtf8(self.ui.lineEdit_3.text())))

    def readInput(self):
        data = {}
        data['origine'] = unicode(self.ui.comboBoxOrigine.currentText()).encode('utf-8')
        data['dateinscription'] = datetime.date(self.ui.dateEditInscription.date().year(), self.ui.dateEditInscription.date().month(), self.ui.dateEditInscription.date().day())
        data['datelevee'] = datetime.date(self.ui.dateEditLevee.date().year(), self.ui.dateEditLevee.date().month(), self.ui.dateEditLevee.date().day())
        data['description'] = unicode(self.ui.textEdit_3.toPlainText()).encode('utf-8')
        parcelleGrevee = []
        i = 0
        while i < self.ui.tableWidgetParcelle.rowCount():
            parcelleGrevee.append(unicode(self.ui.tableWidgetParcelle.item(i, 0).text()).encode('utf-8'))
            i = i+1

        beneficiaires = []
        i = 0
        while i < self.ui.tableWidgetBeneficiaire.rowCount():
            beneficiaires.append(unicode(self.ui.tableWidgetBeneficiaire.item(i, 0).text()).encode('utf-8'))
            i = i+1

        #data['description'] = _fromUtf8(self.textEditDesc.toPlainText())
        self.writeData(data, parcelleGrevee, beneficiaires)

    def writeData(self, data, parcelleGrevee, beneficiaires):
        temp = data['description']
        data['description'] = str(temp).replace("'", "\'")
        self.cur.execute("INSERT INTO servitude (origine, dateinscription, datelevee, descriptionservitude) VALUES (%s, %s, %s, %s)", (data['origine'],data['dateinscription'], data['datelevee'], data['description']))
        self.connection.commit()
        nbrParcelleGrevee = len(parcelleGrevee)
        nbrBeneficiaire = len(beneficiaires)

        i = 0
        while i < len(parcelleGrevee):
            self.cur.execute("INSERT INTO parcellegrevees (libelleparcellegrevees) VALUES (%s)",(parcelleGrevee[i],) )
            self.connection.commit()
            i = i + 1

        i = 0
        while i < len(beneficiaires):
            self.cur.execute("INSERT INTO beneficiaire (libellebeneficiaire) VALUES (%s)", (beneficiaires[i],))
            self.connection.commit()
            i = i + 1

        self.cur.execute("SELECT idservitude FROM servitude ORDER BY idservitude DESC LIMIT 1")
        idservitude = self.cur.fetchone()

        self.idServitude = idservitude[0]

        self.cur.execute("SELECT idparcellegrevees FROM parcellegrevees ORDER BY idparcellegrevees DESC LIMIT %s", (nbrParcelleGrevee, ))
        idsParcelleGrevees = self.cur.fetchall()

        self.cur.execute("SELECT idbeneficiaire FROM beneficiaire ORDER BY idbeneficiaire DESC LIMIT %s",(nbrBeneficiaire, ))
        idsBeneficiaire = self.cur.fetchall()

        i = 0
        while i < len(idsParcelleGrevees):
            self.cur.execute("INSERT INTO servitudeparcellegrevees (idparcellegrevees, idservitude) VALUES (%s, %s)", (idsParcelleGrevees[i][0], idservitude))
            self.connection.commit()
            i = i + 1

        i = 0
        while i < len(idsBeneficiaire):
            self.cur.execute("INSERT INTO servitudebeneficiaire (idbeneficiaire, idservitude) VALUES (%s, %s)", (idsBeneficiaire[i][0], idservitude))
            self.connection.commit()
            i = i + 1

    def enleverParcelle(self):
        if self.ui.tableWidgetParcelle.currentRow() == -1:
            QMessageBox.critical(self, u"Suppression d'une parcelle grevée",
                                     u"Veuillez au moins séléctionner une ligne dans le tableau")
        else:
            row = self.ui.tableWidgetParcelle.currentRow()
            self.ui.tableWidgetParcelle.removeRow(row)

    def enleverBeneficiaire(self):
        if self.ui.tableWidgetBeneficiaire.currentRow() == -1:
            QMessageBox.critical(self, u"Suppression d'un bénéficiaire",
                                     u"Veuillez au moins séléctionner une ligne dans le tableau")
        else:
            row = self.ui.tableWidgetBeneficiaire.currentRow()
            self.ui.tableWidgetBeneficiaire.removeRow(row)

    def getLastInsert(self):
        return self.idServitude
       # self.cur.execute("SELECT idcharge FROM autrecharge ORDER BY idcharge DESC LIMIT 1")
       # lastCharge = self.cur.fetchone()
      #  return lastCharge[0]

    def __del__(self):
        self.cur.close()


