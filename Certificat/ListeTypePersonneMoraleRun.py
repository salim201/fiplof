# coding: utf-8
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from Utilisateur import AccesManager

from .listeTypePersonneMorale import Ui_Dialog
from Utils import Utils

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ListeTypePersonneMoraleRun(QDialog):
    listChanged = pyqtSignal()
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.ui.BTFermer.clicked.connect(self.close)
        self.connection = connection
        self.initDB()
        self.showInTable()
        self.initActions()

    def initActions(self):
        self.ui.pushButtonNouveau.clicked.connect(self.ajouter)
        self.ui.pushButtonModifier.clicked.connect(self.modifier)
        self.ui.pushButtonSupprimer.clicked.connect(self.supprimer)
        self.ui.tableWidget.itemSelectionChanged.connect(self.tableSelected)
        self.ui.tableWidget.cellDoubleClicked.connect(self.modifier)

    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart

    def showInTable(self):
        try:
            self.cur.execute("SELECT * FROM typepersonnemorale")
            data = self.cur.fetchall()
        except StandardError as e:
            self.connection.rollback()
            print(e)

        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            j = 1
            while j < len(data[i]) -1 :
                self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(_fromUtf8(data[i][j])))
                j = j + 1
            self.ui.tableWidget.item(rowPosition, 0).setData(Qt.UserRole, data[i][0])
            i = i + 1
        Utils.setTableWidgetColumnReadOnly(self.ui.tableWidget, 0)
        Utils.setTableWidgetColumnReadOnly(self.ui.tableWidget, 1)

    def ajouter(self):
        from .TypePersonneMoraleRun import TypePersonneMoraleRun
        w = TypePersonneMoraleRun(self.connection)
        if w.exec_():
            self.showInTable()
            self.listChanged.emit()

    def tableSelected(self):
        self.ui.pushButtonModifier.setEnabled(True)
        self.ui.pushButtonSupprimer.setEnabled(True)
        manager = AccesManager.AccessManager(self, self.connection)
        manager.activate_widget("PERSONNE_MORALE_TYPE/CREATE", self.ui.pushButtonNouveau)
        manager.activate_widget("PERSONNE_MORALE_TYPE/EDIT", self.ui.pushButtonModifier)
        manager.activate_widget("PERSONNE_MORALE_TYPE/DELETE", self.ui.pushButtonSupprimer)

    def modifier(self):
        r = self.ui.tableWidget.currentRow()
        if r < 0:
            return
        typeid = self.ui.tableWidget.item(r, 0).data(Qt.UserRole).toInt()[0]
        from .TypePersonneMoraleRun import TypePersonneMoraleRun
        w = TypePersonneMoraleRun(self.connection, typeid)
        if w.exec_():
            self.showInTable()
            self.listChanged.emit()

    def supprimer(self):
        r = self.ui.tableWidget.currentRow()
        if r < 0:
            return
        typeid = self.ui.tableWidget.item(r, 0).data(Qt.UserRole).toInt()[0]
        reply = QMessageBox.question(self, "Confirmation", "Voulez-vous supprimer ce type de personne ?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM typepersonnemorale WHERE idtype=%s", (typeid,))
            self.connection.commit()
        except Exception as ex:
            print(ex)
            self.connection.rollback()
        cursor.close()
        self.showInTable()
        self.listChanged.emit()


