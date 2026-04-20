#coding : utf8
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from qgis.core import *
from qgis.gui import *
from .code import Ui_Dialog


class codeRun(QtGui.QDialog):
    def __init__(self, connection, table, code , idsup, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.table = table
        self.code = code
        self.idsup = idsup
        self.parent = parent
        self.initDB()
        self.name = self.getValueConcerned()
        text = u"Le code que vous venez de saisir existe pour " + self.name
        self.ui.label.setText(text)
        self.codeInscrit = False
        self.newCode = None
        self.initActions()


    def initDB(self):
        self.cur = self.connection.cursor()

    def initActions(self):
        self.ui.btnValider.clicked.connect(self.retValue)

    def retValue(self):
        if str(self.ui.nouveuCodeLineEdit.text()).strip() != "":
            self.newCode = str(self.ui.nouveuCodeLineEdit.text()).strip()
            self.parent.newCode = self.newCode
            self.close()
        else:
            QtGui.QMessageBox.critical(self,  "Erreur", "Veuillez remplir le champ code")


    def getValueConcerned(self):
        sql = "SELECT nom" + self.table + " FROM " + self.table + " WHERE code" + self.table + "= %s"
        #param =[]
        if self.table == "fokontany":
            sql = sql + " and idcommune = %s"
        if self.table == "hameau":
            sql = sql + " and idfokontany"
        param = (self.code, self.idsup)

        try:
            self.cur.execute(sql, param)
            data = self.cur.fetchone()
            return data[0]
        except StandardError as e:
            print(e)
            self.connection.rollback()
            return None

    def __del__(self):
        self.cur.close()