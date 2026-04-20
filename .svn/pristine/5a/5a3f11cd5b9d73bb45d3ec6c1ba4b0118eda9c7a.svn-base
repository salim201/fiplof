#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
import time, psycopg2, datetime, os, sys
from psycopg2.extensions import *
import globalvars
from Utils import Utils
from datetime import datetime

from .ImportImage import Ui_Dialog

from ImportImageThread import ImportImageThread

from PyQt4.QtCore import SIGNAL
from random import randint
import time
from datetime import datetime

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class ImportImageRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.progressBar.setValue(0)


        self.connection = connection
        self.myThread = None
        # self.setWindowTitle("Import OPROD")
        self.substeps = []
        self.steps = []
        self.fileNames = {}
        #self.refImport = self.setRefImport()
        self.id_commune = globalvars.id_commune
        self.idsFokontany = []
        self.idsHameau = []
        # self.fillComboCommune()
        # self.fillComboFokontany()
        self.initActions()
        #self.ui.toolButtonShape.setEnabled(False)
        self.initSteps()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)
        self.ui.toolButtonShape.clicked.connect(self.browseFile)
        self.ui.pushButtonLancer.clicked.connect(self.launch)


    def initSteps(self):
        self.ui.listWidgetSteps.clear()
        self.ui.listWidget.clear()
        del self.steps[:]
        self.steps.append(u"Identites des demandeurs")
        self.steps.append(u"Signature des voisins")

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
                self.filename =  QtGui.QFileDialog.getExistingDirectory(self, "Choisissez un dossier")
            except Exception as err:
                print (err)
            #self.ui.lineEditShape.setText(self.filename)
            if str(self.senderName).strip() == "toolButtonShape":
                self.ui.lineEditDirectory.setText(self.filename)
                self.fileNames['images'] = self.filename


    def launch(self):
        self.ui.progressBar.setValue(0)
        self.initSteps()
        if self.filename == "":
            return
        self.ui.pushButtonLancer.setEnabled(False)
        self.ui.pushButtonFermer.setEnabled(False)
        self.ui.toolButtonShape.setEnabled(False)



        self.myThread = ImportImageThread(filenames=self.fileNames, connection=self.connection, steps = self.steps)
        self.connect(self.myThread, SIGNAL("finished()"), self.termine)
        self.connect(self.myThread, SIGNAL("alert(QString)"), self.alert)
        self.connect(self.myThread, SIGNAL("alertToQuit(QString)"), self.alertToQuit)
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
        self.ui.toolButtonShape.setEnabled(True)


    def alert(self, msg):
        Utils.alert(msg)

    def alertToQuit(self, msg):
        Utils.alert(msg)
        self.close()

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

    # def get_cptImport(self):
    #     cur = self.connection.cursor()
    #     try:
    #         cur.execute('SELECT cptimport FROM commune WHERE idcommune = %s',(globalvars.id_commune,))
    #         res = cur.fetchone()
    #         return res[0]
    #     except Exception as err:
    #         print (err)
    #         self.connection.rollback()
    #     cur.close()
    #
    # def setRefImport(self):
    #     datejour = datetime.now().date()
    #     heure = datetime.now().time()
    #     refImport = 'IMP_Listing_' + str(randint(10000, 99999)) + '-' + datejour.strftime("%Y-%m-%d") + "_" + heure.strftime("%H_%M")
    #     self.ui.lineEditRefImport.setText(refImport.strip())
    #     return refImport
    #
    # def fillComboCommune(self):
    #     cur = self.connection.cursor()
    #
    #     try:
    #         cur.execute('SELECT c.idcommune, c.nomcommune, d.iddistrict, d.nomdistrict, r.idregion, r.nomregion FROM commune c inner join district d on c.iddistrict = d.iddistrict, '
    #                     'district dd inner join region r on dd.idregion = r.idregion where c.idcommune = %s ', (self.id_commune,))
    #         res = cur.fetchone()
    #
    #     except Exception as err:
    #         print err
    #         self.connection.rollback()
    #     cur.close()
    #
    # def fillComboFokontany(self):
    #
    #     self.idsFokontany[:] = []
    #     cur = self.connection.cursor()
    #     try:
    #         cur.execute(
    #             'SELECT f.idfokontany, f.nomfokontany from fokontany f inner join commune c on f.idcommune = c.idcommune where c.idcommune = %s',
    #             (self.id_commune,))
    #         res = cur.fetchall()
    #         if res is not None:
    #             for val in res:
    #                 self.ui.comboBoxFokontany.addItem(val[1], val[0])
    #                 self.idsFokontany.append(val[0])
    #     except Exception as err:
    #         print err
    #         self.connection.rollback()
    #     cur.close()
    #
    # def fillComboHameau(self, currIdx):
    #     self.idsHameau[:] = []
    #     self.ui.comboBoxHameau.clear()
    #     idfokontany = self.idsFokontany[currIdx]
    #     print ('idfokontany = ')
    #     print idfokontany
    #     cur = self.connection.cursor()
    #     try:
    #         cur.execute(
    #             "SELECT h.idhameau, CONCAT (f.codefokontany, h.codehameau, '  -  ' , h.nomhameau) from hameau h inner join fokontany f on h.idfokontany = f.idfokontany where f.idfokontany = %s",
    #             (idfokontany,))
    #         res = cur.fetchall()
    #         for val in res:
    #             self.ui.comboBoxHameau.addItem(val[1], val[0])
    #             self.idsHameau.append(val[0])
    #     except Exception as err:
    #         print err
    #         self.connection.rollback()
    #     cur.close()



