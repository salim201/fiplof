# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConsultationDemande.ui'
#
# Created: Mon Feb 05 19:15:27 2018
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

#from PyQt4 import QtCore, QtGui
import os, os.path, sys
import qgis, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *

from qgis.gui import *
import psycopg2
import globalvars
#sys.setdefaultencoding('utf-8')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Dialog(object):


    def __init__(self, parent,edition = 0):
        print "ffsdf"
        self.parent = parent
        self.stateEdition = edition
        self.tool  = self.parent.tool
        self.current_layer = self.parent.current_layer
        self.canvas = self.parent.MainWindow.canvas
        self.activateChangeOngeom = self.parent.ui.actionEnregistrer
        self.canvas = self.parent.canvas
        self.connection = self.parent.connection
        self.cur = self.parent.connection.cursor()
        self.idparcelle = 1
        self.idDemande = 0
        self.geomid = 0
        self.dlg = ""
        self.id_projet = self.parent.id_projet
        self.gids = []
        #self.tableWidget.setSelectionBehavior(1)
        #self.connection = parent.connection

    def initDB(self):

        #self.cur = self.parent.connection.cursor()
        # revenir au fichier de depart
        print "initDB"

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(435, 534)
        self.dlg = Dialog
        #self.initDB()
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.checkBoxNumeroDemande = QtGui.QCheckBox(Dialog)
        self.checkBoxNumeroDemande.setObjectName(_fromUtf8("checkBoxNumeroDemande"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.checkBoxNumeroDemande)
        self.lineEditNumeroDemande = QtGui.QLineEdit(Dialog)
        self.lineEditNumeroDemande.setEnabled(False)
        self.lineEditNumeroDemande.setObjectName(_fromUtf8("lineEditNumeroDemande"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditNumeroDemande)
        self.checkBoxNomDemandeur = QtGui.QCheckBox(Dialog)
        self.checkBoxNomDemandeur.setObjectName(_fromUtf8("checkBoxNomDemandeur"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.checkBoxNomDemandeur)
        self.lineEditNomDemandeur = QtGui.QLineEdit(Dialog)
        self.lineEditNomDemandeur.setEnabled(False)
        self.lineEditNomDemandeur.setObjectName(_fromUtf8("lineEditNomDemandeur"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditNomDemandeur)
        self.checkBoxDateDemande = QtGui.QCheckBox(Dialog)
        self.checkBoxDateDemande.setObjectName(_fromUtf8("checkBoxDateDemande"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.checkBoxDateDemande)
        self.dateEditDateDemande = QtGui.QDateEdit(Dialog)
        self.dateEditDateDemande.setEnabled(False)
        self.dateEditDateDemande.setCalendarPopup(True)
        self.dateEditDateDemande.setObjectName(_fromUtf8("dateEditDateDemande"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.dateEditDateDemande)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.checkBox)
        self.auDateEdit = QtGui.QDateEdit(Dialog)
        self.auDateEdit.setEnabled(False)
        self.auDateEdit.setObjectName(_fromUtf8("auDateEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.auDateEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonAfficherTous = QtGui.QPushButton(self.groupBox)
        self.pushButtonAfficherTous.setObjectName(_fromUtf8("pushButtonAfficherTous"))
        self.horizontalLayout.addWidget(self.pushButtonAfficherTous)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonRechercher = QtGui.QPushButton(self.groupBox)
        self.pushButtonRechercher.setObjectName(_fromUtf8("pushButtonRechercher"))
        self.horizontalLayout.addWidget(self.pushButtonRechercher)
        self.verticalLayout.addWidget(self.groupBox)
        self.tableWidget = QtGui.QTableWidget(Dialog)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.verticalLayout.addWidget(self.tableWidget)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonDetails = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonDetails.setObjectName(_fromUtf8("pushButtonDetails"))
        self.horizontalLayout_2.addWidget(self.pushButtonDetails)
        #self.pushButtonSelection = QtGui.QPushButton(self.groupBox_2)
        #self.pushButtonSelection.setObjectName(_fromUtf8("pushButtonSelection"))
        #self.horizontalLayout_2.addWidget(self.pushButtonSelection)
        self.pushButtonQuitter = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonQuitter.setObjectName(_fromUtf8("pushButtonQuitter"))
        self.horizontalLayout_2.addWidget(self.pushButtonQuitter)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.checkBoxNumeroDemande, self.lineEditNumeroDemande)
        Dialog.setTabOrder(self.lineEditNumeroDemande, self.checkBoxNomDemandeur)
        Dialog.setTabOrder(self.checkBoxNomDemandeur, self.lineEditNomDemandeur)
        Dialog.setTabOrder(self.lineEditNomDemandeur, self.checkBoxDateDemande)
        Dialog.setTabOrder(self.checkBoxDateDemande, self.dateEditDateDemande)
        Dialog.setTabOrder(self.dateEditDateDemande, self.pushButtonAfficherTous)
        Dialog.setTabOrder(self.pushButtonAfficherTous, self.pushButtonRechercher)
        Dialog.setTabOrder(self.pushButtonRechercher, self.pushButtonQuitter)
        Dialog.setTabOrder(self.pushButtonQuitter, self.tableWidget)
        self.checkBoxNumeroDemande.stateChanged.connect(self.setupFieldsStatus)
        self.checkBoxNomDemandeur.stateChanged.connect(self.setupFieldsStatus)
        self.checkBoxDateDemande.stateChanged.connect(self.setupFieldsStatus)
        self.checkBox.stateChanged.connect(self.setupFieldsStatus)
        #self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.pushButtonAfficherTous.clicked.connect(self.showAll)
        self.pushButtonDetails.clicked.connect(self.detailsDemande)
        self.tableWidget.cellClicked.connect(self.cellSelected)
        self.pushButtonRechercher.clicked.connect(self.readInput)
        self.pushButtonQuitter.clicked.connect(self.closeApp)
        self.tableWidget.setSelectionBehavior(1)

    def setupFieldsStatus(self):

        self.lineEditNumeroDemande.setEnabled(self.checkBoxNumeroDemande.isChecked())
        self.lineEditNomDemandeur.setEnabled(self.checkBoxNomDemandeur.isChecked())
        self.dateEditDateDemande.setEnabled(self.checkBoxDateDemande.isChecked())
        self.auDateEdit.setEnabled(self.checkBox.isChecked())

        if self.checkBoxNumeroDemande.isChecked() != True:
            self.lineEditNumeroDemande.clear()

        if self.checkBoxNomDemandeur.isChecked() != True:
            self.lineEditNomDemandeur.clear()

        if self.checkBoxDateDemande.isChecked() != True:
            self.dateEditDateDemande.clear()

        if self.checkBox.isChecked() != True:
            self.auDateEdit.clear()


    def closeApp(self):
        self.dlg.close()

    def detailsDemande(self):

        #from DetailsDemandeRunn import DetailsDemandeRunn
        from DemandeDetailsRun import  DemandeDetailsRun
        #detail = DetailsDemandeRunn(self)
        detail = DemandeDetailsRun(self)
        detail.show()
        result = detail.exec_()

    def showAll(self):
        print "dfsdf"
        #self.cur.execute("SELECT idcertificat, numerodemande, datereconnaissance FROM certificat")

        self.cur.execute("SELECT DISTINCT pd.numdemande,dmd.nom,d.datedemande,pd.surface,pd.gid FROM "
                         " parcelle_d pd, demande d "
                         " INNER  JOIN avoir_dmd avd ON d.iddemande = avd.iddemande "
                         " INNER  JOIN demandeur_d dmd   ON avd.iddemandeur = dmd.iddemandeur "
                         " WHERE pd.gid = d.gid AND pd.idcertificat IS NULL AND d.idrejet IS NULL AND d.idprojet = %s",[int(self.id_projet)])

        data = self.cur.fetchall()
        print "data in"
        #print data
        print "data out"
        self.add_valuest(data)

        # rint len(data[0])

    def add_values(self, data):
        columns = len(data)
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.insertRow(rowPosition)
        print len(data)
        print "at add_values"
        for i in range(len(data)):
            item = QtGui.QTableWidgetItem()
            print "at add_values range"
            print  str(data[i])

            item.setText(_translate("", str(data[i]), None))
            print "at add_values range out"
            self.tableWidget.setItem(rowPosition, i, item)

    def add_valuest(self, data):
        i = 0
        j = 0
        nb_row = len(data)
        lignes = len(data)
        columns = 5
        self.gids[:] = []
        self.tableWidget.setRowCount(nb_row)
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.setRowCount(0)

        while i < len(data):

            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.gids.append(data[i][0])

            print " self.gids.append(data[i][0]) in"
            print self.gids
            print " self.gids.append(data[i][0]) out"

            for j in range(columns):

                if( str(data[i][j]) != "" or  str(data[i][j]) != None ) :
                    if(j == 2) :
                        item = QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y'))
                        item.setText(_translate("", str(data[i][j]), None))
                        self.tableWidget.setItem(rowPosition, j, item)
                        #self.ui.tableWidget.setItem(rowPosition, j - 1,QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                    else :
                        item = QtGui.QTableWidgetItem(str(data[i][j]))
                        item.setText(_translate("", str(data[i][j]), None))
                        self.tableWidget.setItem(i, j, item)
                else :
                    print str(data[i][j])
            i = i + 1


    def readInput(self):
        data = {}

        data['idprojet'] = int(self.id_projet)

        if self.checkBoxNumeroDemande.isChecked():
            data['numdemande'] = unicode(self.lineEditNumeroDemande.text()).encode('utf-8')
        else :
            data['numdemande'] = ''

        if self.checkBoxNomDemandeur.isChecked():
            data['nomdemandeur'] = unicode(self.lineEditNomDemandeur.text()).encode('utf-8')
        else :
            data['nomdemandeur'] = ''

        if self.checkBoxDateDemande.isChecked():
            data['datedebut'] = datetime.date(self.dateEditDateDemande.date().year(), self.dateEditDateDemande.date().month(), self.dateEditDateDemande.date().day())
            print data['datedebut']
        else:
            data['datedebut'] = ''
        if self.checkBox.isChecked():
            #data['datefin'] = time.strptime(self.ui.dateEditDateDemandeFin.text(), '%d/%m/%Y')
            data['datefin'] = datetime.date(self.auDateEdit.date().year(), self.auDateEdit.date().month(), self.auDateEdit.date().day())
        else:
            data['datefin'] = ''

        #data['fokontany'] = unicode(self.ui.comboBoxFokotany.currentText()).encode('utf-8')

        print " data in "
        print data
        print " data out "
        self.rechercher(data)

    def rechercher(self, data):
        flag = 0
        listeParams =[]
        #SQL = "SELECT pd.gid, pd.numdemande, d.datedemande, d.datereconnaissance,   pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid "
        SQL = "SELECT pd.numdemande,dmd.nom,dmd.prenom, d.datedemande,pd.surface,pd.gid FROM " \
              " parcelle_d pd, demande d " \
              " INNER  JOIN avoir_dmd avd ON d.iddemande = avd.iddemande " \
              " INNER  JOIN demandeur_d dmd   ON avd.iddemandeur = dmd.iddemandeur " \
              " WHERE pd.gid = d.gid AND pd.idcertificat IS NULL AND d.idrejet IS NULL "

        SQL = SQL + "  AND d.idprojet = %s"
        data['idprojet'] = int(self.id_projet)
        listeParams.append(data['idprojet'])
        if self.checkBoxNumeroDemande.isChecked():
            data['numdemande'] = "%"+data['numdemande']+"%"
            SQL = SQL + " AND pd.numdemande LIKE %s "
            listeParams.append(data['numdemande'])
            flag = 1
        if self.checkBoxNomDemandeur.isChecked():
            if flag == 1:
                data['nomdemandeur'] = "%"+data['nomdemandeur']+"%"
                SQL = SQL + " AND dmd.nom = %s"
                listeParams.append(data['nomdemandeur'])
            else:
                data['nomdemandeur'] = "%" + data['nomdemandeur'] + "%"
                SQL = SQL + " AND dmd.nom = %s"
                listeParams.append(data['nomdemandeur'])
                flag = 1
        if self.checkBoxDateDemande.isChecked() and self.checkBox.isChecked():
            if flag == 1:
                SQL = SQL + " and d.datedemande >= %s and d.datedemande <= %s "
                listeParams.append(data['datedebut'])
                listeParams.append(data['datefin'])
            else:
                SQL = SQL + " AND d.datedemande >= %s and d.datedemande <= %s "
                listeParams.append(data['datedebut'])
                listeParams.append(data['datefin'])
                flag = 1
        elif self.checkBoxDateDemande.isChecked():
            if flag == 1:
                SQL = SQL + " and d.datedemande  >= %s "
                listeParams.append(data['datedebut'])
            else:
                SQL = SQL + " AND d.datedemande >= %s "
                listeParams.append(data['datedebut'])
                flag = 1
        elif self.checkBox.isChecked():
            if flag == 1:
                SQL = SQL + " and d.datedemande <= %s "
                listeParams.append(data['datefin'])
            else:
                SQL = SQL + " AND d.datedemande <= %s "
                listeParams.append(data['datefin'])
                flag = 1

        if flag == 1:
            #SQL = SQL + "and pd.idcertificat IS NULL"
            params = tuple(listeParams)
            try:
                self.cur.execute(SQL, params)
                results = self.cur.fetchall()
                #print results
                self.add_valuest(results)
            except StandardError as e:
                print e
        else:
            print "Aucun critere de recherche selectionne"
            QMessageBox.information(self.canvas, "Erreur", "Aucun critere de recherche selectionne ")
            self.tableWidget.setRowCount(0)

    def cellSelected(self , row):

        #print row
        print "row in"
        print row
        print "row out"

        ID = self.gids[row]
        print "ID IN"
        print ID
        print "ID out"

        ID =self.tableWidget.item(row, 4).text()
        #print "ID IN"
        #print ID
        #print "ID out"


        print row

        canvas = self.parent.canvas
        #cLayer = canvas.currentLayer()
        cLayer = self.parent.cLayer
        self.geomid = ID
        print " cLayer = canvas.currentLayer() in "
        print cLayer
        print " cLayer = canvas.currentLayer() out  "

        #mc = self.mapCanvas()
        for layer in canvas.layers():
            print " in layer loop in "
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()

        canvas.refresh()
        self.idparcelle = int(ID)
        cLayer.select(int(ID))
        print " ID in "
        print ID
        print " ID out "
        self.idDemande = int(ID)
        #cLayer.setSelectedFeatures(int(ID))
        canvas.zoomToSelected(cLayer)


        #box = cLayer.boundingBoxOfSelected()
        #canvas.setExtent(box);
        #canvas.refresh();




    def showInTable(self,data):
        self.gids[:] = []
        self.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.gids.append(data[i][0])
            j = 1
            while j < len(data[i]) - 1:
                if (j == 2 ) and data[i][j]:
                    self.tableWidget.setItem(rowPosition, j - 1,
                                             QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                else:
                    self.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(str(data[i][j])))
                j = j + 1

            i = i + 1

    def retranslateUi(self, Dialog):
        self.dlg = Dialog
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Consultation demande", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxNumeroDemande.setText(QtGui.QApplication.translate("Dialog", "Numero Demande", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxNomDemandeur.setText(QtGui.QApplication.translate("Dialog", "Nom Demandeur", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDateDemande.setText(QtGui.QApplication.translate("Dialog", "Date Demande", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Dialog", "Au", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAfficherTous.setText(QtGui.QApplication.translate("Dialog", "Afficher Tous ...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRechercher.setText(QtGui.QApplication.translate("Dialog", "Rechercher", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Dialog", "Numero demande", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Dialog", "Nom demandeurs", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("Dialog", "Date demande", None, QtGui.QApplication.UnicodeUTF8))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("Dialog", "Surface", None, QtGui.QApplication.UnicodeUTF8))

        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(QtGui.QApplication.translate("Dialog", "GID", None, QtGui.QApplication.UnicodeUTF8))

        self.pushButtonDetails.setText(QtGui.QApplication.translate("Dialog", "Details ...", None, QtGui.QApplication.UnicodeUTF8))
#        self.pushButtonSelection.setText(QtGui.QApplication.translate("Dialog", "Selectionner", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonQuitter.setText(QtGui.QApplication.translate("Dialog", "Quitter", None, QtGui.QApplication.UnicodeUTF8))

