from PyQt4 import QtGui, Qt
from .EditSurface import Ui_Dialog
#from .EditCommuneRun import EditCommuneRun
from PgCrud import PgSql, PgColumn
import globalvars

class EditContenanceRun(Qt.QDialog):
    def __init__(self, connection):
        Qt.QDialog.__init__(self)
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        validator = QtGui.QDoubleValidator()
        self.ui.lineEditSurface.setValidator(validator)
        self.ui.lineEditSurface.setText(str(globalvars.SurfaceMax))
        self.ui.update.clicked.connect(self.updateArea)
        self.ui.cancel.clicked.connect(self.cancel)


        #self.refresh()
        #self.initActions()

    def cancel(self):
        self.close()

    def updateArea(self):
        area = float(self.ui.lineEditSurface.text())
        if area > 0 :
            globalvars.SurfaceMax = float(self.ui.lineEditSurface.text())
        self.close()

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
