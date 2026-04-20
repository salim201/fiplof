# coding=utf-8
from PyQt4 import QtGui, Qt, QtCore
from Utilisateur.Groupes import Ui_Dialog
from PgCrud import PgSql, PgColumn
from models.Groupe import Groupe

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class GroupesRun(QtGui.QDialog):
    def __init__(self, parent, connection):
        QtGui.QDialog.__init__(self)
        self.parent, self.connection = parent, connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.init_actions()
        self.pgsql = PgSql.Table(self.connection, "groupe")
        self.pgsql.addColumn("id", "Id", True, PgColumn.ColumnType.INTEGER)
        self.pgsql.addColumn("nom", "Nom Groupe")
        self.refresh()

    def init_actions(self):
        self.ui.pushButtonFermer.clicked.connect(self.reject)
        self.ui.pushButtonNouveau.clicked.connect(self.nouveau)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)

    def nouveau(self):
        from Utilisateur import EditGroupeRun
        dialog = EditGroupeRun.EditGroupeRun(self.parent, self.connection)
        if dialog.exec_():
            self.refresh()

    def modifier(self):
        gid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if gid is None:
            return
        from Utilisateur import EditGroupeRun
        dialog = EditGroupeRun.EditGroupeRun(self.parent, self.connection, gid)
        if dialog.exec_():
            self.refresh()

    def supprimer(self):
        gid = self.pgsql.getSelectedId(self.ui.tableWidget)
        if gid is None:
            return
        if gid == "1":
            Qt.QMessageBox.critical(self, "Erreur", "Vous ne pouvez pas supprimer le groupe Admin")
            return
        model = Groupe(self.connection)
        g = model.find_by_id(gid)
        if g is None:
            return
        reply = Qt.QMessageBox.question(self, "Confirm",
                                        _fromUtf8(u"Voulez-vous supprimer le groupe %s ?\n"
                                                  u"Les utilisateurs dedans seront aussi supprimés !!" % (g.nom, )),
                                        Qt.QMessageBox.Yes | Qt.QMessageBox.No, Qt.QMessageBox.No)
        if reply == Qt.QMessageBox.No:
            return
        g.delete_by_id()
        self.refresh()

    def refresh(self):
        self.pgsql.fillTable(self.ui.tableWidget, [], "id")
        self.ui.tableWidget.horizontalHeader().resizeSection(0, 20)

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)
