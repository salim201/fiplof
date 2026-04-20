# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
import psycopg2
import psycopg2.extras
from .nombre_dmd_cf import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class NombreDemandeEtCfRun(QDialog):
#    def __init__(self, connection,parent):
    def __init__(self, connection, parent):
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(u"Nombre de Demandes et Certificats")
        self.parent = parent
        self.connection = connection
        self.ui.lineEditNombreDemande.setReadOnly(True)
        self.ui.lineEditNombreCF.setReadOnly(True)
        self.getNombreDemande()
        self.getNombreCF()

    def getNombreDemande(self):
        cur = self.connection.cursor()
        nombre = 0
        try:
            cur.execute('SELECT COUNT(*) FROM demande WHERE numdemande IS NOT NULL')
            res = cur.fetchone()
            if res is not None:
                nombre = res[0]
        except Exception as err:
            print (err)
        self.ui.lineEditNombreDemande.setText(str(nombre))

    def getNombreCF(self):
        cur = self.connection.cursor()
        nombre = 0
        try:
            cur.execute('SELECT COUNT(*) FROM certificat WHERE numerocertificat IS NOT NULL')
            res = cur.fetchone()
            if res is not None:
                nombre = res[0]
        except Exception as err:
            print (err)
        self.ui.lineEditNombreCF.setText(str(nombre))
