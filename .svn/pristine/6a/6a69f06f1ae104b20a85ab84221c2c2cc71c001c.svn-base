import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtGui, Qt
from PgCrud import PgSql, PgColumn
from GridHameau import Ui_CreationHameau
from EditHameauRunn import EditHameauRunn

class hameauRunn(Qt.QDialog):

    def __init__(self, connection,project_id = 0,FenHameauFromCF = None):
        Qt.QDialog.__init__(self)
        self.connection = connection
        self.FenHameauFromCF = FenHameauFromCF
        self.project_id = project_id
        self.pgsql = PgSql.Table(self.connection, "hameau")
        self.pgsql.addColumn("idhameau", "Id", True, PgColumn.ColumnType.INTEGER)
        self.pgsql.addColumn("codehameau", "Code Hameau")
        self.pgsql.addColumn("nomhameau", "Nom Hameau")
        self.ui = Ui_CreationHameau()
        self.ui.setupUi(self)
        self.setFixedWidth(700)
        self.initActions()
        self.refresh()


    def initActions(self):
        print " HAMEAU RUN"
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.pushButtonNouveau.clicked.connect(self.nouveau)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)

    def refresh(self):
        #self.pgsql.fillTable(self.ui.tableWidget, [], "idhameau")
        sql = "SELECT h.idhameau, h.codehameau, h.nomhameau,f.nomfokontany FROM hameau h INNER JOIN fokontany f ON h.idfokontany = f.idfokontany ORDER BY idhameau"
        self.pgsql.fillTableWithSql(self.ui.tableWidget, sql, "", "", ["id", "Code Hameau","Nom Hameau", "Fokontany"])

    def nouveau(self):
        uid  = 0
        dialog = EditHameauRunn(self.connection,uid,self.project_id,self.FenHameauFromCF)
        if dialog.exec_():
            self.refresh()

    def modifier(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        print "uid in "
        print uid
        print " uid out "
        if uid is None:
            return
        dialog = EditHameauRunn(self.connection, uid,self.project_id)
        if dialog.exec_():
            self.refresh()

    def supprimer(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        reply = Qt.QMessageBox.question(self, "Confirm", "Voulez-vous supprimer le Hameau ?",
                                     Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.No:
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM hameau WHERE idhameau=%s", (uid,))
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        self.refresh()

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)