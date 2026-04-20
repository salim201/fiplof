# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
from qgis.core import *
from qgis.gui import *
from .Html2Pdf import Html2Pdf
import datetime, time
import globalvars
import os
import webbrowser
import tempfile
from random import randint
from AreaConvert import AreaConvert
from Utils import Utils
from Certificat.RechercheCFRegistre import Ui_Dialog
from PyPDF2 import PdfFileMerger
from .num_debut_pageRun import NumDebut_PageRun

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class RechercheCFRun(QDialog):
#    def __init__(self, connection, canvas, parent):
    def __init__(self, connection, canvas, parent,slf = None, template = None):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.template = template
        self.canvas = canvas
        self.idparcelle = None
        self.numDemande = ""
        self.idCertificat = None
        self.numCF = None
        self.parent = parent
        self.idsCFtoPrint = []
        self.toutCocher = False
        self.nbr_kt_par_table = 100
        self.cLayer = self.parent.cLayer
        self.activateChangeOngeom = None
        #***Utile pour la pagination****#
        self.isShowAll = False
        self.nombreDePage = None
        self.ui.lineEditNumPage.setText("1")
        #***fin utile pour la paginaion***#
        #self.idDemande = None

        #self.cf.setDisabled(True)
        self.idCertificats = []
        self.gids = []
        self.initActions()
        self.initDB()
        appStyle = """  
                QTableWidget 
                {

        	        alternate-background-color: #87cefa;
             	    background-color: white;
                }
                """
        self.setStyleSheet(appStyle)
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.ui.tableWidget.setSelectionBehavior(1)
        #self.ui.tableWidget.horizontalHeaderItem(0).setSizeHint(QtCore.QSize(10, 10))
        # ilaina am details demande
        self.stateEdition = 0
        self.geomid = 0
        self.tool = parent.tool
        self.iddemande = None
        self.fillFokontany()
        self.senderName = self.sender().objectName()
        self.numDebutPage = 1



        if slf :
            self.slf = slf
            self.slf.comBoCF = self.slf.ui.comboNumCertificat
            print " load OPS"
        else :
            print " not load OPS"

        print self.senderName

        #self.ui.btnFermer.clicked.connect(self.close)

    def initActions(self):
        self.ui.btnDetail.clicked.connect(self.consulterCF)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.btnAfficherTous.clicked.connect(self.showAll)
        self.ui.btnRechercher.clicked.connect(self.readInput)
        self.ui.SelBtn.clicked.connect(self.ChoisirCF)
        self.ui.tableWidget.cellClicked.connect(self.selectionLigne)
        self.ui.checkBoxNumDemande.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxNomDemandeur.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxDateCreation.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxType.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxFokontany.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxEtat.stateChanged.connect(self.updateFieldsStatus)
        self.ui.checkBoxCocherTout.stateChanged.connect(self.updateCheck)
        #***Utiles pour la pagination****#
        self.ui.btnDebut.clicked.connect(self.debut)
        self.ui.btnPrecedent.clicked.connect(self.precedent)
        self.ui.btnSuivant.clicked.connect(self.suivant)
        self.ui.btnFin.clicked.connect(self.fin)
        self.ui.comboBoxNumPage.activated.connect(self.updatePage)
        #*****fin utiles pour pagination*****#
        #Recherche automatique
        #self.ui.lineEditNumCF.textEdited.connect(self.readInput)
        self.ui.lineEditNomProprietaire.textEdited.connect(self.readInput)
        #self.ui.btnImprimer.clicked.connect(self.doPrint)
        self.ui.btnImprimer.clicked.connect(self.getNumPagePage)

    def ChoisirCF(self):
        print "choix CF"
        if self.numCF :
            self.slf.comBoCF.addItem(self.numCF, self.idCertificat)
            self.close()
        else :
            print "None"

    def updateFieldsStatus(self):
        self.ui.lineEditNumCF.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.lineEditNomProprietaire.setEnabled(self.ui.checkBoxNomDemandeur.isChecked())
        self.ui.dateEditCreation.setEnabled(self.ui.checkBoxDateCreation.isChecked())
        self.ui.comboBoxType.setEnabled(self.ui.checkBoxType.isChecked())
        self.ui.comboBoxFokotany.setEnabled(self.ui.checkBoxFokontany.isChecked())
        self.ui.comboBoxEtat.setEnabled(self.ui.checkBoxEtat.isChecked())


    def consulterCF(self):
        if self.senderName == "actionEdition_des_informations":
            from Certificat.EditionCFRun import EditionCFRun
            self.editCF = EditionCFRun(self.connection, self)
            self.editCF.exec_()
        elif self.senderName == "actionEdition_de_la_geometrie":
            self.activateChangeOngeom = self.parent.ui.actionEnregistrer
            from Certificat.EditionCFRun import EditionCFRun
            self.editCF = EditionCFRun(self.connection, self, 1)
            self.editCF.exec_()
        else:
            from Certificat.ConsultationCFRun import ConsultationCFRun
            self.cf = ConsultationCFRun(self.connection, self)
            self.cf.exec_()


    def showAll(self):
        #***prepa pagination****#
        self.ui.comboBoxNumPage.clear()
        self.isShowAll = True
        count = []
        listeParams = []
        numeropage = int(self.ui.lineEditNumPage.text())
        limite = self.nbr_kt_par_table
        #print numeropage
        offset = limite * (numeropage - 1)
        listeParams.append(globalvars.id_projet)
        listeParams.append(limite)
        listeParams.append(offset)
        params = tuple(listeParams)
        try:
            self.cur.execute("SELECT COUNT(*) FROM certificat WHERE idprojet = %s  AND TRIM(SPLIT_PART(numerocertificat,'-','4')) <> ''  AND datereconnaissance is not NULL", (globalvars.id_projet,))
            count = self.cur.fetchone()
        except StandardError as e:
            #self.connection.rollback()
            print(e)
        #***fin prepa paination***#
#*****CALCUL DU NOMBRE TOTAL DE PAGES****************#
        if count[0] <= self.nbr_kt_par_table:
            self.nombreDePage = 1
        else:
            nbrDePage = count[0] / self.nbr_kt_par_table
            reste = count[0] % self.nbr_kt_par_table
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
#******FIN CALCUL DU NOMBRE DE PAGES******************#
        SQL = "SELECT c.idcertificat, c.numerocertificat, c.numerodemande, c.datecreation, c.datereconnaissance, p.cout, p.gid, p.idcertificat , CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) as ordre FROM certificat c, parcelle_d p WHERE c.idcertificat = p.idcertificat AND TRIM(SPLIT_PART(c.numerocertificat,'-','4')) <> '' AND c.datereconnaissance is not NULL"
        data = self.pagination(SQL,params)
        print data

        if data:
            try:
                self.showInTable(data)
                print len(data[0])
            except Exception as err:
                print err

    def showInTable(self, data):
        self.idCertificats[:] = []
        self.gids[:] = []
        self.ui.tableWidget.setRowCount(0)
        i = 0
        if data is not None:
            while i < len(data):
                rowPosition = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowPosition)
                self.idCertificats.append(data[i][0])
                self.gids.append(data[i][6])
                j = 0
                while j < len(data[i]) - 2:
                    if data[i][j] is not None:
                        if j  == 0:
                            item = QtGui.QTableWidgetItem(True)
                            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            if self.toutCocher:
                                item.setCheckState(QtCore.Qt.Checked)
                            else:
                                item.setCheckState(QtCore.Qt.Unchecked)
                            self.ui.tableWidget.setItem(rowPosition, j, item)
                            if self.ui.tableWidget.item(rowPosition, 0).checkState():
                                if data[i][0] not in self.idsCFtoPrint:
                                    self.idsCFtoPrint.append(data[i][0])
                            else:
                                if data[i][0] in self.idsCFtoPrint:
                                    self.idsCFtoPrint.remove(data[i][0])
                            print self.idsCFtoPrint
                        elif (j == 4 or j == 5) and type(data[i][j]) == 'str':
                            self.ui.tableWidget.setItem(rowPosition, j ,
                                                     QtGui.QTableWidgetItem(data[i][j].strftime('%d/%m/%Y')))
                        else:
                            self.ui.tableWidget.setItem(rowPosition, j , QtGui.QTableWidgetItem(unicode(data[i][j])))
                    j = j + 1

                i = i + 1


    def selectionLigne(self, row):
        #print row
        ID = self.gids[row]
        self.numDemande = self.ui.tableWidget.item(row, 1).text()
        print ID
        self.idparcelle = ID
        self.idCertificat = self.idCertificats[row]

        if self.ui.tableWidget.item(row, 0).checkState():
            if self.idCertificat not in self.idsCFtoPrint:
                self.idsCFtoPrint.append(self.idCertificat)
        else:
            if self.idCertificat in self.idsCFtoPrint:
                self.idsCFtoPrint.remove(self.idCertificat)

        print self.idsCFtoPrint

        self.numCF = self.ui.tableWidget.item(row, 0).text()
        print " self.idCertificat in"
        print self.idCertificat
        print self.ui.tableWidget.item(row, 0).text()
        print " self.idCertificat out"
        self.iddemande = ID
        self.idDemande = ID
        self.geomid = ID
        #self.cf.getCFById(self.idCertificats[row])
        canvas = self.canvas
        cLayer = self.parent.cLayer
        #cLayer = self.canvas.currentLayer()

        print cLayer
        # cLayer.select(ID)
        # cLayer.setSelectedFeatures([ID])
        # self.cvs.zoomToSelected(cLayer)

        for layer in self.canvas.layers():
            print " in layer loop in "
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()

        self.canvas.refresh()
        cLayer.select(int(ID))
        self.canvas.zoomToSelected(cLayer)

    def readInput(self):

        data = {}
        data['numcert'] = unicode(self.ui.lineEditNumCF.text()).encode('utf-8')
        data['proprietaire'] = unicode(self.ui.lineEditNomProprietaire.text()).encode('utf-8')
        if self.ui.checkBoxDateCreation.isChecked():
            data['datecreation'] = datetime.date(self.ui.dateEditCreation.date().year(), self.ui.dateEditCreation.date().month(), self.ui.dateEditCreation.date().day())
            print data['datecreation']
        else:
            data['datecreation'] = ''
        data['type'] = unicode(self.ui.comboBoxType.currentText()).encode('utf-8')
        data['fokontany'] = unicode(self.ui.comboBoxFokotany.currentText()).encode('utf-8')
        data['etat'] = unicode(self.ui.comboBoxEtat.currentText()).encode('utf-8')

        self.rechercher(data)


    def prepareNumCF(self, numCFBrut):
        numCFIntermed = numCFBrut.split(',')
        # print numDmdIntermed
        return numCFIntermed

    def rechercher(self, data):
        #**prepa pagination***#
        self.ui.comboBoxNumPage.clear()
        self.isShowAll = False
        numeropage = int(self.ui.lineEditNumPage.text())
        limite = self.nbr_kt_par_table
        count = []
        listeParamsPagination = []
        # print numeropage
        offset = limite * (numeropage - 1)
        listeParamsPagination.append(globalvars.id_projet)
        listeParamsPagination.append(limite)
        listeParamsPagination.append(offset)
        #***fin prepa pagination****#

        flag = 0
        listeParam = [] #modif arv
        listeParams =[]
        listeParams1 = []
        listeParams2 = []
        SQL = ""
        SQL_count = ""
        SQL1 = ""
        SQL2 = ""
        SQL1_count = ""
        SQL2_count = ""
        SQL_select = "SELECT distinct c.idcertificat, c.numerocertificat, c.numerodemande, c.datecreation, c.datereconnaissance, p.cout, p.gid, p.idcertificat, c.idprojet, CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) as ordre "
        SQL_select_count = "SELECT distinct COUNT(c.idcertificat) "
        SQL_from = "FROM certificat c JOIN parcelle_d p on c.idcertificat = p.idcertificat "


        #SQL_where = "WHERE c.idcertificat = p.idcertificat AND TRIM(SPLIT_PART(c.numerocertificat,'-','4')) <> ''"

        print SQL1

        """ RECUPERATION CLAUSE WHERE SI """

        numCFBrut = str(data['numcert']).strip()
        numCFToQuery = self.prepareNumCF(numCFBrut)
        print '----------------------num----------------------------'
        print numCFToQuery
        firstOne = True
        SQL_where = ""
        if numCFBrut != "":
            print numCFToQuery
            for numCF in numCFToQuery:
                print numCF
                try:
                    if numCF.find('-') == -1:
                        if firstOne == True:
                            firstOne = False
                            listeParam.append(numCF)
                            listeParams1.append(numCF)
                            SQL_where = SQL_where + " WHERE CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) = %s"
                        else:
                            listeParam.append(numCF)
                            listeParams1.append(numCF)
                            SQL_where = SQL_where + " OR CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) = %s"
                    else:
                        params = numCF.split('-')
                        num_debut = params[0]
                        num_fin = params[1]
                        listeParam.append(num_debut)
                        listeParams1.append(num_debut)
                        listeParam.append(num_fin)
                        listeParams1.append(num_fin)
                        if firstOne == True:
                            firstOne = False
                            SQL_where = SQL_where + " WHERE CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) BETWEEN %s AND %s"
                        else:
                            SQL_where = SQL_where + " OR CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) BETWEEN %s AND %s"
                except StandardError as e:
                    print '----------------------diso---------------------------'
                    print e

        if self.ui.checkBoxNumDemande.isChecked():
            print '----------------------SQL1----------------------------'
            SQL1 = SQL_select + SQL_from + SQL_where
            print SQL1
            SQL1_count = SQL_select_count + SQL_from + SQL_where
            print '----------------------SQL1_count----------------------------'
            print SQL1_count
            flag = 1
        print '----------------------TAFIDITRA----------------------------'


        """
        if self.ui.checkBoxNumDemande.isChecked():#certificat
            data['numcert'] = "%"+data['numcert'].lower()+"%"
            SQL_where = SQL_where + "AND LOWER(c.numerocertificat) LIKE %s "
            SQL1 = SQL_select + SQL_from + SQL_where
            SQL1_count = SQL_select_count + SQL_from + SQL_where
            listeParams1.append(data['numcert'])
            flag = 1

        """

        if self.ui.checkBoxNomDemandeur.isChecked():
            data['proprietaire'] = "%" + data['proprietaire'].lower() + "%"
            if flag == 1:
                SQL1 = ""
                SQL1_count = ""
                listeParams1.append(data['proprietaire'])
                listeParams1.append(data['proprietaire'])
                listeParams2.append(data['numcert'])
                listeParams2.append(data['proprietaire'])
            else:
                listeParams1.append(data['proprietaire'])
                listeParams1.append(data['proprietaire'])
                listeParams2.append(data['proprietaire'])
                flag = 1

            SQL_from1 = SQL_from + ", (select distinct pp.nompersonne, pp.prenompersonne, pdk.gid  FROM personne pp, proprietaireparcelle ppd, parcelle_d pdk" \
                                  "  WHERE pp.idpersonne = ppd.idpersonne AND pdk.gid = ppd.idparcelle) proprietairephysique "
            SQL_where1 = SQL_where + " and proprietairephysique.gid = p.gid " + " AND (LOWER(proprietairephysique.nompersonne) LIKE %s OR LOWER(proprietairephysique.prenompersonne) LIKE %s) "
            SQL_from2 = SQL_from + ", (select distinct pm.denomination, pdl.gid FROM personnemorale pm, personnemoraleparcelle_d pmd, parcelle_d pdl  " \
                                   "WHERE pm.idpersonnemorale = pmd.idpersonne AND pdl.gid = pmd.idparcelle) proprietairemorale "
            SQL_where2 = SQL_where + " and proprietairemorale.gid = p.gid " + " AND (LOWER(proprietairemorale.denomination) LIKE %s) "
            SQL1 = SQL_select + SQL_from1 + SQL_where1
            SQL1_count = SQL_select_count + SQL_from1 + SQL_where1
            SQL2 = SQL_select + SQL_from2 + SQL_where2
            SQL2_count = SQL_select_count + SQL_from2 + SQL_where2

        if self.ui.checkBoxDateCreation.isChecked():
            if data['datecreation'] != "":
                if len(SQL2) == 0:
                    if flag == 1:
                        SQL1 = SQL1 + " AND c.datecreation > %s "
                        SQL1_count = SQL1_count + " AND c.datecreation > %s "
                        listeParams1.append(data['datecreation'])
                    else:
                        SQL1 = SQL_select + SQL_from + SQL_where
                        SQL1 = SQL1 + " AND c.datecreation > %s "
                        SQL1_count = SQL_select_count + SQL_from + SQL_where
                        SQL1_count = SQL1_count + " AND c.datecreation > %s "
                        listeParams1.append(data['datecreation'])
                        flag = 1
                else:
                    SQL1 = SQL1 + " AND c.datecreation > %s "
                    SQL1_count = SQL1_count + " AND c.datecreation > %s "
                    listeParams1.append(data['datecreation'])
                    SQL2 = SQL2 + " AND c.datecreation > %s "
                    SQL2_count = SQL2_count + " AND c.datecreation > %s "
                    listeParams2.append(data['datecreation'])

        if self.ui.checkBoxType.isChecked():
            data['type'] = "%" + data['type'].lower() + "%"
            if len(SQL2) == 0:
                if flag == 1:
                    SQL1 = SQL1 + " AND LOWER(c.typecertificat) LIKE %s "
                    SQL1_count = SQL1_count +  " AND LOWER(c.typecertificat) LIKE %s "
                    listeParams1.append(data['type'])
                else:
                    SQL1 = SQL_select + SQL_from + SQL_where
                    SQL1 = SQL1 + " AND LOWER(c.typecertificat) LIKE %s "
                    SQL1_count = SQL_select_count + SQL_from + SQL_where
                    SQL1_count = SQL1_count + " AND LOWER(c.typecertificat) LIKE %s "
                    listeParams1.append(data['type'])
                    flag = 1
            else:
                SQL1 = SQL1 + " AND LOWER(c.typecertificat) LIKE %s "
                SQL1_count = SQL1_count + " AND LOWER(c.typecertificat) LIKE %s "
                listeParams1.append(data['type'])
                SQL2 = SQL2 + " AND LOWER(c.typecertificat) LIKE %s "
                SQL2_count = SQL2_count + " AND LOWER(c.typecertificat) LIKE %s "
                listeParams2.append(data['type'])

        if flag == 1:
            if SQL2 != "":
                SQL = "SELECT * FROM (" + SQL1 + " UNION " + SQL2 + ") AS allcertificat"
                SQL_count = "SELECT COUNT(*) FROM " + SQL1 + " UNION " + SQL2 + ") AS allcertificat WHERE idprojet = %s"
                param3 = []
                param3.append(globalvars.id_projet)
                #SQL_count = SQL1_count + " UNION " + SQL2_count
                listeParamsCount = listeParams1 + listeParams2 + param3
                listeParams = listeParams1 + listeParams2 + listeParamsPagination
            else:
                SQL = "SELECT * FROM (" + SQL1 + ") AS allcertificat "
                SQL_count = "SELECT COUNT(*) FROM (" + SQL1 + ") AS allcertificat WHERE idprojet = %s"
                param3 = []
                param3.append(globalvars.id_projet)
                listeParamsCount = listeParams1 + param3
                listeParams = listeParams1 + listeParamsPagination
            print listeParams
            #SQL = SQL + "and pd.idcertificat IS NULL"
            print SQL
            print SQL_count
            params = tuple(listeParams)
            paramsCount = tuple(listeParamsCount)
            count1 = []
            count2 = []

            if SQL2 != "":
                try:
                    self.cur.execute(SQL1_count, listeParams1)
                    count1 = self.cur.fetchone()
                except StandardError as e:
                    print e
                try:
                    self.cur.execute(SQL2_count, listeParams2)
                    count2 = self.cur.fetchone()
                except StandardError as e:
                    print e
                count.append(count1[0] + count2[0])
                print count[0]

            else:
                self.cur.execute(SQL_count, paramsCount)
                count = self.cur.fetchone()

            print count
            # *****CALCUL DU NOMBRE TOTAL DE PAGES****************#
            if count[0] <= self.nbr_kt_par_table:
                self.nombreDePage = 1
            else:
                nbrDePage = count[0] / self.nbr_kt_par_table
                reste = count[0] % self.nbr_kt_par_table
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

            results = self.pagination(SQL, params)
            #try:
                #self.cur.execute(SQL, params)
                #results = self.cur.fetchall()
                #print results
            self.showInTable(results)
            #except StandardError as e:
                #print e
        else:
            print "Aucun critere de recherche selectionne"
            self.ui.tableWidget.setRowCount(0)



    def fillFokontany(self):
        # Fokontany
        try:
            self.cur.execute("SELECT nomfokontany, idfokontany FROM fokontany WHERE idcommune = %s",(globalvars.id_commune, ) )
            fkts = self.cur.fetchall()
            for fkt in fkts:
                self.ui.comboBoxFokotany.addItem(fkt[0], fkt[1])
        except StandardError as e:
            print e
# ****************************** FONCTIONS UTILES A LA PAGINATION ************************************#
    def pagination(self, SQL, params):
        print "Appel pagination"
        if self.isShowAll:
            SQL = SQL + " AND idprojet = %s ORDER BY ordre ASC LIMIT %s OFFSET %s"
        else:
            SQL = SQL + " WHERE idprojet = %s ORDER BY ordre ASC LIMIT %s OFFSET %s"
        print SQL
        try:
            self.cur.execute(SQL, params)
            data = self.cur.fetchall()
            #print data
            return data
        except StandardError as e:
            print e
            self.connection.rollback()

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

    def updateCheck(self):
        rowCount = self.ui.tableWidget.rowCount()
        i = 0
        if self.ui.checkBoxCocherTout.isChecked():
            self.toutCocher = True
            while i < rowCount:
                item = QtGui.QTableWidgetItem(True)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Checked)
                self.ui.tableWidget.setItem(i, 0, item)
                if self.ui.tableWidget.item(i, 0).checkState():
                    if self.idCertificats[i] not in self.idsCFtoPrint:
                        self.idsCFtoPrint.append(self.idCertificats[i])
                i = i + 1
        else:
            self.toutCocher = False
            while i < rowCount:
                item = QtGui.QTableWidgetItem(True)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.ui.tableWidget.setItem(i, 0, item)
                if self.idCertificats[i] in self.idsCFtoPrint:
                    self.idsCFtoPrint.remove(self.idCertificats[i])
                i = i + 1
        print self.idsCFtoPrint

    def getNumPagePage(self):
        self.numDebutPage = 0
        try:
            num_page = NumDebut_PageRun(self)
            num_page.exec_()
        except Exception as err:
            print(err)


    def doPrint(self):
        self.merger = PdfFileMerger()
        infosCF = []
        dic = None
        from Projet.journalRunn import journal
        journal = journal(self.connection)
        journal.inserToJournal(globalvars.id_user, 0, u"Certificat",
                               u"Impression de Registre Parcellaire")
        if self.numDebutPage != 0:
            num_page = self.numDebutPage
        else:
            num_page = 1
        for idCFtoPrint in self.idsCFtoPrint:
            proprio = []
            aire = None
            emplacementParcelle = {}
            limitesparcelle = {}
            limitesparcelle['nord'] = ""
            limitesparcelle['sud'] = ""
            limitesparcelle['est'] = ""
            limitesparcelle['ouest'] = ""
            emplacementParcelle['hameau'] = ""
            emplacementParcelle['fokontany'] = ""
            emplacementParcelle['commune'] = ""
            limitesparcelle['nord'] = ""
            limitesparcelle['sud'] = ""
            limitesparcelle['est'] = ""
            limitesparcelle['ouest'] = ""
            charge = ""

            try:
                self.cur.execute("SELECT c.numerocertificat, c.numerodemande, dmd.datedemande, pd.gid, ST_Area(pd.geom), pd.idhameau, c.idfokontany, dmd.datereconnaissance FROM certificat c, parcelle_d pd, demande dmd WHERE c.idcertificat = pd.idcertificat AND pd.gid = dmd.gid AND c.idcertificat = %s", (idCFtoPrint,))
                infosCF = self.cur.fetchone()
                print "Information CF " + str(infosCF)
                if infosCF is not None:
                    idparcelle = int(infosCF[3])
                    ### Traitement des proprietaires du certificat ###
                    try:
                        self.cur.execute("SELECT nompersonne, prenompersonne,"
                                         " datenaissancepersonne, lieunaissancepersonne, "
                                         " sexepersonne, adressepersonne, numcipersonne, "
                                         " datecipersonne, lieucipersonne, numactenaissancepersonne, "
                                         " dateactenaissancepersonne, lieuactenaissancepersonne, "
                                         " situationmatrimoniale, nompere, nommere, nevers, COALESCE(ppd.representant, FALSE) as ordre "
                                         "FROM personne ppq, proprietaireparcelle ppd "
                                         "WHERE ppq.idpersonne = ppd.idpersonne AND ppd.idparcelle = %s ORDER BY ordre DESC", (idparcelle,))
                        dataProprio = self.cur.fetchall()
                        print "Proprietaires  = " + str(dataProprio)
                        if dataProprio is not None:
                            i = 1
                            k = 0

                            proprio [:] = []
                            while (k < len(dataProprio)):
                                infoProprio = {}
                                print "DATA PROPRIO **************************************************************************µ"
                                print dataProprio[k]
                                infoProprio['numero'] = str(i)
                                i = i + 1
                                if dataProprio[k][0] is not None or dataProprio[k][1] is not None:
                                    infoProprio['nomprenom'] = self.takeCareOfAccent(unicode(dataProprio[k][0]).encode('utf-8').strip() + " " + unicode(dataProprio[k][1]).encode('utf-8').strip())
                                else:
                                    infoProprio['nomprenom'] = "&nbsp;"
                                if dataProprio[k][15] is not None:
                                    infoProprio['datenaiss'] = str(dataProprio[k][15])
                                elif dataProprio[k][2] is not None:
                                    infoProprio['datenaiss'] = dataProprio[k][2].strftime('%d/%m/%Y')
                                else:
                                    infoProprio['datenaiss'] = "&nbsp;"
                                if dataProprio[k][3] is not None:
                                    infoProprio['lieunaiss'] = self.takeCareOfAccent(unicode(dataProprio[k][3]).encode('utf-8').strip())
                                else:
                                    infoProprio['lieunaiss'] = "&nbsp;"
                                if dataProprio[k][5] is not None:
                                    infoProprio['adresse'] = self.takeCareOfAccent(unicode(dataProprio[k][5]).encode('utf-8').strip())
                                else:
                                    infoProprio['adresse'] = "&nbsp;"
                                if dataProprio[k][6] is not None:
                                    infoProprio['numpiece'] = unicode(dataProprio[k][6])[0:3].strip() + "-" + unicode(dataProprio[k][6])[3:6].strip() + "-" + unicode(dataProprio[k][6])[6:9].strip() + "-" + unicode(dataProprio[k][6])[9:].strip()
                                    if dataProprio[k][8] is not None:
                                        infoProprio['lieupiece'] = self.takeCareOfAccent(unicode(dataProprio[k][8]).encode('utf-8').strip())
                                    else:
                                        infoProprio['lieupiece'] = "&nbsp;"
                                    if dataProprio[k][7] is not None:
                                        infoProprio['datepiece'] = dataProprio[k][7].strftime('%d/%m/%Y')
                                    else:
                                        infoProprio['datepiece'] = "&nbsp;"
                                elif dataProprio[k][9] is not None:
                                    infoProprio['numpiece'] = unicode(dataProprio[k][9]).strip()
                                    if dataProprio[11] is not None:
                                        infoProprio['lieupiece'] = self.takeCareOfAccent(unicode(dataProprio[k][11]).encode('utf-8').strip())
                                    else:
                                        infoProprio['lieupiece'] = "&nbsp;"
                                    if dataProprio[k][10] is not None:
                                        infoProprio['datepiece'] = dataProprio[k][10].strftime('%d/%m/%Y')
                                    else:
                                        infoProprio['datepiece'] = "&nbsp;"
                                else:
                                    infoProprio['numpiece'] = "&nbsp;"
                                    infoProprio['lieupiece'] = "&nbsp;"
                                if dataProprio[k][12] is not None:
                                    if dataProprio[k][12] == 1:
                                        infoProprio['matrimoniale'] = str("Tsy manambady")
                                    elif dataProprio[k][12] == 2:
                                        infoProprio['matrimoniale'] = str("Manambady")
                                    elif dataProprio[k][12] == 3:
                                        infoProprio['matrimoniale'] = str("Maty vady")
                                    else:
                                        infoProprio['matrimoniale'] = str("Tsy manambady")
                                else:
                                    infoProprio['matrimoniale'] = "Tsy manambady"
                                if dataProprio[k][13] is not None:
                                    infoProprio['nompere'] = self.takeCareOfAccent(unicode(dataProprio[k][13]).encode('utf-8').strip())
                                    #print "Nom Pere = " + infoProprio['nompere']
                                else:
                                    infoProprio['nompere'] = "&nbsp;"
                                if dataProprio[k][14] is not None:
                                    infoProprio['nommere'] = self.takeCareOfAccent(unicode(dataProprio[k][14]).encode('utf-8').strip())
                                else:
                                    infoProprio['nommere'] = "&nbsp;"

                                #proprio.append(infoProprio)
                                proprio.insert(k, infoProprio)
                                '''
                                proprio.append({
                                    "numero":infoProprio['num'],
                                    "nomprenom":infoProprio['nom'],
                                    "numpiece":infoProprio['numpiece'],
                                    "datepiece": infoProprio['datepiece'],
                                    "lieupiece":infoProprio['lieupiece'],
                                    "datenaiss":infoProprio['datenaissance'],
                                    "lieunaiss":infoProprio['lieunaissance'],
                                    "nompere":infoProprio['nompere'],
                                    "nommere":infoProprio['nommere'],
                                    "matrimoniale":infoProprio['matrimoniale'],
                                    "adresse":infoProprio['adresse']
                                })
                                '''
                                k = k + 1

                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ###Fin traitement proprietaire###
                    ###Traitement momban'ny tany###
                    if infosCF[4] is not None:
                        ac = AreaConvert()
                        aire = ac.convertArea(infosCF[4])
                        print aire
                    if infosCF[5] is not None: # raha misy hameau
                        try:
                            self.cur.execute(
                                "SELECT h.nomhameau, f.nomfokontany, c.nomcommune FROM hameau h, fokontany f, commune c, parcelle_d pd "
                                "WHERE h.idfokontany = f.idfokontany "
                                "AND f.idcommune = c.idcommune "
                                "AND pd.idhameau = h.idhameau "
                                "AND pd.gid = %s", (idparcelle,))
                            results = self.cur.fetchone()
                            if results is not None:
                                emplacementParcelle['hameau'] = self.takeCareOfAccent(unicode(results[0]).encode('utf-8').strip())
                                emplacementParcelle['fokontany'] = self.takeCareOfAccent(unicode(results[1]).encode('utf-8').strip())
                                emplacementParcelle['commune'] = self.takeCareOfAccent(unicode(results[2]).encode('utf-8').strip())
                        except StandardError as e:
                            print(e)
                            self.connection.rollback()
                    elif infosCF[6] is not None:  # raha tsy misy hameau
                        try:
                            self.cur.execute(
                                "SELECT f.nomfokontany, c.nomcommune FROM fokontany f, commune c, certificat cert "
                                    "WHERE f.idcommune = c.idcommune "
                                    "AND f.idfokontany = cert.idfokontany "
                                    "AND cert.idfokontany = %s", (int(infosCF[6]),))
                            results = self.cur.fetchone()
                            if results is not None:
                                emplacementParcelle['hameau'] = ""
                                emplacementParcelle['fokontany'] = self.takeCareOfAccent(unicode(results[0]).encode('utf-8').strip())
                                emplacementParcelle['commune'] = self.takeCareOfAccent(unicode(results[1]).encode('utf-8').strip())
                        except StandardError as e:
                            print(e)
                            self.connection.rollback()
                    else:
                        emplacementParcelle['hameau'] = ""
                        emplacementParcelle['fokontany'] = ""
                        emplacementParcelle['commune'] = ""
                    ###Limites de la parcelle ###
                    try:
                        self.cur.execute("SELECT LOWER(pc.position), lm.description "
                                         "FROM pointscardinaux pc, limitesparcelle lm, parcelle_d pd "
                                         "WHERE lm.idparcelle = pd.gid "
                                         "AND pc.idpointscardinaux = lm.idpointscardinaux "
                                         "AND lm.idparcelle = %s",(idparcelle,))
                        results = self.cur.fetchall()
                        #print results
                        if results is not None:
                            for res in results:
                                if str(res[0]).strip() == "nord":
                                    print "Mandalo ato"
                                    if res[1] is not None:
                                        limitesparcelle['nord'] = self.takeCareOfAccent(unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['nord'] = ""
                                elif str(res[0]).strip() == "sud":
                                    if res[1] is not None:
                                        limitesparcelle['sud'] = self.takeCareOfAccent(unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['sud'] = ""
                                elif str(res[0]).strip() == "est":
                                    if res[1] is not None:
                                        limitesparcelle['est'] = self.takeCareOfAccent(unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['est'] = ""
                                elif str(res[0]).strip() == "ouest":
                                    if res[1] is not None:
                                        limitesparcelle['ouest'] = self.takeCareOfAccent(unicode(res[1]).encode('utf-8').strip())
                                    else:
                                        limitesparcelle['ouest'] = ""
                            print limitesparcelle
                        else:
                            limitesparcelle['nord'] = ""
                            limitesparcelle['sud'] = ""
                            limitesparcelle['est'] = ""
                            limitesparcelle['ouest'] = ""

                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ###Charges de la parcelle###
                    ##Autre charges
                    try:
                        self.cur.execute("SELECT ac.descriptioncharge, ac.dateinscriptionregistre "
                                         "FROM autrecharge ac, autrechargesparcelle_d acp "
                                         "WHERE ac.idcharge = acp.idcharge "
                                         "AND acp.idparcelle = %s", (idparcelle,))
                        autreCharge = self.cur.fetchall()
                        for chg in autreCharge:
                            print chg[0]
                            charge = charge + "Vesatra " + unicode(chg[0]).encode('utf-8').strip() + " tamin'ny " + chg[1].strftime('%d/%m/%Y') + "<br/>"
                        #print autreCharge
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ##Hypotheque
                    try:
                        self.cur.execute("SELECT h.descriptionhypotheque, h.valeur, "
                                         "h.creancier, h.dateinscriptionregistre, "
                                         "h.dateradiation "
                                         "FROM hypotheque h, hypothequeparcelle_d hp "
                                         "WHERE h.idhypotheque = hp.idhypotheque "
                                         "AND hp.idparcelle = %s", (idparcelle,))
                        hypotheque = self.cur.fetchall()
                        for hyp in hypotheque:
                            charge = charge + "Hypotheque " + unicode(hyp[0]).encode('utf-8').strip() + " mitentina " + str(hyp[1]).strip() + " ao amin'ny " + unicode(hyp[2]).encode('utf-8').strip() + " tamin'ny " + hyp[3].strftime('%d/%m/%Y') + "<br/>"
                        #print hypotheque
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()
                    ##Servitude
                    try:
                        self.cur.execute("SELECT s.descriptionservitude, s.dateinscription, "
                                         "s.datelevee, s.origine "
                                         "FROM servitude s, servitudeparcelle_d sp "
                                         "WHERE s.idservitude = sp.idservitude "
                                         "AND sp.idparcelle = %s", (idparcelle,))
                        servitude = self.cur.fetchall()
                        for ser in servitude:
                            charge = charge + "Hypotheque " + str(ser[0]).encode('utf-8').strip() + " tamin'ny " + ser[1].strftime('%d/%m/%Y') + "<br/>"

                        #print servitude
                    except StandardError as e:
                        print(e)
                        self.connection.rollback()

            except StandardError as e:
                print(e)
                self.connection.rollback()
            print charge
            numDmde = ""
            numCF = ""
            dateDmde = ""
            dateRL=""
            AireHa = str(0)
            AireCa = str(0)
            AireA = str(0)
            #print infosCF
            if infosCF != None :
                numDmde = str(infosCF[1]).strip()
                numCF = str(infosCF[0]).strip()
                dateDmde = infosCF[2].strftime('%d/%m/%Y')
                dateRL = infosCF[7].strftime('%d/%m/%Y')
            if aire != None:
                AireHa = str(aire['Ha']).strip()
                AireCa = str(aire['Ca']).strip()
                AireA = str(aire['a']).strip()

            print "CONTENUS DE PROPRIO *****************************************************µ"
            print proprio

            dic = {
                "$numCF": numCF,
                "$numDmde": numDmde,
                "$dateDmde":dateDmde,
                "$dateRL": dateRL,
                "$proprios": proprio,
                "$aireHa": AireHa,
                "$aireA": AireA,
                "$aireCa": AireCa,
                "$hameau": emplacementParcelle['hameau'],
                "$fokontany": emplacementParcelle['fokontany'],
                "$commune": emplacementParcelle['commune'],
                "$nord": limitesparcelle['nord'],
                "$sud": limitesparcelle['sud'],
                "$est": limitesparcelle['est'],
                "$ouest": limitesparcelle['ouest'],
                "$charge": charge,
                "$num_page":str(num_page)
            }
            print infosCF
            print dic
            converter = Html2Pdf()
            print "After Html2Pdf"
            converter.setOrientation(orientation="Landscape")
            converter.setMarginLeft(margin=20)
            src = os.path.dirname(__file__) + "/" + self.template
            print src
            dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
            QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
            converter.generate(html=src, pdf=dst, dictionnary=dic)
            #webbrowser.open(dst)
            self.merger.append(dst)
            num_page = (num_page % 200) + 1
            try:
                converter2 = Html2Pdf()
                print "After Html2Pdf"
                dic2 = {
                    "$numPage": str(num_page)
                }
                converter2.setOrientation(orientation="Landscape")
                converter2.setMarginLeft(margin=5)
                converter2.setMarginRight(margin=20)
                src2 = os.path.dirname(__file__) + "/" + "PageOpsubsequente.html"
                print src2
                dst2 = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
                converter2.generate(html=src2, pdf=dst2, dictionnary=dic2)
                #webbrowser.open(dst)
                self.merger.append(dst2)
            except Exception as err:
                print err
            QApplication.restoreOverrideCursor()
            num_page = (num_page % 200) + 1
        dstFinal = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "Registre.pdf")
        self.merger.write(dstFinal)
        webbrowser.open(dstFinal)

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()

    def takeCareOfAccent(self, chaine):
        if chaine.__contains__(unicode(u"è").encode('utf-8')):
            try:
                return chaine.replace(unicode(u"è").encode('utf-8'),unicode("&egrave;").encode('utf-8'))
            except StandardError as e:
                print e
                pass
        if chaine.__contains__(unicode(u"é").encode('utf-8')):
            try:
                return chaine.replace(unicode(u"é").encode('utf-8'), unicode("&eacute;").encode('utf-8'))
            except StandardError as e:
                print e
                pass
        if chaine.__contains__(unicode(u"ê").encode('utf-8')):
            try:
                return chaine.replace(unicode(u"ê").encode('utf-8'), unicode("&ecirc;").encode('utf-8'))
            except StandardError as e:
                print e
                pass
        if chaine.__contains__(unicode(u"ë").encode('utf-8')):
            try:
                return chaine.replace(unicode(u"ë").encode('utf-8'), unicode("&euml;").encode('utf-8'))
            except StandardError as e:
                print e
                pass
        if chaine.__contains__(unicode(u"ç").encode('utf-8')):
            try:
                return chaine.replace(unicode(u"ç").encode('utf-8'), unicode("&ccedil;").encode('utf-8'))
            except StandardError as e:
                print e
                pass
        if chaine.__contains__(unicode(u"ç").encode('utf-8')):
            try:
                return chaine.replace(unicode(u"ç").encode('utf-8'), unicode("&ccedil;").encode('utf-8'))
            except StandardError as e:
                print e
                pass
                        #print "New chiane = " + chaine
        return chaine

