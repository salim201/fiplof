#coding: utf8
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from qgis.core import *
from qgis.gui import *
from ImportDb import Ui_Dialog
from ImporterThreadIpss import ImporterThreadIpss
from Utils import Utils
import sys


class ImporterIpss(QtGui.QDialog):
    def __init__(self, connection):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initAction()
        self.ogroutput, self.connection, self.filename = "ogr.log", connection, ""
        self.myThread = None
        #self.setWindowTitle("Import OPROD")
        self.substeps = []
        self.initSteps()

    def initSteps(self):
        self.ui.listWidgetSteps.clear()
        self.ui.listWidget.clear()
        del self.substeps[:]
        #for i in ["Zone Administratives", "Personnes Physiques", "Parcelles", "Demandes", "Demandeurs", "Personnes morales", "Anomalies"]:
        for i in ["Hameau","Consistance"]:
            step = QtGui.QListWidgetItem(i)
            step.setIcon(QtGui.QIcon(":/std/icone/time.png"))
            self.ui.listWidgetSteps.addItem(step)
            self.substeps.append([])

    def initAction(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.accept)
        self.ui.pushButtonParcourir.clicked.connect(self.browseFile)
        self.ui.pushButtonLancer.clicked.connect(self.launch)
        self.ui.listWidgetSteps.itemSelectionChanged .connect(self.refreshSubSteps)

    def browseFile(self):
        self.filename = QtGui.QFileDialog.getExistingDirectory(self, "Choisissez un fichier")
        self.ui.labelFilename.setText(self.filename)

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

    def launch(self):
        self.ui.progressBar.setValue(0)
        self.initSteps()
        if self.filename == "":
            return
        self.ui.pushButtonLancer.setEnabled(False)
        self.ui.pushButtonAnnuler.setEnabled(False)
        self.ui.pushButtonParcourir.setEnabled(False)
        self.myThread = ImporterThreadIpss(filename=self.filename, connection=self.connection)
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
        self.ui.pushButtonAnnuler.setEnabled(True)
        self.ui.pushButtonParcourir.setEnabled(True)

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
