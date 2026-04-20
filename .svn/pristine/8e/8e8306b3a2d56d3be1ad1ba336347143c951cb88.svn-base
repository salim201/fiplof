# -*- coding: utf-8 -*-
import os
import sys
import os
import os.path
from os.path import expanduser
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from .ExportData import Ui_ExportData
from PyQt4.QtGui import *
import psycopg2
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
from PyQt4 import Qt, QtGui
import globalvars
import psycopg2
import time
import datetime, globalvars
from datetime import date
from ExportDataThread import ExportDataThread
from Utils import Utils
from Configuration import DbConfig
from plof import Plof
from ConfigParser import SafeConfigParser

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ExportDataRun(QtGui.QDialog):
    def __init__(self,parent,connection,isGuData = True, exetype='pg_dump'):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_ExportData()
        self.ui.setupUi(self)
        self.parent = parent
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.isGuData = isGuData
        self.ui.progressBar.setValue(0)
        if not self.isGuData:
            self.setWindowTitle("EXPORT DONNEES BIF")
        self.thread = None
        self.LOGIN = ''
        self.PASSWORD = ''
        self.FILESAVE = ''
        self.CURRENT_DB = ''
        self.CURRENT_USER = ''
        self.NOM_BASE = None
        self.output = []
        self.type = exetype
        self.initActions()

    def get_pgdump_path(self):
        setting = None
        print ("get pg dump path")
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT setting FROM pg_settings where name like 'data_directory'")
            row = cursor.fetchone()
            setting = row["setting"]
        except Exception as e:
            print(e)
        cursor.close()
        if setting is None:
            return None
        b = os.path.dirname(setting)
        print "mon pg dump path"
        return str(os.path.join(b, "bin\\%s.exe" % self.type))

    def initSteps(self):
        self.ui.listWidgetSteps.clear()
        self.ui.listWidget.clear()
        del self.substeps[:]
        for i in [_fromUtf8("Import Geometrie")]:
            step = QtGui.QListWidgetItem(i)
            step.setIcon(QtGui.QIcon(":/std/icone/time.png"))
            self.ui.listWidgetSteps.addItem(step)
            self.substeps.append([])

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)
        self.ui.toolButtonParcourir.clicked.connect(self.browseFile)
        self.ui.pushButtonExport.clicked.connect(self.launch)

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
        self.ui.progressBar.setValue(30)
        # id_projet = int(globalvars.id_projet)
        if self.filename == "":
            return
        self.ui.pushButtonExport.setEnabled(False)
        self.ui.pushButtonFermer.setEnabled(False)
        self.ui.toolButtonParcourir.setEnabled(False)
        print("launch on")
        pgdump = self.get_pgdump_path()
        print ("****pgdump******")
        print (pgdump)
        #self.message_added("Recuperation de l'executable %s" % self.type)

        try:
            self.myThread = ExportDataThread(pgdump=pgdump, filename=self.filename, connection=self.connection, isGuData=self.isGuData)
        except Exception as err:
            print(err)
        self.connect(self.myThread, SIGNAL("finished()"), self.termine)
        self.connect(self.myThread, SIGNAL("alert(QString)"), self.alert)
        self.connect(self.myThread, SIGNAL("clearSubstep(int)"), self.clearSubstep)
        self.connect(self.myThread, SIGNAL("addSubStep(int, QString, QString)"), self.addSubStep)
        self.connect(self.myThread, SIGNAL("progress(int)"), self.progress)
        self.connect(self.myThread, SIGNAL("stepInit(int)"), self.stepInit)
        self.connect(self.myThread, SIGNAL("stepDone(int)"), self.stepDone)
        try:
            self.ui.progressBar.setValue(60)
            self.myThread.start()
        except Exception as err:
            print(err)

    def clearSubstep(self, step):
        del self.substeps[step][:]

    def browseFile(self):
        self.filename = QtGui.QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour exporter les données")
        self.ui.lineEditPath.setText(self.filename)
        self.ui.pushButtonExport.setEnabled(True)

    def alert(self, msg):
        Utils.alert(msg)

    def progress(self, p):
        self.ui.progressBar.setValue(p)

    def termine(self):
        self.ui.progressBar.setValue(100)
        Utils.alert("Importation Terminee")
        self.ui.pushButtonExport.setEnabled(True)
        self.ui.pushButtonFermer.setEnabled(True)
        self.ui.toolButtonParcourir.setEnabled(True)

    def addSubStep(self, index, text, icon):
        if icon == 'red':
            icon = ":/std/icone/error.png"
        if icon == "orange":
            icon = ":/std/icone/warning.png"
        if icon == "green":
            icon = ":/std/icone/accept.png"
        step = QtGui.QListWidgetItem(text)
        step.setIcon(QtGui.QIcon(icon))
        #self.ui.listWidget.addItem(step)
        self.substeps[index].append({'text': text, 'icon': icon})

    def stepInit(self, step):
        self.ui.listWidgetSteps.item(step).setIcon(QtGui.QIcon(':/std/icone/time_go.png'))

    def addlistwidget(self, texte):
        step = QtGui.QListWidgetItem(texte)
        step.setIcon(QtGui.QIcon(":/std/icone/time.png"))
        #self.ui.listWidget.addItem(step)

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