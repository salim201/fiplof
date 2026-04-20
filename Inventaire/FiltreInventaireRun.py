import hashlib
import sys
from logs import xlsLogger
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from FiltreInventaire import Ui_Dialog
from Utils import Utils
#from qgis.gui import QgisInterface
import psycopg2
import psycopg2.extras
from datetime import datetime
import globalvars
from models.Inventaire import Inventaire
from models.Parcelled import Parcelled
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class FiltreInventaireRun(QtGui.QDialog):

    def __init__(self, parent,connection,edition):
        QtGui.QDialog.__init__(self)
        self.parent=parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.initDB()
        print ("Tongasoa ato amin'ny Filtre Inventaire")
        self.ui.labelCurrent.setText("1")
        self.inventaires = []
        self.metadata = {"numpages": 1,"isDecision": False}
        self.btnclickedName=""
        self.edition=edition
        self.idparcelle = 1
        self.idDemande = 0
        self.MainWindow=None
        self.parent = None
        self.geometryeEdit=None
        self.stateEdition=None
        self.geomid=None
        self.canvas=None
        self.tool = None
        self.iface=None
        self.Mcs=None
        self.table_name=None
        self.erreurTransformation=""
        self.idsdemande=None
        self.dataToLog = []
        self.logger = xlsLogger.xlsLogger("Transformation_groupee ")
        self.allrowselected = []
        self.allparcelleselected = []
        self.gid=None
        self.init_actions()


    def init_actions(self):
        #fermeture bouton fermer
        self.ui.btnInventaireFermer.clicked.connect(self.close)
        self.ui.checkBoxCodeParcelle.stateChanged.connect(self.changeFieldsStatus)
        self.ui.checkBoxNomOccupant.stateChanged.connect(self.changeFieldsStatus)
        self.ui.checkBoxDateInventaire.stateChanged.connect(self.controlDateInventaire)
        self.ui.checkBoxDateInventaireEntre.stateChanged.connect(self.controlEntreDateInventaire)
        self.ui.checkBoxInventaireHameau.stateChanged.connect(self.chargeHameau)
        self.ui.checkBoxInventaireFokontany.stateChanged.connect(self.chargeFKT)
        self.ui.comboBoxInventaireFonkontany.currentIndexChanged.connect(self.changeFKT)
        self.ui.btnRechercherInventaire.clicked.connect(self.findByFilter)
        self.ui.btnAfficherTousInventaire.clicked.connect(self.findAll)
        self.ui.btnInventaireDetail.clicked.connect(self.showtheDetails)
        self.ui.pushButtonTransformerDemande.clicked.connect(self.translateDemande)
        ''' Paginations '''
        self.ui.pushButtonNext.clicked.connect(self.goto_next)
        self.ui.pushButtonPrevious.clicked.connect(self.goto_previous)
        self.ui.pushButtonFirst.clicked.connect(self.goto_first)
        self.ui.pushButtonLast.clicked.connect(self.goto_last)
        self.ui.comboBoxPages.currentIndexChanged.connect(self.goto_page)
        '''taille collonne widget'''
        self.ui.tableWidgetInventaire.setColumnWidth(0, 25)
        self.ui.tableWidgetInventaire.setColumnWidth(1, 100)
        self.ui.tableWidgetInventaire.setColumnWidth(2, 100)
        self.ui.tableWidgetInventaire.setColumnWidth(3, 200)
        self.ui.tableWidgetInventaire.setColumnWidth(4, 100)
        self.ui.tableWidgetInventaire.setColumnWidth(5, 100)
        self.ui.tableWidgetInventaire.setColumnWidth(6, 170)
        self.ui.tableWidgetInventaire.setColumnWidth(7, 170)
        self.ui.tableWidgetInventaire.itemClicked.connect(self.handleItemClicked)
        self.ui.checkBoxInventaireCheckAll.stateChanged.connect(self.cocherTout)

    def handleItemClicked(self, item):
        print 'item'
        if item.checkState() == QtCore.Qt.Checked:
            print('"%s" Checked' % item.row())
            for j in range(self.ui.tableWidgetInventaire.columnCount()):
                self.ui.tableWidgetInventaire.item(item.row(), j).setBackground(QtCore.Qt.green)
        else:
            print('"%s" unClicked' % item.row())
            for j in range( self.ui.tableWidgetInventaire.columnCount()):
                self.ui.tableWidgetInventaire.item(item.row(), j).setBackground(QtCore.Qt.transparent)

    def cocherTout(self):
        rowCount = self.ui.tableWidgetInventaire.rowCount()
        print  rowCount
        if self.ui.checkBoxInventaireCheckAll.isChecked():
            for i in range(0, rowCount):
                self.ui.tableWidgetInventaire.item(i,0).setCheckState(QtCore.Qt.Checked)
                for j in range(self.ui.tableWidgetInventaire.columnCount()):
                    self.ui.tableWidgetInventaire.item(i, j).setBackground(QtCore.Qt.green)
                i = i + 1
        else:
            for i in range(0, rowCount):
                self.ui.tableWidgetInventaire.item(i,0).setCheckState(QtCore.Qt.Unchecked)
                for j in range(self.ui.tableWidgetInventaire.columnCount()):
                    self.ui.tableWidgetInventaire.item(i, j).setBackground(QtCore.Qt.transparent)
                i = i + 1

    def changeFieldsStatus(self):
        self.ui.lineEditCodeParcelle.setEnabled(self.ui.checkBoxCodeParcelle.isChecked())
        self.ui.lineEditNomOccupant.setEnabled(self.ui.checkBoxNomOccupant.isChecked())
        self.ui.dateEditInventaire.setEnabled(self.ui.checkBoxDateInventaire.isChecked())
        self.ui.dateEditDebutInvantaire.setEnabled(self.ui.checkBoxDateInventaireEntre.isChecked())
        self.ui.dateEditFinInventaire.setEnabled(self.ui.checkBoxDateInventaireEntre.isChecked())
        self.ui.comboBoxInventaireHameau.setEnabled(self.ui.checkBoxInventaireHameau.isChecked())
        self.ui.comboBoxInventaireFonkontany.setEnabled(self.ui.checkBoxInventaireFokontany.isChecked())

    def setEnabledFalse(self):
        self.ui.lineEditCodeParcelle.setEnabled(False)
        self.ui.lineEditNomOccupant.setEnabled(False)
        self.ui.dateEditInventaire.setEnabled(False)
        self.ui.dateEditDebutInvantaire.setEnabled(False)
        self.ui.dateEditFinInventaire.setEnabled(False)
        self.ui.comboBoxInventaireHameau.setEnabled(False)
        self.ui.comboBoxInventaireFonkontany.setEnabled(False)
        self.ui.checkBoxSujetDemande.setChecked(False)
        self.ui.checkBoxCodeParcelle.setChecked(False)
        self.ui.checkBoxNomOccupant.setChecked(False)
        self.ui.checkBoxDateInventaire.setChecked(False)
        self.ui.checkBoxDateInventaireEntre.setChecked(False)
        self.ui.checkBoxInventaireHameau.setChecked(False)
        self.ui.checkBoxInventaireFokontany.setChecked(False)

    def findByFilter(self):
        self.btnclickedName="Rechercher"
        self.find()

    def findAll(self):
        print ("tonga soa findAll")
        self.btnclickedName = "Afficher tous"
        self.setEnabledFalse()
        self.find()

    def find(self):
        print ("tonga soa find")
        wheres = []
        print ("tonga eto")
        if self.ui.checkBoxSujetDemande.isChecked():
            wheres.append("sujet_demande is true ")
        if self.ui.checkBoxCodeParcelle.isChecked():
            wheres.append("codeparcelle ='" +str(self.ui.lineEditCodeParcelle.text())+"'")
        if self.ui.checkBoxNomOccupant.isChecked():
            wheres.append("LOWER(nomdemandeur) LIKE '%" + str(self.ui.lineEditNomOccupant.text()).lower().replace("'", "''") + "%'")
        if self.ui.checkBoxDateInventaire.isChecked():
            wheres.append(" CAST(date_inventaire as date) = '%s'" %(str(self.ui.dateEditInventaire.date().toString("yyyy-MM-dd"))))
        if self.ui.checkBoxDateInventaireEntre.isChecked():
            debut=str(self.ui.dateEditDebutInvantaire.date().toString("yyyy-MM-dd"))
            fin = str(self.ui.dateEditFinInventaire.date().toString("yyyy-MM-dd"))
            wheres.append(" CAST(date_inventaire as date) BETWEEN  '"+debut+"' AND '"+fin+"'")
        if self.ui.checkBoxInventaireFokontany.isChecked():
            if self.ui.checkBoxInventaireHameau.isChecked():
                wheres.append("LOWER(nomhameau) ='" + str(self.ui.comboBoxInventaireHameau.currentText()).lower().replace("'","''") + "'")
            else :
                wheres.append("LOWER(fkt) ='"+str(self.ui.comboBoxInventaireFonkontany.currentText()).lower().replace("'", "''")+"'")
        wheres.append(
            " id_commune = %s" % (globalvars.id_commune))
        print wheres

        page = int(self.ui.labelCurrent.text())
        self.inventaires = Inventaire.find_where(self.connection, self.metadata, wheres, page)
        self.ui.tableWidgetInventaire.setRowCount(len(self.inventaires))

        print len(self.inventaires)
        for i, d in enumerate(self.inventaires):
            if d.date_inventaire is None : d.date_inventaire=""
            else: d.date_inventaire=d.date_inventaire.strftime("%m-%d-%Y")
            if d.codeparcelle is None: d.codeparcelle = ""
            if d.nomdemandeur is None: d.nomdemandeur=""
            else :d.nomdemandeur = str(d.nomdemandeur).decode('utf-8')
            if d.numdemande is None: d.numdemande = ""
            if d.hameau is None: d.hameau = ""
            if d.fkt is None: d.fkt = ""
            if d.datedemande is None : d.datedemande=""
            else: d.datedemande=d.datedemande.strftime("%m-%d-%Y")
            item = QtGui.QTableWidgetItem(True)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(False)
            self.ui.tableWidgetInventaire.setItem(i, 0, item)
            self.ui.tableWidgetInventaire.setItem(i, 1, QtGui.QTableWidgetItem(str(d.date_inventaire)))
            self.ui.tableWidgetInventaire.setItem(i, 2, QtGui.QTableWidgetItem(str(d.codeparcelle)))
            self.ui.tableWidgetInventaire.setItem(i, 3, QtGui.QTableWidgetItem(str(d.nomdemandeur)))
            self.ui.tableWidgetInventaire.setItem(i, 4, QtGui.QTableWidgetItem(str(d.numdemande)))
            self.ui.tableWidgetInventaire.setItem(i, 5, QtGui.QTableWidgetItem(str(d.datedemande)))
            self.ui.tableWidgetInventaire.setItem(i, 6, QtGui.QTableWidgetItem(str(d.hameau)))
            self.ui.tableWidgetInventaire.setItem(i, 7, QtGui.QTableWidgetItem(str(d.fkt)))
        for i in range(1, 6):
              Utils.setTableWidgetColumnReadOnly(self.ui.tableWidgetInventaire, i)
        self.update_navigation_buttons()
        self.fill_combo_pages()

    def showtheDetails(self):
        print "hello details"
        currentRow=int(self.ui.tableWidgetInventaire.currentRow())
        print currentRow
        numdemande = self.ui.tableWidgetInventaire.item(currentRow, 4).text()
        if numdemande=="" : print "vide"
        else :
            try:
                print numdemande
                id=Parcelled.find_idby_numdemande(self.connection, numdemande)
                print id
                self.idparcelle = int(id[1])
                self.idDemande = int(id[0])
                self.gid= int(id[1])
                # from DetailsDemandeRunn import DetailsDemandeRunn
                from Demande.DemandeDetailsRun import DemandeDetailsRun
                # detail = DetailsDemandeRunn(self)
                detail = DemandeDetailsRun(self)
                detail.show()
                result = detail.exec_()
            except Exception as err:
                print (err)

    def translateDemande(self):
        self.dataToLog = []
        title = ["code_parcelle", "numero_demande", "etat_insertion", "erreur"]
        dateDemande=str(self.ui.dateEditDateTransformationDemande.date().toString("yyyy-MM-dd"))
        dateDemande = datetime.strptime(dateDemande, "%Y-%m-%d")
        dateDemande=dateDemande.date()
        cptDemande = self.getCptDemande()
        codesLoc = self.getCodesLoc()
        self.listidselected()
        isOK=False
        print "translate demande"
        print self.allrowselected
        for row in self.allrowselected:
            self.gid = None
            self.idsdemande = None
            print row
            codeparcelle=str(self.ui.tableWidgetInventaire.item(row, 2).text())
            num_demande =str( self.ui.tableWidgetInventaire.item(row, 4).text())
            num_demande=num_demande.strip("")
            print "codeparcelle---"+codeparcelle
            isOK = True
            if codeparcelle is None or codeparcelle=="" or num_demande !="":
                print 'nakato anie izy e'
                if codeparcelle is None or codeparcelle == "":
                    print "aucun code parcelle"
                    self.erreurTransformation += self.erreurTransformation + ", code parcelle null ou vide"
                if  num_demande!="" :
                    print "num "+ num_demande
                    self.erreurTransformation += self.erreurTransformation + ", Parcelle ayant num de demande"
            else:
                cursor = self.connection.cursor()
                # maka ny info rehetra mahakasika ny inventaire ao anaty parcelle
                try:
                    print "tonga ato e "
                    cursor.execute(
                        "select gid,pd.idhameau,h.idfokontany as id_fokontany,fkt,id_commune,commune,district,region,consistance,cout,idcategorie"
                        " from parcelle_d pd "
                        " INNER JOIN hameau h on  h.idhameau=pd.idhameau"
                        " INNER JOIN fokontany f on f.idfokontany=h.idfokontany WHERE codeparcelle = (%s)",
                        (str(codeparcelle),))
                    infoparcelle = cursor.fetchone()
                    print 'infoparcelle'
                    print len(infoparcelle)
                    oneparcelle=infoparcelle[0]
                    print oneparcelle
                    self.gid = infoparcelle[0]
                    region = str(infoparcelle[7])
                    district = str(infoparcelle[6])
                    idfokontany = int(infoparcelle[2])
                    idCommune = int(infoparcelle[4])
                    consistance = str(infoparcelle[8])
                    idhameau=int(infoparcelle[1])

                except Exception as e:
                    print(e)
                    isOK = False
                    self.erreurTransformation += self.erreurTransformation + " / " +e

                # demande update
                print "code localites"
                codeGuichet = str(codesLoc[1]).strip()
                codeDistrict = str(codesLoc[0]).strip()
                print "-----------------------------------------eto------------------------------------------"
                print codeGuichet
                print codeDistrict
                if len(codeGuichet) == 1:
                    codeGuichet = '0' + codeGuichet

                dep = codeDistrict + '-' + codeGuichet + '-F-'
                numeroDemande = dep + str(cptDemande)
                print numeroDemande
                print "-----------------------------------------vita------------------------------------------"
                cursor = self.connection.cursor()
                print numeroDemande
                # insertion demande
                try:
                    print "aty amin insert"
                    #sql = "INSERT INTO demande (numdemande, gid,datedemande, region, district, idfokontany, idcommune, cout, consistance,idprojet, categorie, code_parcelle)
                    # VALUES ('" + numeroDemande + "'," + int( self.idparcelle) +
                    # "','" + dateDemande + "','" + region + "', '" + district + "', '" + idfokontany + "'," + idCommune + ", 0 ,'"  + consistance + "', " + globalvars.id_projet + ", '" + categorie + "', '" + codeparcelle + "') returning iddemande)"
                    gid=int(self.gid)
                    print gid

                    """cursor.execute("INSERT INTO demande(numdemande,gid,datedemande,region, district,idfokontany, idcommune, cout,consistance,idprojet,code_parcelle)"
                        " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (numeroDemande, gid, dateDemande, region, district, idfokontany, idCommune, 0, consistance,
                        globalvars.id_projet, str(codeparcelle)))"""
                    cursor.execute("UPDATE demande SET numdemande=%s,datedemande=%s WHERE code_parcelle=%s returning numdemande ;"
                                   "INSERT INTO demande(numdemande,gid,datedemande,region, district,idfokontany, idcommune, cout,consistance,idprojet,code_parcelle) returning numdemande"
                                    "SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
                                    "WHERE NOT EXISTS (SELECT * FROM demande WHERE code_parcelle=%s);",
                                   (numeroDemande,dateDemande,str(codeparcelle),numeroDemande,gid,dateDemande,region,district,idfokontany,idCommune,0,consistance,globalvars.id_projet,str(codeparcelle),str(codeparcelle)))
                    cursor.commit()
                    if cursor.fetchone() :
                        "insert"
                        self.idsdemande= self.cur.fetchone()
                    else :
                        print "update"
                    return
                except Exception as e:
                    print(e)
                    isOK = False
                    self.erreurTransformation += self.erreurTransformation + " " + e
                    self.connection.rollback()
                update_compteur=False
                try:
                    if self.idsdemande!=None :
                        #update Commune
                        print(" enter cptdemande")
                        cptDemande = cptDemande + 1
                        print(" cptDemanded  value" )
                        print cptDemande
                        print globalvars.id_commune
                        cursor.execute("UPDATE commune SET cptdemande=(%s)  WHERE idcommune = (%s)",
                                            (int(cptDemande), int(globalvars.id_commune)))
                        self.connection.commit()
                        update_compteur=True
                except Exception as e:
                    print(e)
                    isOK = False
                    self.erreurTransformation += self.erreurTransformation + " " + e
                    self.connection.rollback()
                    self.cur.execute("DELETE FROM demande WHERE iddemande = %s", (self.idsdemande,))
                    self.connection.commit()

                updateparcelle=False
                try:
                    # update Parcelle
                    if update_compteur:
                        print(" update num demande parcelle_d")
                        cursor.execute("UPDATE parcelle_d SET numdemande=(%s) WHERE gid = (%s)", (numeroDemande, gid))
                        self.connection.commit()
                        print "vita ny insertion "+ numeroDemande
                        updateparcelle= True
                except Exception as e:
                    print(e)
                    isOK = False
                    self.erreurTransformation += self.erreurTransformation + "- erreur upddate paecelle " + e
                    self.connection.rollback()
                    self.cur.execute("DELETE FROM demande WHERE iddemande = %s", (self.idsdemande,))
                    self.connection.commit()
                    cursor.execute("UPDATE commune SET cptdemande=(%s)  WHERE idcommune = (%s)",
                                   (int(cptDemande)-1, int(globalvars.id_commune)))
                    self.connection.commit()

                try:
                    # update avoir demande
                    if updateparcelle:
                        print(" avoir demande")
                        cursor.execute("UPDATE avoir_demande SET iddemande=(%s) WHERE idparcelle = (%s)", (self.idsdemande, gid))
                        self.connection.commit()
                        print "vita ny insertion  avoir_demande"
                except Exception as e:
                    print(e)
                    isOK = False
                    self.erreurTransformation += self.erreurTransformation + "- erreur upddate paecelle " + e
                    self.connection.rollback()
                    self.cur.execute("DELETE FROM demande WHERE iddemande = %s", (self.idsdemande,))
                    self.connection.commit()
                    cursor.execute("UPDATE commune SET cptdemande=(%s)  WHERE idcommune = (%s)",
                                   (int(cptDemande)-1, int(globalvars.id_commune)))
                    self.connection.commit()
                    cursor.execute("UPDATE parcelle_d SET numdemande=None WHERE gid = (%s)", (gid,))
                    self.connection.commit()
            etatInsertion=""
            print 'mandalo eto indray ary'
            if self.erreurTransformation != "":
                etatInsertion = "TRANSFORMATION INACCOMPLIE"
            else:
                etatInsertion = "TRANSFORMATION REUSSITE - DEMANDE num: " + num_demande
            self.dataToLog.append(
                    {"code_parcelle": str(codeparcelle), "numero_demande": num_demande, "etat_insertion": etatInsertion,
                     "erreur": self.erreurTransformation})
            print self.dataToLog
            print '-----------vita-----------'
        try:
            print title
            print self.dataToLog
            self.logger.addSheet(title=title, data=self.dataToLog, sheet_name="Log Transformation demande")
            self.logger.write()
        except Exception as e:
            print "erreur  e"
            print e

    def listidselected(self):
        self.allrowselected = []
        self.allparcelleselected = []
        p=0
        for j in range(self.ui.tableWidgetInventaire.rowCount()):
            print j
            items = self.ui.tableWidgetInventaire.item(j, 0)
            if items.checkState() == QtCore.Qt.Checked:
                if str(self.ui.tableWidgetInventaire.item(j, 2).text()) == "":
                    self.erreurTransformation+=self.erreurTransformation+ 'code parcelle vide'
                else:
                    self.allrowselected.append(j)
                    self.allparcelleselected.append(str(self.ui.tableWidgetInventaire.item(j,2).text()))

        print 'self.allrowselected'
        print self.allrowselected
        print self.allparcelleselected

    '''*****************************ref demande***********************************'''
    def getCptDemande(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT cptdemande FROM commune WHERE idcommune = %s", (globalvars.id_commune,))
            res = cursor.fetchone()
            return res[0]
        except Exception as err:
            print(err)
            self.connection.rollback()
        cursor.close()

    def getCodesLoc(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT d.codedistrict, c.codeg FROM commune c INNER JOIN district d ON c.iddistrict = d.iddistrict WHERE idcommune = %s", (globalvars.id_commune,))
            res = cursor.fetchone()
            return res
        except Exception as err:
            print(err)
            self.connection.rollback()
        cursor.close()

    ''' ************************************ paginations ************************************ '''
    def goto_next(self):
        current = int(self.ui.labelCurrent.text()) + 1
        self.ui.labelCurrent.setText(str(current))
        self.find()

    def goto_previous(self):
        current = int(self.ui.labelCurrent.text()) - 1
        self.ui.labelCurrent.setText(str(current))
        self.find()

    def goto_first(self):
        self.ui.labelCurrent.setText("1")
        self.find()

    def goto_last(self):
        self.ui.labelCurrent.setText(str(self.metadata["numpages"]))
        self.find()

    def goto_page(self):
        index = self.ui.comboBoxPages.currentIndex() + 1
        self.ui.labelCurrent.setText(str(index))
        self.find()

    def update_navigation_buttons(self):
        current = int(self.ui.labelCurrent.text())
        self.ui.pushButtonFirst.setEnabled(current > 1)
        self.ui.pushButtonPrevious.setEnabled(current > 1)
        self.ui.pushButtonNext.setEnabled(current < self.metadata["numpages"])
        self.ui.pushButtonLast.setEnabled(current < self.metadata["numpages"])

    def fill_combo_pages(self):
        self.ui.comboBoxPages.blockSignals(True)
        self.ui.comboBoxPages.clear()
        current = int(self.ui.labelCurrent.text())
        for i in range(self.metadata["numpages"]):
            self.ui.comboBoxPages.addItem("%s/%s" % (i + 1, self.metadata["numpages"]))
        self.ui.comboBoxPages.setCurrentIndex(current - 1)
        self.ui.comboBoxPages.blockSignals(False)

        ''' ************************************ FIN paginations ************************************ '''

    def controlDateInventaire(self):
        print ("Tongasoa ato amin'ny controle date")
        isChecked=self.ui.checkBoxDateInventaire.isChecked()
        if isChecked == True :
            print ("controle date")
            self.ui.checkBoxDateInventaireEntre.setChecked(False)
        self.changeFieldsStatus()

    def controlEntreDateInventaire(self):
        print ("Tongasoa ato amin'ny controle entre deux dates")
        isChecked=self.ui.checkBoxDateInventaireEntre.isChecked()
        if isChecked == True :
            print ("controle entre deux dates")
            self.ui.checkBoxDateInventaire.setChecked(False)
        self.changeFieldsStatus()

    def controlDateDecision(self):
        print ("Tongasoa ato amin'ny controle date decision")
        isChecked=self.ui.checkBoxDateDecision.isChecked()
        if isChecked == True :
            print ("controle date")
            self.ui.checkBoxDateDecisionEntre.setChecked(False)
        self.changeFieldsStatus()

    def controlEntreDateDecision(self):
        print ("Tongasoa ato amin'ny controle entre deux dates decision")
        isChecked=self.ui.checkBoxDateDecisionEntre.isChecked()
        if isChecked == True :
            print ("controle entre deux dates oui")
            self.ui.checkBoxDateDecision.setChecked(False)
        self.changeFieldsStatus()

    def initDB(self):
        self.cur = self.connection.cursor()
        self.CurrValeurCF = 0

    def chargeFKT(self):
        self.changeFieldsStatus()
        isCheckedFkt = self.ui.checkBoxInventaireFokontany.isChecked()
        if isCheckedFkt == False:
            self.ui.checkBoxInventaireHameau.setChecked(False)
            self.ui.comboBoxInventaireHameau.setEnabled(False)
        self.selectFkt()

    def changeFKT(self):
        print ("changeFKT et")
        textFkt = self.ui.comboBoxInventaireFonkontany.currentText()
        self.ui.comboBoxInventaireHameau.clear()
        print (textFkt)
        if not (textFkt) :  print ()
        else :
            self.hameauFkt(textFkt)

    def selectFkt(self):
        self.ui.comboBoxInventaireFonkontany.clear()
        try:
            self.cur.execute("SELECT nomfokontany, idfokontany, codefokontany FROM fokontany WHERE idcommune = %s",
                             (globalvars.id_commune,))
            fkts = self.cur.fetchall()
            self.ui.comboBoxInventaireFonkontany.addItem("", "")
            for fkt in fkts:
                self.ui.comboBoxInventaireFonkontany.addItem(fkt[0], fkt[1])

        except StandardError as e:
            print e



    def hameauFkt(self, fkt):
        self.ui.comboBoxInventaireHameau.clear()
        test=str(fkt)
        try:
            self.cur.execute("SELECT nomhameau, idhameau, h.idfokontany FROM public.hameau h INNER JOIN fokontany  f on f.idfokontany=h.idfokontany where f.nomfokontany=%s",
                             (test,))
            hmx = self.cur.fetchall()
            self.ui.comboBoxInventaireHameau.addItem("", "")
            for hm in hmx:
                self.ui.comboBoxInventaireHameau.addItem(hm[0], hm[1])

        except StandardError as e:
            print e

    def chargeHameau(self):
        self.ui.comboBoxInventaireHameau.clear()
        print ("Tokony hamafa")
        self.changeFieldsStatus()
        self.textFkt=self.ui.comboBoxInventaireFonkontany.currentText()
        if not (self.textFkt) :  print ()
        else :
            self.hameauFkt(self.textFkt)


