#coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars, os, sys, psycopg2

from .Operation import Ui_Dialog


class OperationRun(QDialog):
    def __init__(self, connection, parent):
        QDialog.__init__(self)
        self.connection = connection
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(u"Opéartion cause")
        self.setModal(True)
        self.idCF = parent.idCF
        self.initDB()
        self.initActions()
        self.fillOperationCause()

    def initActions(self):
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnVoirActe.clicked.connect(self.ouvrirActe)

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def fillOperationCause(self):
        try:
            self.cur.execute("SELECT DISTINCT h.typeoperation, dmd.datedemande, dmd.cout FROM demande dmd, parcelle_d pd, certificat c, historique h WHERE pd.gid = dmd.gid AND h.idcertificat = c.idcertificat AND pd.idcertificat = c.idcertificat AND c.idcertificat = %s", (self.idCF,))
            data = self.cur.fetchone()
            print data
            self.useData(data)
        except StandardError as e:
            print e

    def useData(self, data):
        print data
        self.ui.lineEditTypeOperation.setText(unicode(data[0]))
        if data[1] is not None:
            self.ui.dateEdit.setDate(data[1])
        self.ui.lineEditCout1.setText(str(data[2]))

    def ouvrirActe(self):
        QMessageBox.information(self,u"Acte", u"Aucun acte n'est lié à cette opération")