# -*- coding: utf-8 -*-
import os, os.path, sys, psycopg2, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4 import QtGui

from qgis.gui import *
import globalvars

from .listePersonnesPque import Ui_Dialog

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ListePersonnePqueRun(QDialog):
    def __init__(self, connection):
        QDialog.__init__(self)
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.fromOps = 0
        print "Construction Liste Personne physique"
        #self.connection = connection
        from .PersonnePhysiqueRun import PersonnePhysiqueRun
        self.personne = PersonnePhysiqueRun(self.connection)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        #***Utile pour la pagination****#
        self.isShowAll = False
        self.nombreDePage = None
        self.ui.lineEditNumPage.setText("1")
        #***fin utile pour la paginaion***#
        self.initActions()
        self.initDB()
        self.setWindowTitle("Liste des personnes physiques")
        self.disableAll()
        self.idpersonnes = []
        self.initMasks()
        print "fin construction liste personne physique"

    def initActions(self):
        self.ui.btnDetails.clicked.connect(self.ouvrirPersonnePque)
        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        self.ui.btnAjouter.clicked.connect(self.ajouterPersonne)
        self.ui.checkBoxNom.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxPrenom.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomPere.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomMere.stateChanged.connect(self.updateFieldsState)
        self.ui.radioButtonCIN.clicked.connect(self.updateFieldsState)
        self.ui.radioButtonNumActN.clicked.connect(self.updateFieldsState)
        self.ui.radioButtonRien.clicked.connect(self.updateFieldsState)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.lineEditNom.textEdited.connect(self.readInput)
        self.ui.lineEditPrenom.textEdited.connect(self.readInput)
        self.ui.lineEditNomPere.textEdited.connect(self.readInput)
        self.ui.lineEditNomMere.textEdited.connect(self.readInput)
        self.ui.lineEditCIN.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN_1.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN_2.textEdited.connect(self.nextFields)
        self.ui.lineEditCIN.textEdited.connect(self.readInput)
        self.ui.lineEditCIN_1.textEdited.connect(self.readInput)
        self.ui.lineEditCIN_2.textEdited.connect(self.readInput)
        self.ui.lineEditCIN_3.textEdited.connect(self.readInput)
        self.personne.ui.btnOk.clicked.connect(self.enregistrerPersonnePque)
        #***Utiles pour la pagination****#
        self.ui.btnDebut.clicked.connect(self.debut)
        self.ui.btnPrecedent.clicked.connect(self.precedent)
        self.ui.btnSuivant.clicked.connect(self.suivant)
        self.ui.btnFin.clicked.connect(self.fin)
        self.ui.comboBoxNumPage.activated.connect(self.updatePage)
        self.ui.btnFermer.clicked.connect(self.close)
        #*****fin utiles pour pagination*****#


    def ajouterPersonne(self):
        try:
            self.personne.consultation(0)
            result = self.personne.exec_()
        except StandardError as e:
            print e

    def ouvrirPersonnePque(self):
        try:
            self.personne.consultation(2)
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
            self.cur.execute("SELECT COUNT(*) FROM personnephysique")
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
        SQL = "SELECT idpersonne, nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, numcipersonne, numactenaissancepersonne  FROM personnephysique ORDER BY(idpersonne)"
        results = self.pagination(SQL, params)
        self.showInTable(results)
        #try:
            #self.cur.execute("SELECT idpersonne, nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, numcipersonne, numactenaissancepersonne  FROM personnephysique")
            #results = self.cur.fetchall()
            #self.showInTable(results)
        #except StandardError as e:
            #print e

    def showInTable(self, data):
        print "debut donnees personne physiques"
        print data
        print "fin donnees personne physiques"
        self.idpersonnes[:] = []
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.idpersonnes.append(data[i][0])
            j = 1
            while j < len(data[i]):
                if data[i][j] != None:
                    if j == 3:
                        if data[i][j]:
                            try:
                                self.ui.tableWidget.setItem(rowPosition, j - 1, QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                            except StandardError as e:
                                print "erreur ao amin'ny manipulation des dates: "
                                print e
                            j = j + 1
                    else:
                        self.ui.tableWidget.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(data[i][j])))
                        j = j + 1
                else:
                    self.ui.tableWidget.setItem(rowPosition, j - 1, QTableWidgetItem(""))
                    j = j + 1
            i = i + 1

    def selectionLigne(self, row):
        self.idpersonne = self.idpersonnes[row]
        self.personne.getPersonneById(self.idpersonne)
        #self.choix.getDemandeNum(numDemande, self.cur)

    def getIdPersonne(self):
        return self.idpersonne

    def disableAll(self):
        self.ui.lineEditNom.setDisabled(True)
        self.ui.lineEditPrenom.setDisabled(True)
        self.ui.lineEditNomPere.setDisabled(True)
        self.ui.lineEditNomPere.setDisabled(True)
        self.ui.lineEditNomMere.setDisabled(True)
        self.ui.lineEditCIN.setDisabled(True)
        self.ui.lineEditCIN_2.setDisabled(True)
        self.ui.lineEditCIN_3.setDisabled(True)
        self.ui.lineEditCIN_1.setDisabled(True)
        self.ui.lineEditNumActN.setDisabled(True)

    def updateFieldsState(self):
        self.ui.lineEditNom.setEnabled(self.ui.checkBoxNom.isChecked())
        if self.ui.checkBoxNom.isChecked() != True:
            self.ui.lineEditNom.clear()
        self.ui.lineEditPrenom.setEnabled(self.ui.checkBoxPrenom.isChecked())
        if self.ui.checkBoxPrenom.isChecked() != True:
            self.ui.lineEditPrenom.clear()
        self.ui.lineEditNomPere.setEnabled(self.ui.checkBoxNomPere.isChecked())
        if self.ui.checkBoxNomPere.isChecked() != True:
            self.ui.lineEditNomPere.clear()
        self.ui.lineEditNomMere.setEnabled(self.ui.checkBoxNomMere.isChecked())
        if self.ui.checkBoxNomMere.isChecked() != True:
            self.ui.lineEditNomMere.clear()
        if self.ui.radioButtonCIN.isChecked():
            self.ui.lineEditCIN.setEnabled(True)
            self.ui.lineEditCIN_2.setEnabled(True)
            self.ui.lineEditCIN_1.setEnabled(True)
            self.ui.lineEditCIN_3.setEnabled(True)
            self.ui.lineEditNumActN.setDisabled(True)
        if self.ui.radioButtonNumActN.isChecked():
            self.ui.lineEditCIN.setEnabled(False)
            self.ui.lineEditCIN_2.setEnabled(False)
            self.ui.lineEditCIN_1.setEnabled(False)
            self.ui.lineEditCIN_3.setEnabled(False)
            self.ui.lineEditNumActN.setDisabled(False)
        if self.ui.radioButtonRien.isChecked():
            self.ui.lineEditCIN.setEnabled(False)
            self.ui.lineEditCIN_2.setEnabled(False)
            self.ui.lineEditCIN_1.setEnabled(False)
            self.ui.lineEditCIN_3.setEnabled(False)
            self.ui.lineEditNumActN.setDisabled(True)
        #self.ui.dateEditDateDemande.setEnabled(self.ui.checkBoxDu.isChecked())
        #self.ui.dateEditDateDemande.clear()
        #self.ui.dateEditDateDemandeFin.setEnabled(self.ui.checkBoxAu.isChecked())
        #self.ui.dateEditDateDemandeFin.clear()
        #self.ui.comboBoxFokotany.setEnabled(self.ui.checkBoxFokontany.isChecked())
        #self.ui.comboBoxFokotany.clear()

    def readInput(self):
        print "read input"
        data = {}
        data['nom'] = unicode(self.ui.lineEditNom.text()).encode('utf-8')
        data['prenom'] = unicode(self.ui.lineEditPrenom.text()).encode('utf-8')
        data['nompere'] = unicode(self.ui.lineEditNomPere.text()).encode('utf-8')
        data['nommere'] = unicode(self.ui.lineEditNomMere.text()).encode('utf-8')
        data['cin'] = unicode(self.ui.lineEditCIN.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_1.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_2.text()).encode('utf-8') + unicode(self.ui.lineEditCIN_3.text()).encode('utf-8')
        data['numacte'] = unicode(self.ui.lineEditNumActN.text()).encode('utf-8')

        self.rechercher(data)

    def rechercher(self, data):
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
        print "rechercher"
        flag = 0
        print flag
        print data
        listeParams = []
        SQL = "SELECT idpersonne, nompersonne, prenompersonne, datenaissancepersonne, sexepersonne, adressepersonne, numcipersonne, numactenaissancepersonne  FROM personnephysique "
        SQL_count = "SELECT COUNT(*) FROM personnephysique " #Utile pour compter le resultat total de la requette
        print SQL
        if self.ui.checkBoxNom.isChecked():
            data['nom'] = "%" + data['nom'].lower() + "%"
            listeParams.append(data['nom'])
            if flag == 0:
                SQL = SQL + "WHERE LOWER(nompersonne) LIKE %s "
                SQL_count = SQL_count + "WHERE LOWER(nompersonne) LIKE %s "
                flag = 1
            else:
                SQL = SQL + "AND LOWER(nompersonne) LIKE %s "
                SQL_count = SQL + "AND LOWER(nompersonne) LIKE %s "
        if self.ui.checkBoxPrenom.isChecked():
            data['prenom'] = "%" + data['prenom'].lower() + "%"
            listeParams.append(data['prenom'])
            if flag == 0:
                SQL = SQL + "WHERE LOWER(prenompersonne) LIKE %s "
                SQL_count = SQL_count + "WHERE LOWER(prenompersonne) LIKE %s "
                flag = 1
            else:
                SQL = SQL + "AND LOWER(prenompersonne) LIKE %s "
                SQL_count = SQL_count + "AND LOWER(prenompersonne) LIKE %s "
        if self.ui.checkBoxNomPere.isChecked():
            data['nompere'] = "%" + data['nompere'] + "%"
            listeParams.append(data['nompere'])
            if flag == 0:
                SQL = SQL + "WHERE LOWER(nompere) LIKE %s "
                SQL_count = SQL_count + "WHERE LOWER(nompere) LIKE %s "
                flag = 1
            else:
                SQL = SQL + "AND LOWER(nompere) LIKE %s "
                SQL_count = SQL_count + "AND LOWER(nompere) LIKE %s "
        if self.ui.checkBoxNomMere.isChecked():
            data['nommere'] = "%" + data['nommere'] + "%"
            listeParams.append(data['nommere'])
            if flag == 0:
                SQL = SQL + "WHERE LOWER(nommere) LIKE %s "
                SQL_count = SQL_count + "WHERE LOWER(nommere) LIKE %s "
                flag = 1
            else:
                SQL = SQL + "AND LOWER(nommere) LIKE %s "
                SQL_count = SQL_count + "AND LOWER(nommere) LIKE %s "
        if self.ui.radioButtonCIN.isChecked():
            data['cin'] = data['cin'] + "%"
            listeParams.append(data['cin'])
            if flag == 0:
                SQL = SQL + "WHERE numcipersonne LIKE %s "
                SQL_count = SQL_count + "WHERE numcipersonne LIKE %s "
                flag = 1
            else:
                SQL = SQL + "AND numcipersonne LIKE %s "
                SQL_count = SQL_count + "AND numcipersonne LIKE %s "
        if self.ui.radioButtonNumActN.isChecked():
            data['numacte'] = "%" + data['numacte'] + "%"
            listeParams.append(data['numacte'])
            if flag == 0:
                SQL = SQL + "WHERE numactenaissancepersonne LIKE %s "
                SQL_count = SQL_count + "WHERE numactenaissancepersonne LIKE %s "
                flag = 1
            else:
                SQL = SQL + "AND numactenaissancepersonne LIKE %s "
                SQL_count = SQL_count + "AND numactenaissancepersonne LIKE %s "

        print "fin lecture"


        if flag == 1:
            #SQL = SQL + "and pd.idcertificat IS NULL"
            print listeParams
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
        else:
            print "Aucun critere de recherche selectionne"
            self.ui.tableWidget.setRowCount(0)

    ###### Masque de saisie#######
    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEditNom.setValidator(validatorAlpha)
        self.ui.lineEditPrenom.setValidator(validatorAlpha)
        #self.ui.lineEditPrenom.textEdited.connect(self.controlInput)
        self.ui.lineEditNomPere.setValidator(validatorAlpha)
        self.ui.lineEditNumActN.setValidator(validatorNum)
        self.ui.lineEditCIN.setValidator(validatorNum)
        self.ui.lineEditCIN_1.setValidator(validatorNum)
        self.ui.lineEditCIN_2.setValidator(validatorNum)
        self.ui.lineEditCIN_3.setValidator(validatorNum)
        self.ui.lineEditNomMere.setValidator(validatorAlpha)
        self.ui.lineEditCIN.setMaxLength(3)
        self.ui.lineEditCIN_1.setMaxLength(3)
        self.ui.lineEditCIN_2.setMaxLength(3)
        self.ui.lineEditCIN_3.setMaxLength(3)

    def enregistrerPersonnePque(self):
        status = self.personne.readInput()
        if status:
            self.personne.close()

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

    def nextFields(self):
        senderName = self.sender().objectName()
        if senderName == "lineEditCIN" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_1.setFocus()
        if senderName == "lineEditCIN_1" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_2.setFocus()
        if senderName == "lineEditCIN_2" and self.sender().text().length() == 3:
            self.ui.lineEditCIN_3.setFocus()


    def __del__(self):
        self.cur.close()
