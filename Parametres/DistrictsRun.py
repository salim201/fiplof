from PyQt4 import QtGui, Qt
from .District import Ui_Dialog
from .EditDistrictRun import EditDistrictRun
from PgCrud import PgSql, PgColumn

class DistrictsRun(Qt.QDialog):
    def __init__(self, connection):
        Qt.QDialog.__init__(self)
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.pgsql = PgSql.Table(self.connection, "district")
        self.pgsql.join("region", "district.idregion = region.idregion")
        self.pgsql.addColumn("iddistrict", "Id", True, PgColumn.ColumnType.INTEGER)
        self.pgsql.addColumn("nomregion", "Region")
        self.pgsql.addColumn("codedistrict", "Code District")
        self.pgsql.addColumn("nomdistrict", "Nom District")
        self.refresh()
        self.initActions()

    def refresh(self):
        self.pgsql.fillTable(self.ui.tableWidget, [], "iddistrict")

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.pushButtonNouveau.clicked.connect(self.nouveau)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)

    def nouveau(self):
        dialog = EditDistrictRun(self.connection)
        if dialog.exec_():
            self.refresh()

    def modifier(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        dialog = EditDistrictRun(self.connection, uid)
        if dialog.exec_():
            self.refresh()

    def supprimer(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        reply = Qt.QMessageBox.question(self, "Confirm", "Voulez-vous supprimer ce District ?",
                                     Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.No:
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM district WHERE iddistrict=%s", (uid,))
            self.connection.commit()
        except Exception as ex:
            print(ex)
            self.connection.rollback()
        cursor.close()
        self.refresh()

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)
