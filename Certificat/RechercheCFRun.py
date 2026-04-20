# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
from Widgets.ReadonlyTable import ReadonlyTable
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars

from .RechercheCF import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class RechercheCFRun(QDialog):
#    def __init__(self, connection, canvas, parent):
    def __init__(self, connection, canvas, parent,slf = None):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        appStyle = """  
                QTableWidget 
                {

        	        alternate-background-color: #00bfff;
             	    background-color: white;
                }
                """
        self.setStyleSheet(appStyle)
        self.ui.tableWidget.setAlternatingRowColors(True)
        self.canvas = canvas
        self.idparcelle = None
        self.numDemande = ""
        self.idCertificat = None
        self.numCF = None
        self.parent = parent
        self.cLayer = self.parent.cLayer
        self.registry = parent.registry
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
        self.ui.tableWidget.setSelectionBehavior(1)
        # ilaina am details demande
        self.stateEdition = 0
        self.geomid = 0
        self.tool = parent.tool
        self.iddemande = None
        self.fillFokontany()
        self.senderName = self.sender().objectName()


        if slf :
            self.slf = slf
            self.slf.comBoCF = self.slf.ui.comboNumCertificat
            print " load OPS"
        else :
            print " not load OPS"
            self.ui.SelBtn.hide()

        print self.senderName

        #self.ui.btnFermer.clicked.connect(self.close)

    def initActions(self):
        self.ui.btnDetail.clicked.connect(self.consulterCF)
        self.ui.tableWidget.cellDoubleClicked.connect(self.consulterCF)
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
        #***Utiles pour la pagination****#
        self.ui.btnDebut.clicked.connect(self.debut)
        self.ui.btnPrecedent.clicked.connect(self.precedent)
        self.ui.btnSuivant.clicked.connect(self.suivant)
        self.ui.btnFin.clicked.connect(self.fin)
        self.ui.comboBoxNumPage.currentIndexChanged.connect(self.preUpdatePage)
        self.ui.comboBoxNumPage.activated.connect(self.updatePage)
        #*****fin utiles pour pagination*****#
        #Recherche automatique
        self.ui.lineEditNumCF.textEdited.connect(self.readInput)
        self.ui.lineEditNomProprietaire.textEdited.connect(self.readInput)
        self.ui.dateEditCreation.dateChanged.connect(self.readInput)
        self.ui.comboBoxType.currentIndexChanged.connect(self.readInput)
        self.ui.comboBoxFokotany.currentIndexChanged.connect(self.readInput)

    def ChoisirCF(self):
        print "choix CF"

        try:
            if self.numCF:
                self.slf.comBoCF.addItem(self.numCF, self.idCertificat)
                self.close()
            else:
                print
                "None"
        except StandardError as e:
            # self.connection.rollback()
            print(e)
        self.close()

    def updateFieldsStatus(self):
        self.ui.lineEditNumCF.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.lineEditNomProprietaire.setEnabled(self.ui.checkBoxNomDemandeur.isChecked())
        self.ui.dateEditCreation.setEnabled(self.ui.checkBoxDateCreation.isChecked())
        self.ui.comboBoxType.setEnabled(self.ui.checkBoxType.isChecked())
        self.ui.comboBoxFokotany.setEnabled(self.ui.checkBoxFokontany.isChecked())
        self.ui.comboBoxEtat.setEnabled(self.ui.checkBoxEtat.isChecked())


    def consulterCF(self):
        if self.senderName == "actionEdition_des_informations":
            from .EditionCFRun import EditionCFRun
            self.editCF = EditionCFRun(self.connection, self)
            self.editCF.exec_()
        elif self.senderName == "actionEdition_de_la_geometrie":
            self.activateChangeOngeom = self.parent.ui.actionEnregistrer
            from .EditionCFRun import EditionCFRun
            self.editCF = EditionCFRun(self.connection, self, 1)
            self.editCF.exec_()
        else:
            from .ConsultationCFRun import ConsultationCFRun
            self.cf = ConsultationCFRun(self.connection, self)
            self.cf.exec_()

    def preUpdatePage(self):
        if self.ui.comboBoxNumPage.currentIndex() != -1:
            text = str(self.ui.comboBoxNumPage.currentText()).split("/")
            NumPage = int(text[0])
            self.ui.lineEditNumPage.setText(str(NumPage))


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
        listeParams.append(globalvars.id_projet)
        listeParams.append(globalvars.id_commune)
        listeParams.append(limite)
        listeParams.append(offset)
        params = tuple(listeParams)
        try:
            self.cur.execute("SELECT COUNT(*) FROM certificat WHERE idprojet = %s  AND idcommune = %s ", (globalvars.id_projet,globalvars.id_commune,))
            count = self.cur.fetchone()
            print count[0]
        except StandardError as e:
            self.connection.rollback()
            print(e)
        #***fin prepa paination***#
#*****CALCUL DU NOMBRE TOTAL DE PAGES****************#
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
#******FIN CALCUL DU NOMBRE DE PAGES******************#

        SQL = "SELECT c.idcertificat, c.numerocertificat, c.numerodemande, c.datecreation, " \
              "c.datereconnaissance, p.cout, p.gid, p.idcertificat, CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) as ordre,p.estfiscalite FROM certificat c, parcelle_d p " \
              "WHERE c.idcertificat = p.idcertificat"
        data = self.pagination(SQL,params)
        print data

        if data :
            self.showInTable(data,True)
            print len(data[0])

    def showInTable(self, data,cf=False):
        vtlayer = self.registry.mapLayersByName("Certificats")[0]
        self.canvas.setCurrentLayer(vtlayer)
        self.idCertificats = map(lambda row: row[0], data)
        self.gids = map(lambda row: row[6], data)
        readonlyTable = ReadonlyTable(self.ui.tableWidget, self.getCellValue)
        readonlyTable.fillWithData(data,cf)

    def getCellValue(self, data, rowIndex, columnIndex):
        columnIndex = columnIndex + 1
        if columnIndex >= 6:
            return ""
        content = data[rowIndex][columnIndex]
        if (columnIndex == 3 or columnIndex == 4):
            if content is not None:
                return content.strftime('%d/%m/%Y')
            else:
                return ""
        return unicode(content)

    def selectionLigne(self, row):
        #print row
        vtlayer = self.registry.mapLayersByName("Certificats")[0]
        self.canvas.setCurrentLayer(vtlayer)
        ID = self.gids[row]
        self.numDemande = self.ui.tableWidget.item(row, 1).text()
        print ID
        self.idparcelle = ID
        self.idCertificat = self.idCertificats[row]
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
        #cLayer = self.parent.cLayer
        #cLayer = self.canvas.currentLayer()
        cLayer = vtlayer

        print cLayer
        # cLayer.select(ID)
        # cLayer.setSelectedFeatures([ID])
        # self.cvs.zoomToSelected(cLayer)

        for layer in self.canvas.layers():
            print " in layer loop in "
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()

        self.canvas.refresh()
        print "idCF selected" + str(ID)
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

    def rechercher(self, data):
        #**prepa pagination***#
        self.ui.comboBoxNumPage.clear()
        self.isShowAll = False
        numeropage = int(self.ui.lineEditNumPage.text())
        limite = 20
        count = []
        listeParamsPagination = []
        # print numeropage
        offset = limite * (numeropage - 1)
        listeParamsPagination.append(globalvars.id_projet)
        listeParamsPagination.append(globalvars.id_commune)

        listeParamsPagination.append(limite)
        listeParamsPagination.append(offset)
        #***fin prepa pagination****#

        flag = 0
        listeParams =[]
        listeParams1 = []
        listeParams2 = []
        SQL = ""
        SQL_count = ""
        SQL1 = ""
        SQL2 = ""
        SQL1_count = ""
        SQL2_count = ""
        SQL_select_no_order = "SELECT distinct c.idcertificat, c.numerocertificat, c.numerodemande, c.datecreation, c.datereconnaissance, p.cout, p.gid, p.idcertificat, c.idprojet, c.idcommune,c.idcertificat as ordre "
        SQL_select = "SELECT distinct c.idcertificat, c.numerocertificat, c.numerodemande, c.datecreation, c.datereconnaissance, p.cout, p.gid, p.idcertificat, c.idprojet, c.idcommune,CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer) as ordre "
        SQL_select_count = "SELECT distinct COUNT(c.idcertificat) "
        SQL_from = "FROM certificat c, parcelle_d p "
        SQL_where = "WHERE c.idcertificat = p.idcertificat "
        if self.ui.checkBoxNumDemande.isChecked():
            data['numcert'] = "%"+data['numcert'].upper()+"%"
            SQL_where = SQL_where + "AND UPPER(c.numerocertificat) LIKE %s "
            SQL1 = SQL_select + SQL_from + SQL_where
            SQL1_count = SQL_select_count + SQL_from + SQL_where
            listeParams1.append(data['numcert'])
            flag = 1
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
                SQL_count = "SELECT COUNT(*) FROM (" + SQL1_count + " UNION " + SQL2_count + ") AS allcertificat WHERE idprojet = %s AND idcommune = %s "
                #SQL_count = SQL1_count + " UNION " + SQL2_count
                param3 = []
                param3.append(str(globalvars.id_projet))
                param3.append(str(globalvars.id_commune))
                listeParamsCount = listeParams1 + listeParams2 + param3
                listeParams = listeParams1 + listeParams2 + listeParamsPagination
            else:
                SQL = "SELECT * FROM (" + SQL1 + ") AS allcertificat"
                SQL_count = "SELECT COUNT(*) FROM (" + SQL1 + ") AS allcertificat WHERE idprojet = %s AND idcommune = %s "
                param3 = []
                param3.append(str(globalvars.id_projet))
                param3.append(str(globalvars.id_commune))
                listeParamsCount = listeParams1 + param3
                listeParams = listeParams1 + listeParamsPagination
            print listeParams
            #SQL = SQL + "and pd.idcertificat IS NULL"
            print SQL
            print SQL_count
            params = tuple(listeParams)
            paramsCount = tuple(listeParamsCount)
            print paramsCount
            count1 = []
            count2 = []
            params1 = tuple(listeParams1)
            params2 = tuple(listeParams2)
            print "Avant requete"
            if SQL2 != "":
                try:
                    self.cur.execute(SQL1_count, params1)
                    count1 = self.cur.fetchone()
                except StandardError as e:
                    print e
                    self.connection.rollback()
                    try:
                        SQLR = SQL1_count.replace("CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer)",
                                           "TRIM(SPLIT_PART(c.numerocertificat,'-','4')) ")
                        self.cur.execute(SQLR, params1)
                        count1 = self.cur.fetchone()
                        # print data
                        #return data
                    except Exception as err:
                        print(err)
                        self.connection.rollback()
                try:
                    self.cur.execute(SQL2_count, params2)
                    count2 = self.cur.fetchone()
                except StandardError as e:
                    print e
                    self.connection.rollback()
                    try:
                        SQLR = SQL2_count.replace("CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer)",
                                                  "TRIM(SPLIT_PART(c.numerocertificat,'-','4')) ")
                        self.cur.execute(SQLR, params2)
                        count2 = self.cur.fetchone()
                        # print data
                        # return data
                    except Exception as err:
                        print(err)
                        self.connection.rollback()
                count.append(count1[0] + count2[0])
                print count[0]

            else:
                try:
                    self.cur.execute(SQL_count, paramsCount)
                    count = self.cur.fetchone()
                except StandardError as e:
                    print e
                    self.connection.rollback()
                    try:
                        SQLR = SQL_count.replace("CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer)",
                                                  "TRIM(SPLIT_PART(c.numerocertificat,'-','4')) ")
                        self.cur.execute(SQLR, paramsCount)
                        count = self.cur.fetchone()
                        # print data
                        # return data
                    except Exception as err:
                        print(err)
                        self.connection.rollback()

            print "Après requete"
            print count
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

            results = self.pagination(SQL, params)
            print results
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
            self.connection.rollback()
# ****************************** FONCTIONS UTILES A LA PAGINATION ************************************#
    def pagination(self, SQL, params):
        print "Appel pagination"
        if self.isShowAll:
            SQL = SQL + " AND idprojet = %s AND  idcommune = %s ORDER BY ordre LIMIT %s OFFSET %s"
        else:
            SQL = SQL + " WHERE idprojet = %s AND  idcommune = %s ORDER BY ordre LIMIT %s OFFSET %s"
        print SQL
        try:
            self.cur.execute(SQL, params)
            data = self.cur.fetchall()
            #print data
            return data
        except StandardError as e:
            print e
            self.connection.rollback()
            try:
                SQL2 = SQL.replace("CAST(TRIM(SPLIT_PART(c.numerocertificat,'-','4')) as integer)", "TRIM(SPLIT_PART(c.numerocertificat,'-','4')) ")
                self.cur.execute(SQL2, params)
                data = self.cur.fetchall()
                # print data
                return data
            except Exception as err:
                print(err)
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

    def initDB(self):
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()