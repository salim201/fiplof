import os, os.path, sys
from Widgets.ReadonlyTable import ReadonlyTable
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
import psycopg2, time, datetime
from Utilisateur import AccesManager

from .ListePersonneMorale import Ui_Dialog

#sys.setdefaultencoding('utf-8')

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ListePersonneMoraleRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        from .ListeTypePersonneMoraleRun import ListeTypePersonneMoraleRun
        self.typePersonneMorale = ListeTypePersonneMoraleRun(self.connection)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        #***Utile pour la pagination****#
        self.isShowAll = False
        self.nombreDePage = None
        self.ui.lineEditNumPage.setText("1")
        #***fin utile pour la paginaion***#
        self.initDB()
        self.initActions()
        self.fillComboType()
        self.idpersonnes = []
        self.idpersonne = None
        #self.idPersonneMorale = None

    def initActions(self):
        manager = AccesManager.AccessManager(self, self.connection)
        manager.activate_widget("PERSONNE_MORALE/CREATE", self.ui.pushButtonAjouter)

        self.ui.pushButton_6.clicked.connect(self.ouvrirPersonneMorale)
        self.ui.tableWidget.cellDoubleClicked.connect(self.ouvrirPersonneMorale)
        self.ui.pushButton_4.clicked.connect(self.showAll)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        self.ui.pushButton_2.clicked.connect(self.readInput)
        self.ui.pushButtonAjouter.clicked.connect(self.ajouter)
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        #***Utiles pour la pagination****#
        self.ui.btnDebut.clicked.connect(self.debut)
        self.ui.btnPrecedent.clicked.connect(self.precedent)
        self.ui.btnSuivant.clicked.connect(self.suivant)
        self.ui.btnFin.clicked.connect(self.fin)
        self.ui.comboBoxNumPage.activated.connect(self.updatePage)
        #*****fin utiles pour pagination*****#

    def ajouter(self):
        from .PersonneMoraleRun import PersonneMoraleRun
        try:
            w = PersonneMoraleRun(self.connection, self)
            w.consultation(0)
            if w.exec_():
                self.showAll()
        except Exception as err:
            print(err)

    def ouvrirPersonneMorale(self):
        if self.idpersonne is None:
            return
        from .PersonneMoraleRun import PersonneMoraleRun
        self.personne = PersonneMoraleRun(self.connection, self)
        self.personne.consultation(2)
        self.personne.ui.btnOk.clicked.connect(self.savePersonneMorale)
        try:
            result = self.personne.exec_()
        except StandardError as e:
            print e

    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart

    def showAll(self):
        #***prepa pagination****#
        self.ui.comboBoxNumPage.clear()
        self.isShowAll = True
        count = []
        listeParams = []
        numeropage = int(self.ui.lineEditNumPage.text())
        limite = 20
        #print numeropage
        offset = limite * (numeropage - 1)
        listeParams.append(limite)
        listeParams.append(offset)
        params = tuple(listeParams)
        try:
            self.cur.execute("SELECT COUNT(*) FROM personnemorale")
            count = self.cur.fetchone()
        except StandardError as e:
            #self.connection.rollback()
            print(e)
        #***fin prepa paination***#
        # *****CALCUL DU NOMBRE TOTAL DE PAGES****************#
        if count[0] <= 20:
            self.nombreDePage = 1
        else:
            nbrDePage = count[0] / 20
            reste = count[0] % 20
            if reste > 0:
                self.nombreDePage = nbrDePage + 1
            else:
                self.nombreDePage = nbrDePage

        i = 1
        while i <= self.nombreDePage:
            item = str(i) + "/" + str(self.nombreDePage)
            if self.ui.comboBoxNumPage.findText(item) == -1:
                self.ui.comboBoxNumPage.addItem(item)
            i = i + 1

        self.ui.comboBoxNumPage.setCurrentIndex(numeropage - 1)

        print "Nombre de page = " + str(self.nombreDePage)
            # ******FIN CALCUL DU NOMBRE DE PAGES******************#
        SQL = "SELECT pm.idpersonnemorale, pm.denomination, pm.datecreation, pm.siege, pm.observation, pm.idtype, tpm.type, tpm.idtype FROM personnemorale pm, typepersonnemorale tpm WHERE pm.idtype=tpm.idtype"
        #self.cur.execute("SELECT pm.idpersonnemorale, pm.denomination, pm.datecreation, pm.siege, pm.observation, pm.idtype, tpm.type, tpm.idtype FROM personnemorale pm, typepersonnemorale tpm WHERE pm.idtype=tpm.idtype")
        data = self.pagination(SQL, params)
        #self.showInTable(results)
        #data = self.cur.fetchall()
        self.showInTable(data)

    def showInTable(self, data):
        self.idpersonnes = map(lambda row: row[0], data)
        readonlyTable = ReadonlyTable(self.ui.tableWidget, self.getCellValue)
        readonlyTable.fillWithData(data)

    def getCellValue(self, data, rowIndex, columnIndex):
        row = data[rowIndex]
        if columnIndex == 0:
            return unicode(row[6])
        if columnIndex == 2:
            return unicode(row[columnIndex].strftime('%d/%m/%Y'))
        return unicode(row[columnIndex])


    def selectionLigne(self, row):
        #print row
        self.idpersonne = self.idpersonnes[row]
        #print self.idpersonne
        #self.personne.getPersonneById(self.idpersonne)
        #self.ui.comboBox.setCurrentIndex(int(self.idpersonne) - 1)
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 1).text())

    def fillComboType(self):
        self.cur.execute("SELECT * FROM typepersonnemorale")
        data = self.cur.fetchall()
        i = 0
        while i < len(data):
            print data[i][0]
            self.ui.comboBox.addItem(data[i][1], data[i][0])
            i = i + 1

    def readInput(self):
        print "read input"
        data = {}
        try:
            data['type'] = unicode(self.ui.comboBox.currentText()).encode('utf-8')
        except StandardError as e:
            print e
        print data['type']
        data['nom'] = unicode(self.ui.lineEdit.text()).encode('utf-8')
        self.rechercherPersMorale(data)

    def rechercherPersMorale(self, data):
        #**prepa pagination***#
        self.ui.comboBoxNumPage.clear()
        self.isShowAll = False
        count = []
        numeropage = int(self.ui.lineEditNumPage.text())
        limite = 20
        listeParamsPagination = []
        # print numeropage
        offset = limite * (numeropage - 1)
        listeParamsPagination.append(limite)
        listeParamsPagination.append(offset)
        #***fin prepa pagination****#
        SQL = "SELECT pm.idpersonnemorale, pm.denomination, pm.datecreation, pm.siege, pm.observation, pm.idtype, tpm.type, tpm.idtype FROM personnemorale pm, typepersonnemorale tpm WHERE pm.idtype=tpm.idtype AND tpm.type = %s "
        SQL_count = "SELECT COUNT(*) FROM personnemorale pm, typepersonnemorale tpm WHERE pm.idtype=tpm.idtype AND tpm.type = %s "
        listeParams = []
        listeParams.append(data['type'])
        if data['nom'] != "":
            SQL = SQL + "AND pm.denomination = %s "
            SQL_count = SQL_count + "AND pm.denomination = %s "
            listeParams.append(data['nom'])

        paramsCount = tuple(listeParams)
        try:
            self.cur.execute(SQL_count, paramsCount)
            count = self.cur.fetchone()
        except StandardError as e:
            print(e)

        # *****CALCUL DU NOMBRE TOTAL DE PAGES****************#
        if count[0] <= 20:
            self.nombreDePage = 1
        else:
            nbrDePage = count[0] / 20
            reste = count[0] % 20
            if reste > 0:
                self.nombreDePage = nbrDePage + 1
            else:
                self.nombreDePage = nbrDePage

        i = 1
        while i <= self.nombreDePage:
            item = str(i) + "/" + str(self.nombreDePage)
            if self.ui.comboBoxNumPage.findText(item) == -1:
                self.ui.comboBoxNumPage.addItem(item)
            i = i + 1

        self.ui.comboBoxNumPage.setCurrentIndex(numeropage - 1)

        print "Nombre de page = " + str(self.nombreDePage)

        # ******FIN CALCUL DU NOMBRE DE PAGES******************#
        listeParams = listeParams + listeParamsPagination
        params = tuple(listeParams)
        results = self.pagination(SQL, params)
        self.showInTable(results)
        #try:
            #self.cur.execute(SQL, params)
            #results = self.cur.fetchall()
            #print results
            #self.showInTable(results)
        #except StandardError as e:
            #print e

            # ****************************** FONCTIONS UTILES A LA PAGINATION ************************************#

    def pagination(self, SQL, params):
        print "Appel pagination"
        SQL = SQL + " LIMIT %s OFFSET %s"
        print SQL
        try:
            self.cur.execute(SQL, params)
            data = self.cur.fetchall()
            # print data
            return data
        except StandardError as e:
            print (e)

    def debut(self):
        self.ui.lineEditNumPage.setText("1")
        if self.isShowAll:
            self.showAll()
        else:
            self.readInput()

    def precedent(self):
        NumPageActuel = int(self.ui.lineEditNumPage.text())
        Numpage = 1
        if NumPageActuel > 1:
            NumPage = NumPageActuel - 1
        else:
            NumPage = 1
        self.ui.lineEditNumPage.setText(str(NumPage))
        if self.isShowAll:
            self.showAll()
        else:
            self.readInput()

    def suivant(self):
        print "suivant"
        NumPageActuel = int(self.ui.lineEditNumPage.text())
        if NumPageActuel < self.nombreDePage:
            NumPage = NumPageActuel + 1
        else:
            NumPage = self.nombreDePage

        self.ui.lineEditNumPage.setText(str(NumPage))
        if self.isShowAll:
            self.showAll()
        else:
            self.readInput()

    def fin(self):
        self.ui.lineEditNumPage.setText(str(self.nombreDePage))
        if self.isShowAll:
            self.showAll()
        else:
            self.readInput()

    def updatePage(self):
        if self.ui.comboBoxNumPage.currentIndex() != -1:
            text = str(self.ui.comboBoxNumPage.currentText()).split("/")
            NumPage = int(text[0])
            self.ui.lineEditNumPage.setText(str(NumPage))
            if self.isShowAll:
                self.showAll()
            else:
                self.readInput()

                # ******************FIN FONCTIONS UTILES A LA PAGINATION ************************#

    def getIdPersonne(self):
        return self.idpersonne

    def savePersonneMorale(self):
        if self.personne.readInput():
            self.personne.close()
