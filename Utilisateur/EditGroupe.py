# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EditGroupe.ui'
#
# Created: Sat Jan 05 22:26:30 2019
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(784, 477)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/users/icone/group.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditNom = QtGui.QLineEdit(self.tab)
        self.lineEditNom.setObjectName(_fromUtf8("lineEditNom"))
        self.gridLayout.addWidget(self.lineEditNom, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.plainTextEditDescription = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEditDescription.setObjectName(_fromUtf8("plainTextEditDescription"))
        self.gridLayout.addWidget(self.plainTextEditDescription, 2, 0, 1, 2)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.treeWidget_2 = QtGui.QTreeWidget(self.tab_3)
        self.treeWidget_2.setObjectName(_fromUtf8("treeWidget_2"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_2)
        self.horizontalLayout_3.addWidget(self.treeWidget_2)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeWidget = QtGui.QTreeWidget(self.tab_2)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.horizontalLayout_2.addWidget(self.treeWidget)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonEnregistrer = QtGui.QPushButton(Dialog)
        self.pushButtonEnregistrer.setDefault(True)
        self.pushButtonEnregistrer.setObjectName(_fromUtf8("pushButtonEnregistrer"))
        self.horizontalLayout.addWidget(self.pushButtonEnregistrer)
        self.pushButtonAnnuler = QtGui.QPushButton(Dialog)
        self.pushButtonAnnuler.setAutoDefault(False)
        self.pushButtonAnnuler.setObjectName(_fromUtf8("pushButtonAnnuler"))
        self.horizontalLayout.addWidget(self.pushButtonAnnuler)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Edition Groupe", None))
        self.label.setText(_translate("Dialog", "Nom du Groupe", None))
        self.label_2.setText(_translate("Dialog", "Description", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Groupe", None))
        self.treeWidget_2.headerItem().setText(0, _translate("Dialog", "Item", None))
        self.treeWidget_2.headerItem().setText(1, _translate("Dialog", "Accès", None))
        __sortingEnabled = self.treeWidget_2.isSortingEnabled()
        self.treeWidget_2.setSortingEnabled(False)
        self.treeWidget_2.topLevelItem(0).setText(0, _translate("Dialog", "Plof", None))
        self.treeWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Privilèges", None))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "Menu", None))
        self.treeWidget.headerItem().setText(1, _translate("Dialog", "Création", None))
        self.treeWidget.headerItem().setText(2, _translate("Dialog", "Lecture", None))
        self.treeWidget.headerItem().setText(3, _translate("Dialog", "Modification", None))
        self.treeWidget.headerItem().setText(4, _translate("Dialog", "Supression", None))
        self.treeWidget.headerItem().setText(5, _translate("Dialog", "Impression", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Dialog", "Plof", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Accès aux menus", None))
        self.pushButtonEnregistrer.setText(_translate("Dialog", "Enregistrer", None))
        self.pushButtonAnnuler.setText(_translate("Dialog", "Annuler", None))

import icons_rc
