import os, os.path, sys, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

from .AutresCharges import Ui_Dialog


class AutresChargesRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.initActions()
        self.initDB()
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.setModal(True)


    def readInput(self):
        data = {}
        print "read input"
        data['date'] = datetime.date(self.ui.dateEditRegistre.date().year(), self.ui.dateEditRegistre.date().month(), self.ui.dateEditRegistre.date().day())
        try:
            data['description'] = unicode(self.ui.textEditDesc.toPlainText()).encode('utf-8')
        except StandardError as e:
            print e
        print data
        self.writeData(data)

    def initDB(self):
        self.cur = self.connection.cursor()

    def writeData(self, data):
        temp = data['description']
        data['description'] = str(temp).replace("'", "\'")
        try:
            charge = self.cur.execute("INSERT INTO autrecharge (dateinscriptionregistre, descriptioncharge) VALUES (%s, %s)", (data['date'], data['description']))
            self.connection.commit()
        except StandardError as e:
            print e

    def getLastInsert(self):
        try:
            self.cur.execute("SELECT idcharge FROM autrecharge ORDER BY idcharge DESC LIMIT 1")
            lastCharge = self.cur.fetchone()
            return lastCharge[0]
        except StandardError as e:
            print e

    def __del__(self):
        self.cur.close()



