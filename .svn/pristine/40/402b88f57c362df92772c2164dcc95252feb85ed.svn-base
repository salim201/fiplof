# coding: utf8
from PyQt4 import QtGui, Qt
from .Projets import Ui_Dialog
from .EditProjetRun import EditProjetRun
from PgCrud import PgSql
from Utils import Utils

class ProjetsRun(QtGui.QDialog):
    def __init__(self, connection):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.refresh()
        self.initActions()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.pushButtonNouveau.clicked.connect(self.nouveau)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.pushButtonParametres.clicked.connect(self.parametres)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)

    def nouveau(self):
        d = EditProjetRun(self.connection)
        if d.exec_():
            self.refresh()

    def modifier(self):
        uid = Utils.getTableWidgetSelectedId(self.ui.tableWidget)
        if uid is None or uid == 0:
            return
        d = EditProjetRun(self.connection, uid)
        if d.exec_():
            self.refresh()

    def supprimer(self):
        uid = Utils.getTableWidgetSelectedId(self.ui.tableWidget, 0)
        if uid is None:
            return
        reply = Qt.QMessageBox.question(self, "Confirm", "Voulez-vous supprimer ce Projet ?",
                                     Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.No:
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM projet WHERE idprojet=%s", (uid,))
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        self.refresh()

    def refresh(self):
        sql = "SELECT idprojet, nom, date_lancement, date_premier_import, date_dernier_import FROM projet ORDER BY idprojet"
        pgsql = PgSql.Table(self.connection, "")
        pgsql.fillTableWithSql(self.ui.tableWidget, sql, [], "", ["Id", "Nom Projet", "Date De Lancement", "Date Premier Apport", "Date Dernier Apport"])

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)

    def parametres(self):
        from .ParamProjetsRun import ParamProjetsRun
        d = ParamProjetsRun(self.connection)
        d.exec_()