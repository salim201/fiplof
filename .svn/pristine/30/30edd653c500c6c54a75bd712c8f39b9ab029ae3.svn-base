# coding: utf-8
import os, os.path, sys
import qgis, time, datetime
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *

from qgis.gui import *
import psycopg2
#sys.setdefaultencoding('utf-8')
from .RechercheDmdeCert import Ui_Dialog
import globalvars

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s



class RechercheDmdeCertRun(QDialog):
    def __init__(self, connection, canvas, parent,stateEdition = 0):
        self.connection = connection
        QDialog.__init__(self)
        self.idparcelle = 0

        # Set up the user interface from Designer.
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.geometryeEdit = []
        #self.registry = self.parent.registry
        self.ui.setupUi(self)
        self.resize(493, 628)

        appStyle = """  
                QTableWidget 
                {

        	        alternate-background-color: #00bfff;
             	    background-color: white;
                }
                """
        self.setStyleSheet(appStyle)
        self.canvas = canvas
        self.parent = parent
        self.registry = self.parent.registry
        self.iface = self.parent.iface
        self.Mcs = self.parent.Mcs
        self.newParcelleCF = self.parent.newParcelleCF
        self.ui.tableWidget.setSelectionBehavior(1)
        self.initActions()
        #***Utile pour la pagination****#
        self.isShowAll = False
        self.nombreDePage = None
        self.ui.lineEditNumPage.setText("1")
        #***fin utile pour la paginaion***#
        self.initDB()
        #from .ConsultationDmdRun import ConsultationDmdRun #tokony antsoina any am Radoris
        #self.demandes = ConsultationDmdRun(self.connection)
        self.gids = []
        self.datesDemandes = []
        #self.idsDemandes = []
        self.disableAll()
        now = QDate.currentDate()
        self.ui.dateEditDateDemande.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditDateDemande.setDate(now)
        self.ui.dateEditDateDemandeFin.setDate(now)
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.numDemande = None
        self.initMasks()
        self.fillComboFokontany()
        self.currentLayer = ""
        self.cvs = ""
        #ilaina am details demande
        self.stateEdition = 0
        self.geomid = 0
        self.tool = parent.tool
        self.iddemande = None
        self.geometryeEdit = None
        self.MainWindow = self.parent.MainWindow
        #self.actiondelVertex = self.parent.ui.actiondelVertex

    def initActions(self):
        self.ui.btnDetail.clicked.connect(self.detailsDemande)
        self.ui.tableWidget.cellDoubleClicked.connect(self.detailsDemande)
        self.ui.btnSelectionner.clicked.connect(self.ouvrirChoixSurParcelle)
        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.checkBoxNumDemande.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxNomDemandeur.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxDu.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxAu.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxFokontany.stateChanged.connect(self.updateFieldsState)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        #***Utiles pour la pagination****#
        self.ui.btnDebut.clicked.connect(self.debut)
        self.ui.btnPrecedent.clicked.connect(self.precedent)
        self.ui.btnSuivant.clicked.connect(self.suivant)
        self.ui.btnFin.clicked.connect(self.fin)
        self.ui.comboBoxNumPage.activated.connect(self.updatePage)
        self.ui.lineEditNumDemande.textEdited.connect(self.readInput)
        self.ui.lineEditNomDemandeur.textEdited.connect(self.readInput)
        self.ui.comboBoxFokotany.currentIndexChanged.connect(self.readInput)
        self.ui.dateEditDateDemande.dateChanged.connect(self.readInput)
        self.ui.dateEditDateDemandeFin.dateChanged.connect(self.readInput)

        #*****fin utiles pour pagination*****#


    def updateFieldsState(self):
        self.ui.lineEditNumDemande.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        if self.ui.checkBoxNumDemande.isChecked() != True:
            self.ui.lineEditNumDemande.clear()
        self.ui.lineEditNomDemandeur.setEnabled(self.ui.checkBoxNomDemandeur.isChecked())
        if self.ui.checkBoxNomDemandeur.isChecked() != True:
            self.ui.lineEditNomDemandeur.clear()
        self.ui.dateEditDateDemande.setEnabled(self.ui.checkBoxDu.isChecked())
        #self.ui.dateEditDateDemande.clear()
        self.ui.dateEditDateDemandeFin.setEnabled(self.ui.checkBoxAu.isChecked())
        #self.ui.dateEditDateDemandeFin.clear()
        self.ui.comboBoxFokotany.setEnabled(self.ui.checkBoxFokontany.isChecked())
        #self.ui.comboBoxFokotany.clear()

    def ouvrirConsultDmdCert(self):
        # self.iface.mapCanvas().refresh()

        self.demandes.show()
        result = self.demandes.exec_()


    def ouvrirChoixSurParcelle(self):
        from .ChoixSurParcelleDmdRun import ChoixSurParcelleDmdRun
        self.choix = ChoixSurParcelleDmdRun(self.connection, self.canvas, self)
        if self.choix.creation.getEtatOpposition():
            reply = QMessageBox.critical(self, "Erreur Opposition", u"Il existe encore des oppositions non résolues liées à cette demande")
            if reply == QMessageBox.Ok:
                self.choix.close()
        elif self.choix.creation.isCertificat():
            reply = QMessageBox.critical(self, "Erreur",
                                         u"Cette demande à déjà été transformée en Certificat.")
            if reply == QMessageBox.Ok:
                self.choix.close()
        else:
            nJours =  datetime.date.today() - self.dateDemande
            print nJours.days
            if nJours.days > 15:
                self.choix.show()
                #self.choix.recupnuDemande()
                result = self.choix.exec_()
            else:
                print "erreur"
                reply = QMessageBox.critical(self, "Erreur",
                                             u"La date du jour doit être superieure à la  date de la demande d'au moins 15 jours !")
                if reply == QMessageBox.Ok:
                    self.choix.close()
                #qmessage = QString(u"La date du jour doit être superieure a la de date de la demande d'au moins 15 jours !")
                #self.messageErreur(qmessage)


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
        print "numero page in"
        print numeropage
        limite = 20
        #print numeropage
        offset = limite * (numeropage - 1)
        listeParams.append(globalvars.id_projet)
        listeParams.append(limite)
        listeParams.append(offset)
        params = tuple(listeParams)
        try:
            self.cur.execute("SELECT DISTINCT COUNT(*) FROM parcelle_d pd, demande d WHERE pd.gid = d.gid and pd.idcertificat IS NULL ")
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
        # self.cur.execute("SELECT idcertificat, numerodemande, datereconnaissance FROM certificat")
        SQL = "SELECT DISTINCT pd.gid, d.numdemande, d.datedemande, d.datereconnaissance, pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid and pd.idcertificat IS NULL "
        data = self.pagination(SQL, params)
        #self.cur.execute(
            #"SELECT pd.gid, pd.numdemande, d.datedemande, d.datereconnaissance, pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid AND pd.idcertificat IS NULL ")
        #data = self.cur.fetchall()
        self.showInTable(data)
        print data
        # rint len(data[0])

    def showInTable(self, data):
        self.gids[:] = []
        self.datesDemandes[:] = []
        self.ui.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            self.gids.append(data[i][0])
            self.datesDemandes.append(data[i][2])
            j = 1
            while j < len(data[i]) - 1:
                if data[i][j] is not None:
                    if (j == 2 or j == 3) and data[i][j]:
                        if data[i][j].year > 1900:
                            self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                        else:
                            dateiso = data[i][j].isoformat()
                            tokens = dateiso.strip().split("-")
                            date = "%s/%s/%s" % (tokens[2], tokens[1], tokens[0])
                            #print date
                            self.ui.tableWidget.setItem(rowPosition, j - 1,
                                                        QtGui.QTableWidgetItem(date))
                    else:
                        self.ui.tableWidget.setItem(rowPosition, j - 1, QtGui.QTableWidgetItem(unicode(data[i][j])))
                j = j + 1

            i = i + 1

    def selectionLigne(self, row):
        ID = self.gids[row]
        self.dateDemande = self.datesDemandes[row]
        self.iddemande = ID

        print "selection self.gids[row] in"
        print ID
        print "selection self.gids[row] out"
        self.numDemande = str(self.ui.tableWidget.item(row, 0).text())
        #self.choix.creation.getDemandeNum(numDemande)
        self.geomid = ID
        self.iddemande = ID
        print "test"
        #cLayer = self.canvas.currentLayer()
        cLayer = self.parent.cLayer
        print cLayer
        #cLayer.select(ID)
        #cLayer.setSelectedFeatures([ID])
        #self.cvs.zoomToSelected(cLayer)

        for layer in self.canvas.layers():
            print " in layer loop in "
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()

        self.canvas.refresh()
        self.idparcelle = int(ID)
        #canvas.setSelectionColor(QtGui.QColor(str(globalvars.SelectionColor)))
        cLayer.select(int(ID))
        self.canvas.zoomToSelected(cLayer)


    def reloadCanvas(self):
        print " reload canvas "
        canvas = self.canvas
        for layer in canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()


    def readInput(self):
        data = {}
        data['numdemande'] = unicode(self.ui.lineEditNumDemande.text()).encode('utf-8')
        data['nomdemandeur'] = unicode(self.ui.lineEditNomDemandeur.text()).encode('utf-8')
        if self.ui.checkBoxDu.isChecked():
            data['datedebut'] = datetime.date(self.ui.dateEditDateDemande.date().year(), self.ui.dateEditDateDemande.date().month(), self.ui.dateEditDateDemande.date().day())
            print data['datedebut']
        else:
            data['datedebut'] = ''
        if self.ui.checkBoxAu.isChecked():
            #data['datefin'] = time.strptime(self.ui.dateEditDateDemandeFin.text(), '%d/%m/%Y')
            data['datefin'] = datetime.date(self.ui.dateEditDateDemandeFin.date().year(), self.ui.dateEditDateDemandeFin.date().month(), self.ui.dateEditDateDemandeFin.date().day())
        else:
            data['datefin'] = ''

        data['fokontany'] = unicode(self.ui.comboBoxFokotany.currentText()).encode('utf-8')
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
        listeParamsPagination.append(globalvars.id_projet)
        listeParamsPagination.append(limite)
        listeParamsPagination.append(offset)
        #***fin prepa pagination****#
        flag = 0
        listeParams =[]
        SQL = "SELECT DISTINCT pd.gid, d.numdemande, d.datedemande, d.datereconnaissance, pd.cout, d.nomdemandeur, d.gid FROM parcelle_d pd, demande d WHERE pd.gid = d.gid and pd.idcertificat IS NULL "
        SQL_count = "SELECT DISTINCT COUNT(*) FROM parcelle_d pd, demande d WHERE pd.gid = d.gid and pd.idcertificat IS NULL "
        if self.ui.checkBoxNumDemande.isChecked():
            data['numdemande'] = "%"+data['numdemande']+"%"
            SQL = SQL + "AND d.numdemande LIKE %s "
            SQL_count = SQL_count + "AND d.numdemande LIKE %s "
            listeParams.append(data['numdemande'])
            flag = 1
        if self.ui.checkBoxNomDemandeur.isChecked():
            if flag == 1:
                data['nomdemandeur'] = "%"+data['nomdemandeur']+"%"
                SQL = SQL + "AND d.nomdemandeur = %s "
                SQL_count = SQL_count + "AND d.nomdemandeur = %s "
                listeParams.append(data['nomdemandeur'])
            else:
                data['nomdemandeur'] = "%" + data['nomdemandeur'] + "%"
                SQL = SQL + "AND d.nomdemandeur = %s "
                SQL_count = SQL_count + "AND d.nomdemandeur = %s "
                listeParams.append(data['nomdemandeur'])
                flag = 1
        if self.ui.checkBoxDu.isChecked() and self.ui.checkBoxAu.isChecked():
            if flag == 1:
                SQL = SQL + "and d.datedemande >= %s and d.datedemande <= %s "
                SQL_count = SQL_count + "and d.datedemande >= %s and d.datedemande <= %s "
                listeParams.append(data['datedebut'])
                listeParams.append(data['datefin'])
            else:
                SQL = SQL + "AND d.datedemande >= %s and d.datedemande <= %s "
                SQL_count = SQL_count + "and d.datedemande >= %s and d.datedemande <= %s "
                listeParams.append(data['datedebut'])
                listeParams.append(data['datefin'])
                flag = 1
        elif self.ui.checkBoxDu.isChecked():
            if flag == 1:
                SQL = SQL + "and d.datedemande  >= %s "
                SQL_count = SQL_count + "and d.datedemande  >= %s "
                listeParams.append(data['datedebut'])
            else:
                SQL = SQL + "AND d.datedemande >= %s "
                SQL_count = SQL_count + "AND d.datedemande >= %s "
                listeParams.append(data['datedebut'])
                flag = 1
        elif self.ui.checkBoxAu.isChecked():
            if flag == 1:
                SQL = SQL + "and d.datedemande <= %s "
                SQL_count  = SQL_count + "and d.datedemande <= %s "
                listeParams.append(data['datefin'])
            else:
                SQL = SQL + "AND d.datedemande <= %s "
                SQL_count = SQL_count + "AND d.datedemande <= %s "
                listeParams.append(data['datefin'])
                flag = 1
        elif self.ui.checkBoxFokontany.isChecked():
            if flag == 1:
                SQL = SQL + "and d.fokontany = %s "
                SQL_count = SQL_count + "and d.fokontany = %s "
                listeParams.append(data['fokontany'])
            else:
                SQL = SQL + "AND d.fokontany = %s "
                SQL_count = SQL_count + "AND d.fokontany = %s "
                listeParams.append(data['fokontany'])
                flag = 1

        if flag == 1:
            SQL = SQL + "and pd.idcertificat IS NULL "
            SQL_count = SQL_count + "and pd.idcertificat IS NULL "
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

    def disableAll(self):
        self.ui.dateEditDateDemande.setEnabled(False)
        self.ui.dateEditDateDemandeFin.setEnabled(False)
        self.ui.lineEditNomDemandeur.setEnabled(False)
        self.ui.lineEditNumDemande.setEnabled(False)
        #self.ui.toolButton.setEnabled(False)
        #self.ui.toolButton_2.setEnabled(False)

    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)
        self.ui.lineEditNumDemande.setValidator(validatorAlphaNum)
        self.ui.lineEditNomDemandeur.setValidator(validatorAlpha)


    def fillComboFokontany(self):
        try:
            self.cur.execute("SELECT nomfokontany, idfokontany FROM fokontany WHERE idcommune = %s", (globalvars.id_commune, ))
            fkts = self.cur.fetchall()
            for fkt in fkts:
                self.ui.comboBoxFokotany.addItem(fkt[0], fkt[1])
        except StandardError as e:
            print e


    def certificatReady(self):
        self.choix.creation.close()
        self.choix.close()
        self.showAll()

    #def setCurrentLayer(self, cLayer, cvs):
        #self.currentLayer = cLayer
        #self.cvs = cvs

    def detailsDemande(self):
        print "test "
        print "details demande  AT CF"
        #from Demande.DetailsDemandeRunn import DetailsDemandeRunn
        #demandes = DetailsDemandeRunn(self)
        self.idDemande = self.iddemande
        from Demande.DemandeDetailsRun import DemandeDetailsRun
        demandes = DemandeDetailsRun(self)
        demandes.show()
        result = demandes.exec_()

    def messageErreur(self, message):
        self.isValid = True
        msgBox = QtGui.QMessageBox()
        msgBox.setText(message)
        msgBox.setModal(True)
        msgBox.show()
        msgBox.exec_()

# ****************************** FONCTIONS UTILES A LA PAGINATION ************************************#

    def pagination(self, SQL, params):
        print "Appel pagination"
        SQL = SQL + " AND idprojet = %s LIMIT %s OFFSET %s"
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

    def fermer(self):
        self.close()

    def __del__(self):
        self.cur.close()
