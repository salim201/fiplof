# -*- coding: utf-8 -*-
import qgis, time, datetime
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from .ListePiecesAnnulation import Ui_Dialog

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


class ListePiecesAnnulation(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
        self.idDecision = 0
#       print self.parent.txt
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        #self.connection = self.parent.connection
        self.cur = self.parent.connection.cursor()
        #       print self.parent.txt
        self.ui.setupUi(self)
        self.gids = []
        self.initActions()


    def initActions(self):
        self.ui.btnAjouter.clicked.connect(self.ajoutDecision)
        self.ui.comboBoxTypeDecision.setEnabled(False)
        self.ui.lineEditNumDecision.setEnabled(False)

        self.ui.checkBoxTypeDecision.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxNumDecision.stateChanged.connect(self.setupFieldsStatus)

        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.tableWidget.setSelectionBehavior(1)

        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnSelectionner.clicked.connect(self.SelActe)
        self.ui.tableWidget.cellClicked.connect(self.cellSelected)
        self.ui.tableWidget.setSelectionBehavior(1)

    def  SelActe(self):
        print "SelActe"
        print self.idDecision
        if self.idDecision == 0 :
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins sélécionner une ligne")
        else :
            self.parent.idActe = self.idDecision
    def cellSelected(self, row):
        #ID = self.gids[row]
        ID = self.ui.tableWidget.item(row, 4).text()
        self.idDecision = int(ID)
    def ajoutDecision(self):
        from .DecisionAnnulationRun import DecisionAnnulation
        decision = DecisionAnnulation(self)
        decision.exec_()


    def setupFieldsStatus(self):

        self.ui.comboBoxTypeDecision.setEnabled(self.ui.checkBoxTypeDecision.isChecked())
        self.ui.lineEditNumDecision.setEnabled(self.ui.checkBoxNumDecision.isChecked())


        if self.ui.checkBoxNumDecision.isChecked() != True:
            self.ui.lineEditNumDecision.clear()



    def add_valuest(self, data):
        i = 0
        j = 0
        nb_row = len(data)
        lignes = len(data)
        columns = 4
        self.gids[:] = []
        self.ui.tableWidget.setRowCount(nb_row)
        self.ui.tableWidget.setColumnCount(columns)
        self.ui.tableWidget.setRowCount(0)

        while i < len(data):

            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.gids.append(data[i][0])

            print " self.gids.append(data[i][0]) in"
            print self.gids
            print " self.gids.append(data[i][0]) out"

            for j in range(columns):

                if( str(data[i][j]) != "" or  str(data[i][j]) != None ) :
                    if((j == 2)) :
                        item = QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y'))
                        item.setText(_translate("", str(data[i][j]), None))
                        self.ui.tableWidget.setItem(rowPosition, j, item)
                        #self.ui.tableWidget.setItem(rowPosition, j - 1,QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                    else :
                        item = QtGui.QTableWidgetItem(str(data[i][j]))
                        item.setText(_translate("", str(data[i][j]), None))
                        self.ui.tableWidget.setItem(i, j, item)
                else :
                    print str(data[i][j])
            i = i + 1
    def showAll(self):
        print "dfsdf"
        self.cur.execute("SELECT numerodecision,typedecision,datedecision,iddecision  FROM decision "
                         " WHERE idprojet=%s", [int(self.id_projet)])
        data = self.cur.fetchall()
        self.add_valuest(data)

    def readInput(self):
        data = {}

        if self.ui.checkBoxTypeDecision.isChecked():
            data['typedecision'] = unicode(str(self.ui.comboBoxDecisionDu.currentText())).encode('utf-8')

        else:
            data['typedecision'] = ''

        if self.ui.checkBoxNumDecision.isChecked():
            data['numerodecision'] = unicode(self.ui.lineEditNumDecision.text()).encode('utf-8')
        else:
            data['numerodecision'] = ''

        self.rechercher(data)

    def rechercher(self, data):
        flag = 0
        listeParams = []
        # SQL = "SELECT pd.gid, pd.numdemande, d.datedemande, d.datereconnaissance, pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid "
        SQL = " SELECT numerodecision,typedecision,datedecision,iddecision FROM decision " \
              " where  "

        SQL = SQL + "  idprojet = %s"
        data['idprojet'] = int(self.id_projet)
        listeParams.append(data['idprojet'])

        if self.ui.checkBoxTypeDecision.isChecked():
            #data['dateenregistrement'] = "%"+data['dateenregistrement']+"%"
            SQL = SQL + "  AND typedecision = %s  "
            listeParams.append(data['typedecision'])
            flag = 1
        if self.ui.checkBoxNumDecision.isChecked():
            if flag == 1:
                data['numerodecision'] = "%" + data['numerodecision'] + "%"
                SQL = SQL + " AND numerodecision  LIKE %s"
                listeParams.append(data['numerodecision'])
            else:
                data['numerodecision'] = "%" + data['numerodecision'] + "%"
                SQL = SQL + "  AND numerodecision   LIKE %s"
                listeParams.append(data['numerodecision'])
                flag = 1

        print
        SQL
        if flag == 1:
            # SQL = SQL + "and pd.idcertificat IS NULL"
            params = tuple(listeParams)
            try:
                self.cur.execute(SQL, params)
                results = self.cur.fetchall()
                # print results
                self.add_valuest(results)
            except StandardError as e:
                print e
        else:
            print
            "Aucun critere de recherche selectionne"
            QMessageBox.information(self.ui.tableWidget, "Erreur", "Aucun critere de recherche selectionne ")
            self.ui.tableWidget.setRowCount(0)



