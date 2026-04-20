#coding: utf8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import psycopg2
import psycopg2.extras
import globalvars
import os
from Utils import Utils
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import SIGNAL
from random import randint
import time
from datetime import datetime
from ImportInventaireThread import ImportInventaireThread

from ImportInventaire import Ui_Dialog
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class ImportInventaireRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()
        self.ui.progressBar.setValue(0)
        self.ui.toolButtonShape.hide()
        self.ui.lineEditShape.hide()
        self.ui.checkBoxFichierForme.hide()

        self.ui.checkBoxLocalite.setChecked(True)
        self.ui.checkBoxOccupant.setChecked(True)
        self.ui.checkBoxPersonne.setChecked(True)
        self.ui.checkBoxParcelle.setChecked(True)
        self.ui.checkBoxFichierForme.setChecked(True)
        self.ui.label_5.hide()
        self.connection = connection
        self.myThread = None
        # self.setWindowTitle("Import OPROD")
        self.substeps = []
        self.steps = []
        self.fileNames = {}
        self.refImport = self.setRefImport()
        self.initSteps()


    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)
        #self.ui.toolButtonShape.clicked.connect(self.browseFile)
        self.ui.toolButtonPrcourir_parcelle.clicked.connect(self.browseFile)
        self.ui.toolButtonParcourir_personne.clicked.connect(self.browseFile)
        self.ui.toolButtonParcourir_occupant.clicked.connect(self.browseFile)
        self.ui.toolButtonParcourir_localite.clicked.connect(self.browseFile)
        self.ui.pushButtonLancer.clicked.connect(self.launch)
        self.ui.checkBoxFichierForme.clicked.connect(self.checkState)
        self.ui.checkBoxLocalite.clicked.connect(self.checkState)
        self.ui.checkBoxOccupant.clicked.connect(self.checkState)
        self.ui.checkBoxParcelle.clicked.connect(self.checkState)
        self.ui.checkBoxPersonne.clicked.connect(self.checkState)

    def checkState(self):
        self.ui.lineEditShape.setEnabled(self.ui.checkBoxFichierForme.isChecked())
        self.ui.toolButtonShape.setEnabled(self.ui.checkBoxFichierForme.isChecked())
        self.ui.lineEditParcelles.setEnabled(self.ui.checkBoxParcelle.isChecked())
        self.ui.toolButtonPrcourir_parcelle.setEnabled(self.ui.checkBoxParcelle.isChecked())
        self.ui.lineEditPersonnes.setEnabled(self.ui.checkBoxPersonne.isChecked())
        self.ui.toolButtonParcourir_personne.setEnabled(self.ui.checkBoxPersonne.isChecked())
        self.ui.lineEditOccupants.setEnabled(self.ui.checkBoxOccupant.isChecked())
        self.ui.toolButtonParcourir_occupant.setEnabled(self.ui.checkBoxOccupant.isChecked())
        self.ui.toolButtonParcourir_localite.setEnabled(self.ui.checkBoxOccupant.isChecked())
        self.ui.lineEditLocalites.setEnabled(self.ui.checkBoxLocalite.isChecked())
        self.ui.toolButtonParcourir_localite.setEnabled(self.ui.checkBoxLocalite.isChecked())

        self.initSteps()

    def initSteps(self):
        self.ui.listWidgetSteps.clear()
        self.ui.listWidget.clear()
        del self.steps[:]
        if self.ui.checkBoxLocalite.isChecked():
            self.steps.append(u"Localités")
        if self.ui.checkBoxPersonne.isChecked():
            self.steps.append(u"Personne")
        if self.ui.checkBoxParcelle.isChecked():
            self.steps.append(u"Données parcellaire")
        if self.ui.checkBoxOccupant.isChecked():
            self.steps.append(u"liaison personnes et parcelles")

        del self.substeps[:]
        #for i in ["Zone Administratives", "Personnes Physiques", "Parcelles", "Demandes", "Demandeurs", "Personnes morales", "Anomalies"]:
        for i in self.steps:
            step = QtGui.QListWidgetItem(i)
            step.setIcon(QtGui.QIcon(":/std/icone/time.png"))
            self.ui.listWidgetSteps.addItem(step)
            self.substeps.append([])

    def refreshSubSteps(self):
        items = self.ui.listWidgetSteps.selectedItems()
        self.ui.listWidget.clear()
        if len(items) == 0:
            return
        index = self.ui.listWidgetSteps.indexFromItem(items[0])
        self.ui.listWidget.clear()
        for item in self.substeps[index.row()]:
            listitem = QtGui.QListWidgetItem(item['text'])
            listitem.setIcon(QtGui.QIcon(":/std/icone/bullet_%s.png" % (item['icon'])))
            self.ui.listWidget.addItem(listitem)

    def browseFile(self):
        self.senderName = self.sender().objectName()
        if str(self.senderName).strip() == "toolButtonShape":
            try:
                self.filename = QtGui.QFileDialog.getOpenFileName(self,"Choisir un fichier shapefile", "", u"Fichiers Shapefile (*.shp)")
            except Exception as err:
                print (err)
            self.ui.lineEditShape.setText(self.fileName)

        else:
            try:
                self.filename = QtGui.QFileDialog.getOpenFileName(self,"Choisir un fichier csv", "", u"Fichiers Excel (*.csv)")
            except Exception as err:
                print (err)
            if str(self.senderName).strip() == "toolButtonPrcourir_parcelle":
                self.ui.lineEditParcelles.setText(self.filename)
                self.fileNames['parcelle'] = self.filename
            if str(self.senderName).strip() == "toolButtonParcourir_personne":
                self.ui.lineEditPersonnes.setText(self.filename)
                self.fileNames['personne'] = self.filename
            if str(self.senderName).strip() == "toolButtonParcourir_occupant":
                self.ui.lineEditOccupants.setText(self.filename)
                self.fileNames['occupant'] = self.filename
            if str(self.senderName).strip() == "toolButtonParcourir_localite":
                self.ui.lineEditLocalites.setText(self.filename)
                self.fileNames['localite'] = self.filename

    def launch(self):
        self.ui.progressBar.setValue(0)
        self.initSteps()
        if self.filename == "":
            return
        self.ui.pushButtonLancer.setEnabled(False)
        self.ui.pushButtonFermer.setEnabled(False)
        self.ui.toolButtonPrcourir_parcelle.setEnabled(False)
        self.ui.toolButtonParcourir_personne.setEnabled(False)
        self.ui.toolButtonParcourir_occupant.setEnabled(False)
        self.ui.toolButtonParcourir_localite.setEnabled(False)

        self.myThread = ImportInventaireThread(filenames=self.fileNames, connection=self.connection, refimport = self.refImport, steps = self.steps)
        self.connect(self.myThread, SIGNAL("finished()"), self.termine)
        self.connect(self.myThread, SIGNAL("alert(QString)"), self.alert)
        self.connect(self.myThread, SIGNAL("clearSubstep(int)"), self.clearSubstep)
        self.connect(self.myThread, SIGNAL("addSubStep(int, QString, QString)"), self.addSubStep)
        self.connect(self.myThread, SIGNAL("progress(int)"), self.progress)
        self.connect(self.myThread, SIGNAL("stepInit(int)"), self.stepInit)
        self.connect(self.myThread, SIGNAL("stepDone(int)"), self.stepDone)
        self.myThread.start()

    def termine(self):
        Utils.alert("Importation Terminee")
        self.ui.pushButtonLancer.setEnabled(True)
        self.ui.pushButtonFermer.setEnabled(True)
        self.ui.toolButtonPrcourir_parcelle.setEnabled(True)
        self.ui.toolButtonParcourir_personne.setEnabled(True)
        self.ui.toolButtonParcourir_occupant.setEnabled(True)
        self.ui.toolButtonParcourir_localite.setEnabled(True)

    def alert(self, msg):
        Utils.alert(msg)

    def clearSubstep(self, step):
        del self.substeps[step][:]

    def progress(self, p):
        self.ui.progressBar.setValue(p)

    def addSubStep(self, index, text, icon):
        self.substeps[index].append({'text': text, 'icon': icon})

    def stepInit(self, step):
        self.ui.listWidgetSteps.item(step).setIcon(QtGui.QIcon(':/std/icone/time_go.png'))

    def stepDone(self, step):
        m = 0
        for item in self.substeps[step]:
            if item["icon"] == 'red':
                v = 2
            if item["icon"] == "orange":
                v = 1
            if item["icon"] == "green":
                v = 0
            m = v if m < v else m
        if m == 0:
            icon = ":/std/icone/accept.png"
        if m == 1:
            icon = ":/std/icone/warning.png"
        if m == 2:
            icon = ":/std/icone/error.png"
        self.ui.listWidgetSteps.item(step).setIcon(QtGui.QIcon(icon))

    def get_cptImport(self):
        cur = self.connection.cursor()
        try:
            cur.execute('SELECT cptimport FROM commune WHERE idcommune = %s',(globalvars.id_commune,))
            res = cur.fetchone()
            return res[0]
        except Exception as err:
            print (err)
            self.connection.rollback()
        cur.close()

    def setRefImport(self):
        datejour = datetime.now().date()
        heure = datetime.now().time()
        refImport = 'IMP_INV_' + str(randint(10000, 99999)) + '-' + datejour.strftime("%Y-%m-%d") + "_" + heure.strftime("%H_%M")
        self.ui.lineEditRefImport.setText(refImport.strip())
        return refImport


