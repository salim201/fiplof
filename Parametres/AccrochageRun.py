from PyQt4 import QtGui, Qt
from Accrochage import Ui_Accrochage
from PgCrud import PgSql, PgColumn


class AccrochageRun(Qt.QDialog):
    def __init__(self):
        Qt.QDialog.__init__(self)
        #self.connection = connection
        #self.pgsql = PgSql.Table(self.connection, "consistance")
        #self.pgsql.addColumn("idconsistance", "Id", True, PgColumn.ColumnType.INTEGER)
        #self.pgsql.addColumn("libelleconsistance", "Consistance")
        #self.pgsql.addColumn("parcelleoubatiment", "Momba Ny Tany")
        self.ui = Ui_Accrochage()
        self.ui.setupUi(self)
        #self.initActions()
        #self.refresh()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.pushButtonNouveau.clicked.connect(self.nouveau)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)

    def refresh(self):
        self.pgsql.fillTable(self.ui.tableWidget, [], "idconsistance")


    def supprimer(self):
        uid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if uid is None:
            return
        reply = Qt.QMessageBox.question(self, "Confirm", "Voulez-vous supprimer la consistance ?",
                                     Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.No:
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM consistance WHERE idconsistance=%s", (uid,))
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()
        self.refresh()

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)