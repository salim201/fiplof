from PyQt4 import QtGui, Qt
from .Regions import Ui_Dialog
from .EditRegionRun import EditRegionRun
from PgCrud import PgSql, PgColumn


class RegionsRun(Qt.QDialog):
    def __init__(self, connection):
        Qt.QDialog.__init__(self)
        self.connection = connection
        self.pgsql = PgSql.Table(self.connection, "region")
        self.pgsql.addColumn("idregion", "Id", True, PgColumn.ColumnType.INTEGER)
        self.pgsql.addColumn("coderegion", "Code Region")
        self.pgsql.addColumn("nomregion", "Nom Region")
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()
        self.refresh()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.pushButtonNouveau.clicked.connect(self.nouveau)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)

    def refresh(self):
        self.pgsql.fillTable(self.ui.tableWidget, [], "idregion")

    def nouveau(self):
        print "nouveau region"
        dialog = EditRegionRun(self.connection)
        if dialog.exec_():
            self.refresh()

    def modifier(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        dialog = EditRegionRun(self.connection, uid)
        if dialog.exec_():
            self.refresh()

    def supprimer(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        reply = Qt.QMessageBox.question(self, "Confirm", "Voulez-vous supprimer la region ?",
                                     Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.No:
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM region WHERE idregion=%s", (uid,))
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        self.refresh()

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)