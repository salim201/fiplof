# coding: utf8
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from .Journal import Ui_Dialog
import datetime, time

class journal(QtGui.QDialog): 
    def __init__(self, connection):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        #self.parent = parent
        #print self.parent.txt
        self.ui.setupUi(self)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        self.setWindowTitle("Journal")
        self.connection = connection
        self.idsUser = []
        self.initActions()
        self.initDB()
        self.fillLogin()
        self.updateFieldsStatus()
        self.fillComboGroupAction()
        if self.ui.comboGroupeAction.count() > 0:
            self.ui.comboGroupeAction.setCurrentIndex(0)
        #self.inserToJournal()

    def initActions(self):
        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.tableWidget.cellClicked.connect(self.fillOverTab)
        self.ui.checkBoxLogin.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxDu.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxAu.stateChanged.connect(self.updateFieldsStatus)
        self.ui.chkCritereavancees.stateChanged.connect(self.updateFieldsStatus)
        self.ui.btnRecherche.clicked.connect(self.recherche)
        self.ui.comboGroupeAction.currentIndexChanged.connect(self.fillComboAction)
        self.ui.btnFermer.clicked.connect(self.close)

    def recherche(self):
        data = {}
        if self.ui.checkBoxLogin.isChecked():
            data['login'] = str(self.ui.comboBoxLogin.currentText())
            #print data['login']
        if self.ui.checkBoxDu.isChecked():
            data['du'] = datetime.date(self.ui.dateEditDu.date().year(), self.ui.dateEditDu.date().month(), self.ui.dateEditDu.date().day())
        if self.ui.checkBoxAu.isChecked():
            data['au'] = datetime.date(self.ui.dateEditAu.date().year(), self.ui.dateEditAu.date().month(), self.ui.dateEditAu.date().day())
        print data

        self.showAll(data)



    def fillLogin(self):
        self.idsUser[:] = []
        self.ui.comboBoxLogin.clear()
        try:
            self.cur.execute("SELECT loginutilisateur, idutilisateur FROM utilisateur")
            users = self.cur.fetchall()
            for user in users:
                self.ui.comboBoxLogin.addItem(user[0])
                self.idsUser.append(user[1])
        except StandardError as e:
            print e


    def inserToJournal(self, id_user, idobjetCible = None, typeObjetCible = None, description = None):
        date = datetime.datetime.now()
        print date.date()
        print date.time()
        try:
            self.cur.execute("INSERT INTO journal(idutilisateur, idobjetcible, typeobjectcible, description, dateaction, heureaction) VALUES (%s, %s, %s, %s, %s, %s)",(id_user, idobjetCible, unicode(typeObjetCible).encode('utf-8'), unicode(description).encode('utf-8'), date.date(), date.time()))
            self.connection.commit()
            self.close()
        except StandardError as e:
            print e
            self.connection.rollback()
            self.close()

    def showAll(self, data = None):
        self.ui.tableWidget.setRowCount(0)
        preData = []
        if data is None:
            try:
                self.cur.execute("SELECT u.loginutilisateur, j.idobjetcible, j.typeobjectcible, j.description, j.dateaction, j.heureaction FROM utilisateur u, journal j WHERE u.idutilisateur = j.idutilisateur")
                preData = self.cur.fetchall()
            except StandardError as e:
                print e
        else:
            SQL = "SELECT u.loginutilisateur, j.idobjetcible, j.typeobjectcible, j.description, j.dateaction, j.heureaction FROM utilisateur u, journal j WHERE u.idutilisateur = j.idutilisateur "
            listParams = []
            if self.ui.checkBoxLogin.isChecked():
                SQL = SQL + "AND u.loginutilisateur = %s "
                listParams.append(data['login'])
            if self.ui.checkBoxDu.isChecked() and self.ui.checkBoxAu.isChecked() == False:
                SQL = SQL + "AND j.dateaction >= %s "
                listParams.append(data['du'])
            elif self.ui.checkBoxDu.isChecked() == False and self.ui.checkBoxAu.isChecked():
                SQL = SQL + "AND j.dateaction <= %s "
                listParams.append(data['au'])
            elif self.ui.checkBoxDu.isChecked() and self.ui.checkBoxAu.isChecked():
                SQL = SQL + "AND j.dateaction >= %s AND j.dateaction <= %s "
                listParams.append(data['du'])
                listParams.append(data['au'])

            # Criteres avancees
            if self.ui.chkCritereavancees.isChecked():
                SQL = SQL + " AND j.typeobjectcible = %s AND j.description = %s "
                listParams.append(unicode(self.ui.comboGroupeAction.currentText()).encode('utf-8'))
                listParams.append(unicode(self.ui.comboAction.currentText()).encode('utf-8'))
                if self.ui.lineEditObjet.text() != '':
                    criteria = u"%" + unicode(self.ui.lineEditObjet.text()).encode('utf-8') + u"%"
                    if unicode(self.ui.comboGroupeAction.currentText()).encode('utf-8') == u'Certificat':
                        SQL = SQL + " AND j.idobjetcible IN (SELECT idcertificat FROM certificat WHERE numerocertificat LIKE %s)"
                        listParams.append(criteria)
                    if unicode(self.ui.comboGroupeAction.currentText()).encode('utf-8') == u'Demande':
                        SQL = SQL + " AND j.idobjetcible IN (SELECT iddemande FROM demande WHERE numdemande LIKE %s)"
                        listParams.append(criteria)

            #Execution de la requete
            params = tuple(listParams)
            try:
                self.cur.execute(SQL, params)
                preData = self.cur.fetchall()
            except StandardError as e:
                print e

        for data in preData:
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            numCert = None
            # data
            i = 0
            while i < len(data):

                if i == 0:
                    self.ui.tableWidget.setItem(rowPosition, i , QtGui.QTableWidgetItem(data[i]))
                    #print data[i]
                if i == 4 or i == 5:
                    if i == 4:
                        #print data[i]
                        self.ui.tableWidget.setItem(rowPosition, i - 3,
                                                QtGui.QTableWidgetItem(data[i].strftime('%d/%m/%Y')))
                    if i == 5:
                        #print data[i]
                        self.ui.tableWidget.setItem(rowPosition, i - 3,
                                                    QtGui.QTableWidgetItem(data[i].strftime('%H:%M')))
                if i == 2:
                    #print data[i]
                    if data[i] == 'Certificat':
                        try:
                            self.cur.execute("SELECT numerocertificat FROM certificat WHERE idcertificat = %s", (data[i-1], ))
                            numCert = self.cur.fetchone()
                            if numCert is not None:
                                self.ui.tableWidget.setItem(rowPosition, i + 1, QtGui.QTableWidgetItem(numCert[0]))
                            else:
                                self.ui.tableWidget.setItem(rowPosition, i + 1, QtGui.QTableWidgetItem(''))
                            #print numCert[0]
                        except StandardError as e:
                            print e
                            self.connection.roollback()
                    if data[i] == 'Demande':
                        try:
                            self.cur.execute("SELECT numdemande FROM demande WHERE iddemande = %s", (data[i-1], ))
                            numCert = self.cur.fetchone()
                            if numCert is not None:
                                self.ui.tableWidget.setItem(rowPosition, i + 1, QtGui.QTableWidgetItem(numCert[0]))
                            else:
                                self.ui.tableWidget.setItem(rowPosition, i + 1, QtGui.QTableWidgetItem(''))
                            #print numCert[0]
                        except StandardError as e:
                            print e
                            self.connection.rollback()
                if i == 3:
                    self.ui.tableWidget.setItem(rowPosition, i + 1, QtGui.QTableWidgetItem(data[i]))
                    #print data[i]

                i = i + 1

    def fillOverTab(self):
        self.ui.lineEditLogin.clear()
        self.ui.lineEditDescriptionAction.clear()
        self.ui.lineEditHeureAction.clear()

        self.ui.lineEditLogin.setText(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())
        self.ui.lineEditObjetid.setText(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 3).text())
        self.ui.dateEditAction.setDate(QtCore.QDate(time.strptime(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(),1 ).text(),'%d/%m/%Y' ).tm_year,
                                             time.strptime(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(),1 ).text(),'%d/%m/%Y' ).tm_mon,
                                             time.strptime(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(),1 ).text(),'%d/%m/%Y' ).tm_mday))
        self.ui.lineEditHeureAction.setText(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text())
        self.ui.lineEditDescriptionAction.setText(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 4).text())

    def updateFieldsStatus(self):
        self.ui.comboBoxLogin.setEnabled(self.ui.checkBoxLogin.isChecked())
        self.ui.dateEditAu.setEnabled(self.ui.checkBoxAu.isChecked())
        self.ui.dateEditDu.setEnabled(self.ui.checkBoxDu.isChecked())
        self.ui.groupBox.setEnabled(self.ui.chkCritereavancees.isChecked())

    def fillComboGroupAction(self):
        self.ui.comboGroupeAction.clear()
        self.cur.execute("SELECT DISTINCT typeobjectcible FROM journal")
        groups = self.cur.fetchall()
        for group in groups:
            self.ui.comboGroupeAction.addItem(group[0])

    def fillComboAction(self):
        self.ui.comboAction.clear()
        self.cur.execute("SELECT DISTINCT description FROM journal WHERE typeobjectcible = %s",(unicode(self.ui.comboGroupeAction.currentText()),))
        actions = self.cur.fetchall()
        for action in actions:
            self.ui.comboAction.addItem(action[0])


    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart

    def __del__(self):
            self.cur.close()