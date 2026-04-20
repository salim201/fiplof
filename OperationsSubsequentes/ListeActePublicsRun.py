# -*- coding: utf-8 -*-
import qgis, time, datetime
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from .ListeActePublics import Ui_Dialog

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

class ListeActePublics(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.IdActePublic = 0
        self.details = []
        print "init"

        self.ui = Ui_Dialog()
        self.parent = parent
        self.IdActePublic = 0
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        self.connection = self.parent.connection
        self.cur = self.parent.connection.cursor()
#       print self.parent.txt
        self.ui.setupUi(self)
        self.gids = []
        self.initActions()


    def initActions(self):
        self.ui.btnAjouter.clicked.connect(self.ajoutActePublic)
        self.ui.dateEditEnregistrement.setEnabled(False)
        self.ui.lineEditNumActe.setEnabled(False)
        self.ui.checkBoxDateEnregistrement.stateChanged.connect(self.setupFieldsStatus)
        self.ui.checkBoxNumActe.stateChanged.connect(self.setupFieldsStatus)

        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.tableWidget.cellClicked.connect(self.cellSelected)
        self.ui.btnSelectionner.clicked.connect(self.SelActe)
        self.ui.btnFermer.clicked.connect(self.fermer)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnDetail.clicked.connect(self.show)
        #self.setupFieldsStatus()


    def show(self):

        cursor = self.connection.cursor()
        cursor.execute("SELECT *  FROM actepublic where idactepublic = %s", [int(self.IdActePublic)])
        dm = cursor.fetchone()
        self.details = dm
        from .ActePublicsRun import ActePublic
        actePublic = ActePublic(self)
        #actePublic.
        actePublic.exec_()
    def fermer(self):
        self.close()

    def  SelActe(self):
        print "SelActe"
        print self.IdActePublic
        if self.IdActePublic == 0 :
            QtGui.QMessageBox.information(self, u"Données non séléctionnées",
                                          u"Veuillez au moins sélécionner une ligne")
        else :
            self.parent.idActe = self.IdActePublic
            self.parent.IdActePublic = self.IdActePublic
            print "self.parent.IdActePublic"
        self.parent.close()
        self.close()

    def setupFieldsStatus(self):

        self.ui.dateEditEnregistrement.setEnabled(self.ui.checkBoxDateEnregistrement.isChecked())
        self.ui.lineEditNumActe.setEnabled(self.ui.checkBoxNumActe.isChecked())
        if self.ui.checkBoxDateEnregistrement.isChecked() != True:
            self.ui.dateEditEnregistrement.clear()

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
                    if(j == 1) :
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
        #print "dfsdf"

        typeacte = 0
        self.cur.execute("SELECT numeroactepublic,dateenregistrement,nomofficierpublic,valeurtransaction,idactepublic "
                       "  FROM actepublic "
                       " where idprojet=%s and lance = %s ",
                         [int(self.id_projet),int(typeacte)])
        #self.cur.execute("SELECT numeroactepublic,dateenregistrement,nomofficierpublic,valeurtransaction,idactepublic FROM actepublic WHERE idprojet=%s", [int(self.id_projet)])
        data = self.cur.fetchall()
        self.add_valuest(data)

        # rint len(data[0])

    def cellSelected(self, row):
        #ID = self.gids[row]
        ID = self.ui.tableWidget.item(row, 4).text()
        self.IdActePublic = int(ID)
        print "acte public select"
        print self.IdActePublic

    def readInput(self):
        data = {}

        if self.ui.checkBoxDateEnregistrement.isChecked():
            data['dateenregistrement'] = datetime.date(self.ui.dateEditEnregistrement.date().year(), self.ui.dateEditEnregistrement.date().month(), self.ui.dateEditEnregistrement.date().day())
            print self.ui.dateEditEnregistrement.date().year()
            print self.ui.dateEditEnregistrement.date().month()
            print self.ui.dateEditEnregistrement.date().day()
        else :
            data['dateenregistrement'] = ''

        if self.ui.checkBoxNumActe.isChecked():
            data['numeroactepublic'] = unicode(self.ui.lineEditNumActe.text()).encode('utf-8')
        else :
            data['numeroactepublic'] = ''


        print " data in "
        print data
        print " data out "
        self.rechercher(data)

    def rechercher(self, data):
        flag = 0
        listeParams =[]
        #SQL = "SELECT pd.gid, pd.numdemande, d.datedemande, d.datereconnaissance, pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid "
        SQL = " SELECT numeroactepublic,dateenregistrement,nomofficierpublic,valeurtransaction,idactepublic FROM actepublic" \
              " where  "

        print " SQL in"
        print data['dateenregistrement']
        print "SQL out"

        SQL = SQL + "  idprojet = %s"
        data['idprojet'] = int(self.id_projet)
        listeParams.append(data['idprojet'])

        if self.ui.checkBoxDateEnregistrement.isChecked():
            #data['dateenregistrement'] = "%"+data['dateenregistrement']+"%"
            SQL = SQL + "  AND dateenregistrement >= %s  "
            listeParams.append(data['dateenregistrement'])
            flag = 1
        if self.ui.checkBoxNumActe.isChecked():
            if flag == 1:
                data['numeroactepublic'] = "%"+data['numeroactepublic']+"%"
                SQL = SQL + " AND CAST(numeroactepublic AS varchar(10))  LIKE %s"
                listeParams.append(data['numeroactepublic'])
            else:
                data['numeroactepublic'] = "%" + data['numeroactepublic'] + "%"
                SQL = SQL + "  AND CAST(numeroactepublic AS varchar(10))  LIKE %s"
                listeParams.append(data['numeroactepublic'])
                flag = 1

        print SQL
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


    def ajoutActePublic(self):
        from .ActePublicsRun import ActePublic
        acte = ActePublic(self)
        acte.exec_()