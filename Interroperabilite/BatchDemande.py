# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BatchDemande.ui'
#
# Created: Wed May 13 06:25:52 2026
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Gestion(object):
    def setupUi(self, Gestion):
        Gestion.setObjectName(_fromUtf8("Gestion"))
        Gestion.resize(1230, 779)
        self.pushButton_valider = QtGui.QPushButton(Gestion)
        self.pushButton_valider.setGeometry(QtCore.QRect(1100, 380, 111, 23))
        self.pushButton_valider.setObjectName(_fromUtf8("pushButton_valider"))
        self.label = QtGui.QLabel(Gestion)
        self.label.setGeometry(QtCore.QRect(410, 30, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.tableWidgetBath = QtGui.QTableWidget(Gestion)
        self.tableWidgetBath.setGeometry(QtCore.QRect(10, 100, 1081, 239))
        self.tableWidgetBath.setObjectName(_fromUtf8("tableWidgetBath"))
        self.tableWidgetBath.setColumnCount(7)
        self.tableWidgetBath.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetBath.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetBath.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetBath.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetBath.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetBath.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetBath.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetBath.setHorizontalHeaderItem(6, item)
        self.tableWidgetDemande = QtGui.QTableWidget(Gestion)
        self.tableWidgetDemande.setGeometry(QtCore.QRect(10, 380, 1081, 391))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft New Tai Lue"))
        self.tableWidgetDemande.setFont(font)
        self.tableWidgetDemande.setObjectName(_fromUtf8("tableWidgetDemande"))
        self.tableWidgetDemande.setColumnCount(10)
        self.tableWidgetDemande.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetDemande.setHorizontalHeaderItem(9, item)
        self.cocherTous = QtGui.QCheckBox(Gestion)
        self.cocherTous.setGeometry(QtCore.QRect(20, 350, 111, 17))
        self.cocherTous.setObjectName(_fromUtf8("cocherTous"))

        self.retranslateUi(Gestion)
        QtCore.QMetaObject.connectSlotsByName(Gestion)

    def retranslateUi(self, Gestion):
        Gestion.setWindowTitle(_translate("Gestion", "Gestion Batch ", None))
        self.pushButton_valider.setText(_translate("Gestion", "Valider", None))
        self.label.setText(_translate("Gestion", "Liste des blocs de demande reçus", None))
        item = self.tableWidgetBath.horizontalHeaderItem(0)
        item.setText(_translate("Gestion", "Id", None))
        item = self.tableWidgetBath.horizontalHeaderItem(1)
        item.setText(_translate("Gestion", "Source", None))
        item = self.tableWidgetBath.horizontalHeaderItem(2)
        item.setText(_translate("Gestion", "Statut", None))
        item = self.tableWidgetBath.horizontalHeaderItem(3)
        item.setText(_translate("Gestion", "Date Insertion", None))
        item = self.tableWidgetBath.horizontalHeaderItem(4)
        item.setText(_translate("Gestion", "Nb demande Ok", None))
        item = self.tableWidgetBath.horizontalHeaderItem(5)
        item.setText(_translate("Gestion", "Nb demande Erreur", None))
        item = self.tableWidgetBath.horizontalHeaderItem(6)
        item.setText(_translate("Gestion", "Traitement", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(1)
        item.setText(_translate("Gestion", "Code Parcelle", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(2)
        item.setText(_translate("Gestion", "Contenance", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(3)
        item.setText(_translate("Gestion", "Date demande", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(4)
        item.setText(_translate("Gestion", "Num décision", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(5)
        item.setText(_translate("Gestion", "Date Décision", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(6)
        item.setText(_translate("Gestion", "Début Affichage", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(7)
        item.setText(_translate("Gestion", "Fin Affichage", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(8)
        item.setText(_translate("Gestion", "Date RL", None))
        item = self.tableWidgetDemande.horizontalHeaderItem(9)
        item.setText(_translate("Gestion", "Occupation (année)", None))
        self.cocherTous.setText(_translate("Gestion", "Cocher tous", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Gestion = QtGui.QWidget()
    ui = Ui_Gestion()
    ui.setupUi(Gestion)
    Gestion.show()
    sys.exit(app.exec_())

