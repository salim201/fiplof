# -*- coding: utf-8 -*-
import qgis, time, datetime
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from .ListeActeDeces import Ui_Dialog



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
class ListeActeDeces(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
        self.details = []
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        self.connection = self.parent.connection
        self.cur = self.parent.connection.cursor()
#       print self.parent.txt
        self.ui.setupUi(self)
        self.gids = []
        self.IdActeDeces  = 0
        self.initActions()



    def initActions(self):
        self.ui.btnAjouter.clicked.connect(self.ajoutActeDeces)
        self.ui.dateEditActeDeces.setEnabled(False)
        self.ui.lineEditNumActe.setEnabled(False)
        self.ui.checkBoxDateEnregistrement.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxNumActe.stateChanged.connect(self.setupFieldsStatus)

        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.cellClicked.connect(self.cellSelected)
        self.ui.btnSelectionner.clicked.connect(self.SelActe)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnDetail.clicked.connect(self.Details)

    def Details(self):

        if int(self.IdActeDeces) != 0 :
            self.idActe = self.IdActeDeces
            cursor = self.connection.cursor()
            cursor.execute("SELECT *  FROM actedeces where idactedeces = %s",[int(self.IdActeDeces)])
            dm = cursor.fetchone()
            self.details = dm
            from .ActeDecesRun import ActeDeces
            actedeces = ActeDeces(self)
            actedeces.exec_()

    def cellSelected(self, row):
        #ID = self.gids[row]
        ID = self.ui.tableWidget.item(row, 4).text()
        self.IdActeDeces = int(ID)
    def  SelActe(self):
        print "SelActe"
        print self.IdActeDeces
        if self.IdActeDeces == 0 :
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins sélécionner une ligne")
        else :
            print "self.IdActeDeces IN"
            print self.IdActeDeces
            self.parent.IdActeDeces = self.IdActeDeces
            print "self.parent.IdActeDeces  IN"
            print self.parent.IdActeDeces
        self.close()

    def setupFieldsStatus(self):

        self.ui.dateEditActeDeces.setEnabled(self.ui.checkBoxDateEnregistrement.isChecked())
        self.ui.lineEditNumActe.setEnabled(self.ui.checkBoxNumActe.isChecked())
        if self.ui.checkBoxDateEnregistrement.isChecked() != True:
            self.ui.dateEditActeDeces.clear()

        if self.ui.checkBoxNumActe.isChecked() != True:
            self.ui.lineEditNumActe.clear()


    def add_valuest(self, data):
        i = 0
        j = 0
        nb_row = len(data)
        lignes = len(data)
        columns = 5
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
                    if((j == 2) or (j==3)):
                        print ("j = " + str(j))
                        print (str(data[i][j]))
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
        try:
            self.cur.execute("SELECT numeroactedeces,numeroactenotoriete,dateactenotoriete,dateactedeces,idactedeces "
                           "  FROM actedeces "
                           " where idprojet=%s and lance = %s ",
                             [int(self.id_projet),int(typeacte)])
            #self.cur.execute("SELECT numeroactedeces,numeroactenotoriete,dateactenotoriete,dateactedeces,idactedeces FROM actedeces WHERE idprojet=%s", [int(self.id_projet)])
            data = self.cur.fetchall()
            self.add_valuest(data)
        except Exception as err:
            print (err)



    def readInput(self):
        data = {}

        if self.ui.checkBoxDateEnregistrement.isChecked():
            data['dateactedeces'] = datetime.date(self.ui.dateEditActeDeces.date().year(), self.ui.dateEditActeDeces.date().month(), self.ui.dateEditActeDeces.date().day())
        else :
            data['dateactedeces'] = ''

        if self.ui.checkBoxNumActe.isChecked():
            data['numeroactedeces'] = unicode(self.ui.lineEditNumActe.text()).encode('utf-8')
        else :
            data['numeroactedeces'] = ''


        print " data in "
        print data
        print " data out "
        self.rechercher(data)

    def rechercher(self, data):
        flag = 0
        listeParams =[]
        #SQL = "SELECT pd.gid, pd.numdemande, d.datedemande, d.datereconnaissance, pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid "
        SQL = "SELECT numeroactedeces,numeroactenotoriete,dateactenotoriete,dateactedeces,idactedeces FROM actedeces WHERE"

        print " SQL in"
        print data['dateactedeces']
        print "SQL out"
        SQL = SQL + "  idprojet = %s"
        data['idprojet'] = int(self.id_projet)
        listeParams.append(data['idprojet'])

        if self.ui.checkBoxDateEnregistrement.isChecked():
            #data['dateenregistrement'] = "%"+data['dateenregistrement']+"%"
            SQL = SQL + "  AND dateactedeces >= %s  "
            listeParams.append(data['dateactedeces'])
            flag = 1
        if self.ui.checkBoxNumActe.isChecked():
            if flag == 1:
                data['numeroactedeces'] = "%"+data['numeroactedeces']+"%"
                SQL = SQL + " AND numeroactedeces LIKE %s"
                listeParams.append(data['numeroactedeces'])
            else:
                data['numeroactedeces'] = "%" + data['numeroactedeces'] + "%"
                SQL = SQL + "  AND numeroactedeces LIKE %s"
                listeParams.append(data['numeroactedeces'])
                flag = 1


        if flag == 1:
            #SQL = SQL + "and pd.idcertificat IS NULL"
            print " listeParams in"
            print listeParams
            print " listeParams out "
            params = tuple(listeParams)
            try:
                print " params in"
                print SQL
                print " params out "

                self.cur.execute(SQL, params)
                results = self.cur.fetchall()
                #print results
                self.add_valuest(results)
            except StandardError as e:
                print e
        else:
            print "Aucun critere de recherche selectionne"
            QMessageBox.information(self.ui.tableWidget, "Erreur", "Aucun critere de recherche selectionne ")
            self.ui.tableWidget.setRowCount(0)



    def ajoutActeDeces(self):
        from .ActeDecesRun import ActeDeces
        actedeces = ActeDeces(self)
        actedeces.exec_()


