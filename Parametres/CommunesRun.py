from PyQt4 import QtGui, Qt
from .Communes import Ui_Dialog
from .EditCommuneRun import EditCommuneRun
from PgCrud import PgSql, PgColumn

class CommunesRun(Qt.QDialog):
    def __init__(self, connection):
        Qt.QDialog.__init__(self)
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.pgsql = PgSql.Table(self.connection, "commune")
        self.pgsql.join("district", "district.iddistrict = commune.iddistrict")
        self.pgsql.addColumn("idcommune", "Id", True, PgColumn.ColumnType.INTEGER)
        self.pgsql.addColumn("nomdistrict", "District")
        self.pgsql.addColumn("codecommune", "Code Commune")
        self.pgsql.addColumn("nomcommune", "Nom Commune")
        self.pgsql.addColumn("codeg", "Code Guichet")
        self.pgsql.addColumn("maire", "Maire")
        self.refresh()
        self.initActions()

    def refresh(self):
        self.pgsql.fillTable(self.ui.tableWidget, [], "idcommune")

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.pushButtonNouveau.clicked.connect(self.nouveau)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)

    def nouveau(self):
        dialog = EditCommuneRun(self.connection)
        if dialog.exec_():
            self.refresh()

    def modifier(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        dialog = EditCommuneRun(self.connection, uid)
        if dialog.exec_():
            self.refresh()

    def supprimer(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        reply = Qt.QMessageBox.question(self, "Confirm", "Voulez-vous supprimer ce Commune ?",
                                     Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.No:
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM commune WHERE idcommune=%s", (uid,))
            self.connection.commit()
        except Exception as ex:
            print(ex)
            self.connection.rollback()
        cursor.close()
        self.refresh()

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)
