# -*- coding: utf-8 -*-
import qgis, time, datetime
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from .ListeActePrives import Ui_Dialog

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
class ListeActePrives(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
        self.details = []
        self.IdActePrivee = 0
        print "init"
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        self.connection = self.parent.connection
        self.cur = self.parent.connection.cursor()
#       print self.parent.txt
        self.ui.setupUi(self)
        self.gids = []
        self.initActions()

    def setupFieldsStatus(self):

        self.ui.dateEditEnregistrement.setEnabled(self.ui.checkBoxDateEnregistrement.isChecked())
        self.ui.lineEditNumActe.setEnabled(self.ui.checkBoxNumActe.isChecked())
        if self.ui.checkBoxDateEnregistrement.isChecked() != True:
            self.ui.dateEditEnregistrement.clear()

        if self.ui.checkBoxNumActe.isChecked() != True:
            self.ui.lineEditNumActe.clear()
    def initActions(self):
        self.ui.btnAjouter.clicked.connect(self.ajoutActePrive)
        self.ui.dateEditEnregistrement.setEnabled(False)
        self.ui.lineEditNumActe.setEnabled(False)
        self.ui.checkBoxDateEnregistrement.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxNumActe.stateChanged.connect(self.setupFieldsStatus)

        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnSelectionner.clicked.connect(self.SelActe)
        self.ui.tableWidget.cellClicked.connect(self.cellSelected)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.btnDetail.clicked.connect(self.show)

    def show(self):

        cursor = self.connection.cursor()
        cursor.execute("SELECT *  FROM acteprive where idacteprive = %s", [int(self.IdActePrivee)])
        dm = cursor.fetchone()
        self.details = dm
        from .ActePriveRun import ActePrive
        try:
            acteprive = ActePrive(self)
            acteprive.exec_()
        except Exception as err:
            print err
    def fermer(self):
        self.close()

    def  SelActe(self):
        print "SelActe"
        print self.IdActePrivee
        if self.IdActePrivee == 0 :
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins sélécionner une ligne")
        else :
            self.parent.idActe = self.IdActePrivee
            self.parent.idActe = self.IdActePrivee
            self.parent.IdActePrivee = self.IdActePrivee
            print "self.parent.IdActePublic"
        self.parent.close()
        self.close()

    def cellSelected(self, row):
        #ID = self.gids[row]
        print " IdActePrivee selected "
        ID = self.ui.tableWidget.item(row, 5).text()
        self.IdActePrivee = int(ID)
        self.parent.IdActePrivee = int(ID)
        print self.IdActePrivee

    def ajoutActePrive(self):
        from .ActePriveRun import ActePrive
        try:
            acteprive = ActePrive(self)
            acteprive.exec_()
        except Exception as err:
            print err

    def add_valuest(self, data):
        i = 0
        j = 0

        nb_row = len(data)
        lignes = len(data)
        columns = 6
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
                    if((j == 1) or (j == 2)) :
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
        typeacte = 0
        self.cur.execute("SELECT numeroacteprive,dateenregistrement,datelegalisationsignature,valeurtransaction,nombreoperation,idacteprive "
                         " FROM acteprive WHERE idprojet=%s and lance = %s", [int(self.id_projet),int(typeacte)])
        data = self.cur.fetchall()

        print "DATADATDTA"
        print data

        self.add_valuest(data)

    def readInput(self):
        data = {}

        if self.ui.checkBoxDateEnregistrement.isChecked():
            data['dateenregistrement'] = datetime.date(self.ui.dateEditEnregistrement.date().year(),
                                                       self.ui.dateEditEnregistrement.date().month(),
                                                       self.ui.dateEditEnregistrement.date().day())

        else:
            data['dateenregistrement'] = ''

        if self.ui.checkBoxNumActe.isChecked():
            data['numeroacteprive'] = unicode(self.ui.lineEditNumActe.text()).encode('utf-8')
        else:
            data['numeroacteprive'] = ''

        self.rechercher(data)

    def rechercher(self, data):
        flag = 0
        listeParams = []
        # SQL = "SELECT pd.gid, pd.numdemande, d.datedemande, d.datereconnaissance, pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid "
        SQL = " SELECT numeroacteprive,dateenregistrement,datelegalisationsignature,valeurtransaction,nombreoperation ,idacteprive FROM acteprive" \
              " where  "

        SQL = SQL + "  idprojet = %s"
        data['idprojet'] = int(self.id_projet)
        listeParams.append(data['idprojet'])

        if self.ui.checkBoxDateEnregistrement.isChecked():
            # data['dateenregistrement'] = "%"+data['dateenregistrement']+"%"
            SQL = SQL + "  AND dateenregistrement >= %s  "
            listeParams.append(data['dateenregistrement'])
            flag = 1
        if self.ui.checkBoxNumActe.isChecked():
            if flag == 1:
                data['numeroacteprive'] = "%" + data['numeroacteprive'] + "%"
                SQL = SQL + " AND numeroacteprive  LIKE %s"
                listeParams.append(data['numeroacteprive'])
            else:
                data['numeroacteprive'] = "%" + data['numeroacteprive'] + "%"
                SQL = SQL + "  AND numeroacteprive   LIKE %s"
                listeParams.append(data['numeroacteprive'])
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

