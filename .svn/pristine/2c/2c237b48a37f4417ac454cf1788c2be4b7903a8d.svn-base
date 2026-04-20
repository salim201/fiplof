# coding: utf-8
import os
from logs import xlsLogger
from PyQt4 import Qt,QtGui, QtCore
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *


from Certificat.TransformationGroupeeDmd import Ui_Dialog
import globalvars
from models.Commune import Commune
from models.District import District
from models.Region import Region
from Etats.Html2Pdf import Html2Pdf
import webbrowser
import tempfile
from random import randint
import datetime
from Utils import Utils
from models.Demande import Demande
from PyPDF2 import PdfFileMerger
from models.Demande import Demande

import psycopg2.extras

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class TransformationGroupeeDmdRun(QDialog):
#    def __init__(self, connection, canvas, parent):
    def __init__(self, connection):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.idparcelle = None
        self.numDemandes = []
        self.numCF = None
        self.idsFokontany = []
        self.idsHameau = []
        self.allrowdmdselected = []# row demande selectionnés dans le tableau
        self.alliddmdselected = []# id demande selectionnés dans le tableau
        self.alldemande=[]
        self.metadata = {"numpages": 1}
        self.demandes=[]
        self.nbdmdaaffiche=0
        self.commune = Commune.findById(self.connection, globalvars.id_commune)
        self.district = District.findById(self.connection, self.commune.iddistrict)
        self.region = Region.findById(self.connection, self.district.idregion)
        self.paths=[]
        self.perssignature=''
        self.perscin1=''
        self.perscin2=''
        self.current_value = 0
        self.ui.progressBarlisting.setValue(0)
        self.nbrepetition=0
        self.pas=1
        self.dataToCheck = []
        try:
            self.initDB()
            self.initActions()
        except Exception as e:
            print(e)
        self.template=''
        self.orientation='Landscape'
        self.numeroCertificat=""
        self.currentValCF = ""
        self.CurrValeurCF = ""
        self.idParcelle=0
        self.erreurTGroupee=""
        self.iddemandeGroupee=""
        self.logger = xlsLogger.xlsLogger("Transformation_groupee ")
        self.dataToLog=[]
        self.current_value = 0
        self.pas=10

    def initDB(self):
        self.cur = self.connection.cursor()
        print self.cur
        print "vita dlkjfkldjglkfdjlkgjdfkljgldf"

    def initActions(self):
        print 'ato e'
        #self.setWindowTitle(u"Transformation Groupée Demande en CF")
        #self.ui.pushButtonExport.setText( "TRANSFORMER")
        self.ui.checkBoxNumDemande.clicked.connect(self.changeFieldsStatus)
        self.ui.checkBoxNumdecision.clicked.connect(self.changeFieldsStatus)
        self.ui.checkBoxHameau.stateChanged.connect(self.chargeHameau)
        self.ui.checkBoxFkt.stateChanged.connect(self.chargeFKT)
        self.ui.checkBoxFkt.stateChanged.connect(self.chargeFKT)
        self.ui.comboBoxFokontany.currentIndexChanged.connect(self.changeFKT)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercher)
        self.ui.tableWidgetDemande.setColumnWidth(0, 25)
        self.ui.checkBoxCocherTous.stateChanged.connect(self.cocherTout)
        self.ui.tableWidgetDemande.itemClicked.connect(self.handleItemClicked)
        self.ui.pushButtonTransformer.clicked.connect(self.transformationGroupee)


    def changeFieldsStatus(self):
        self.ui.lineEditNumeroDemande.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.comboBoxFokontany.setEnabled(self.ui.checkBoxFkt.isChecked())
        self.ui.comboBoxHameau.setEnabled(self.ui.checkBoxHameau.isChecked())
        self.ui.lineEditNumdecision.setEnabled(self.ui.checkBoxNumdecision.isChecked())

    def progresswithp(self, p):
        self.ui.progressBarlisting.setValue(p)

    def reset(self):
        self.current_value = 0
        self.ui.progressBarlisting.reset()

    def progress(self):
        print '-----progress---'
        print self.current_value
        if self.current_value <=self.ui.progressBarlisting.maximum() :
            self.current_value += self.pas
            self.ui.progressBarlisting.setValue(self.current_value)
        print '-----progress suivant---'
        print self.current_value

    def transformationGroupee(self):
        self.ui.progressBarlisting.setValue(1)
        self.ui.pushButtonTransformer.setEnabled(False)
        title = ["code_parcelle", "numero_demande", "etat_insertion", "erreur"]
        print '-------------------transformation groupee----------------------'
        #récupération demande secelctionner
        self.listiddmdselected()
        print self.alliddmdselected
        self.dataToLog = []
        if len(self.alliddmdselected)>0 :
            self.pas = 100 / len(self.alliddmdselected)
            print ' debut transformation demande'
            for id in self.alliddmdselected :
                self.progress()
                self.transformationID(id)
            self.rechercher()
            try:
                print title
                print self.dataToLog
                self.logger.addSheet(title=title, data=self.dataToLog, sheet_name="Log Transformation groupee")
                print 'ato ve'
                self.logger.write()
            except Exception as e:
                print "erreur  e"
                print e
            self.ui.progressBarlisting.setValue(100)
            QMessageBox.information(None, 'Rapport transformation', u'Execution terminée')
        else :
            QMessageBox.critical(self, "Erreur", u"aucune demande selectionnée")

        self.ui.progressBarlisting.setValue(0)
        self.ui.pushButtonTransformer.setEnabled(True)

    def transformationID(self, idDemande):
        print "transformationID"
        self.erreurTGroupee=""
        idDemande=int(idDemande)
        self.iddemandeGroupee=str(idDemande)
        data=[]
        print idDemande
        try:
            data= Demande.select_by_id(self.connection,idDemande)
            print data
        except Exception as e:
            print e
            self.erreurTGroupee=self.erreurTGroupee+" erreur de selection demande: "+ str(idDemande)
        if len(data)>0 :
            self.writeData(data)
        else:
            self.erreurTGroupee = self.erreurTGroupee + " erreur selection demande : " + str(idDemande)
            print data
            print self.erreurTGroupee

    def listiddmdselected(self):
        self.allrowdmdselected = []
        self.alliddmdselected = []
        for j in range(self.ui.tableWidgetDemande.rowCount()):
            items = self.ui.tableWidgetDemande.item(j, 0)
            if items.checkState() == QtCore.Qt.Checked:
                if (self.ui.tableWidgetDemande.item(j, 7).text() == ""):
                    print int(self.ui.tableWidgetDemande.item(j, 1).text())
                else:
                    self.allrowdmdselected.append(j)
                    self.alliddmdselected.append(int(self.ui.tableWidgetDemande.item(j, 1).text()))

    def setNumCF(self) :
        print "setNumCF"
        try:
            self.cur.execute("SELECT *   FROM commune  WHERE idcommune=%s", [int(globalvars.id_commune)])
            comm = self.cur.fetchone()
            codGuichet = comm[9]
            self.currentValCF = comm[6]
            self.CurrValeurCF = comm[6]
            # a demander Salim
            if codGuichet < 10:
                codGuichet = "0" + str(codGuichet)
            # Recuperer le district
            self.cur.execute(
                    "SELECT d.nomdistrict, d.iddistrict, d.codedistrict FROM district d, commune c WHERE d.iddistrict = c.iddistrict AND c.idcommune = %s",
                        (globalvars.id_commune,))
            dist = self.cur.fetchone()
            print dist
        except StandardError as e:
            print e
            self.erreurTGroupee+= e+ ' Demande concernee: '+ self.iddemandeGroupee

        numCert = str(dist[2]).strip() + "-" + str(codGuichet).strip() + "-KT-" + str(self.currentValCF).strip()
        print numCert
        self.numeroCertificat = numCert

    def writeData(self, data):
        print "to write"
        dataforcontrol=[]
        code_parcelle, numdemande, etatInsertion, erreur = "", "", "", ""

        self.numeroCertificat = ""
        self.currentValCF = ""
        self.CurrValeurCF = ""

        dataforcontrol.append(data[0])
        dataforcontrol.append(data[1])
        dataforcontrol.append(data[2])
        dataforcontrol.append(data[12])
        dataforcontrol.append(data[11])
        dataforcontrol.append(data[9])
        dataforcontrol.append(data[7])
        dataforcontrol.append(data[3])
        dataforcontrol.append(data[6])
        dataforcontrol.append(data[5])

        idemande = data[0]
        numdemande = data[1]
        datedemande = data[2]
        numdecision = data[12]
        datedecision = data[11]
        categorie = data[9]
        consistance = data[7]
        datereconnaissance = data[3]
        idfokontany = data[6]
        self.idParcelle=data[4]
        code_parcelle=data[13]
        geom=data[5]

        self.controlData(dataforcontrol)
        self.setNumCF()
        if self.erreurTGroupee=="":
            date = datetime.datetime.now()
            print 'numero karatany//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
            print self.numeroCertificat.strip()

            if idfokontany != "" or idfokontany  is not None:#idfokontany not null
                print 'idfokontany'
                try:
                    SQL = "INSERT INTO certificat (numerocertificat, numerodemande, typecertificat, datereconnaissance, datecreation, idfokontany, idprojet, idcommune) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) returning idcertificat"
                    params = (self.numeroCertificat.strip(), numdemande.strip(),"Certificat foncier",
                              datereconnaissance, date.now(), idfokontany, globalvars.id_projet,
                              globalvars.id_commune)
                    self.cur.execute(SQL, params)
                    self.connection.commit()
                    self.idsCertificat = self.cur.fetchone()
                    print  self.idsCertificat
                except psycopg2.Error as e:
                    # print e.pgcode
                    if e.pgcode == "23505":
                        QtGui.QMessageBox.critical(self, "Erreur", u"Ce numero de certificat éxiste déjà")
                        self.erreurTGroupee += "le numero de certificat "+ self.numeroCertificat +" éxiste déjà"
                        self.connection.rollback()
                except StandardError as e:
                    print e
                    self.connection.rollback()
            else:
                print "tsy misy certificat"
                self.erreurTGroupee += " le numero de certificat "

            # Enregistrement proprietaires personne physique
            # Vider proprietaire avant reinsertion apres modification des proprietaires
            try:
                self.cur.execute("DELETE FROM proprietaireparcelle WHERE idparcelle = %s", (self.idParcelle,))
                self.connection.commit()
            except StandardError as e:
                print(e)
                self.erreurTGroupee += e + "erreur suppression veuillez contacter votre administrateur"
                self.connection.rollback()
                self.cur.execute("DELETE FROM certificat WHERE idCertificat = %s", (self.idsCertificat,))
                self.connection.commit()

            #select personnne iscrit dans demande
            try:
                self.cur.execute(
                    "SELECT idpersonne, iddemande, idparcelle, representant FROM public.avoir_demande  a WHERE a.idparcelle =%s AND a.iddemande = %s",
                    (self.idParcelle,idemande))
                proprietaire_demande = self.cur.fetchall()
                print 'avoir_demande'
                print proprietaire_demande
            except StandardError as e:
                print(e)
                self.erreurTGroupee += e + "selection personne inachevée"
                self.connection.rollback()
                self.cur.execute("DELETE FROM certificat WHERE idCertificat = %s", (self.idsCertificat,))
                self.connection.commit()

            try:
                for proprietaire in proprietaire_demande:
                    print "avoir"
                    print proprietaire
                    if proprietaire[3] == True:
                        self.cur.execute(
                            "INSERT INTO proprietaireparcelle (idpersonne, idparcelle, representant, estcoproprietaire) VALUES (%s, %s, %s, %s)",
                            (proprietaire[0], proprietaire[2], True, False))
                    else:
                        self.cur.execute(
                            "INSERT INTO proprietaireparcelle (idpersonne, idparcelle, representant, estcoproprietaire) VALUES (%s, %s, %s, %s)",
                            (proprietaire[0], proprietaire[2], False, False))
            except StandardError as e:
                print(e)
                self.connection.rollback()
                self.cur.execute("DELETE FROM certificat WHERE idCertificat = %s", (self.idsCertificat,))
                self.connection.commit()
                self.erreurTGroupee += e + " erreur d'insertion proprietaire"
                self.cur.execute("DELETE FROM certificat WHERE idCertificat = %s", (self.idsCertificat,))
                self.connection.commit()

            try:
                print "modification parcelle"
                self.cur.execute("UPDATE parcelle_d SET idcertificat = %s WHERE gid = %s", (self.idsCertificat[0],  self.idParcelle))
                self.connection.commit()

                # update compteur demande
                self.currentValCF = int(self.currentValCF) + 1
                self.cur.execute("UPDATE commune SET cptcertificat=(%s)  WHERE idcommune = (%s)",
                                 (int(self.currentValCF), int(globalvars.id_commune)))
                self.connection.commit()

            except StandardError as e:
                print e
                self.connection.rollback()
                self.erreurTGroupee += e + " mise à jour commune et parcelle "
                self.cur.execute("DELETE FROM certificat WHERE idCertificat = %s", (self.idsCertificat,))
                self.connection.commit()


            print self.erreurTGroupee
            if self.erreurTGroupee=="" :
                #Ecriture dans le journal
                print "+++++++++++++++++++++++++++Ecriture dans le journal+++++++++++++++++"
                self.idCF = self.idsCertificat[0]
                from Projet.journalRunn import journal
                journal = journal(self.connection)
                journal.inserToJournal(globalvars.id_user, self.idsCertificat[0], u"Certificat", u"Création de certificat foncier")
                self.insertIntoHistorique(self.idCF)
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Enregistrement du certificat reussi")
                # MAJ compteur demande

                self.CurrValeurCF = self.CurrValeurCF + 1
                self.cur.execute("UPDATE commune SET cptcertificat=(%s)  WHERE idcommune = (%s)",
                                    (self.CurrValeurCF, globalvars.id_commune))
                self.connection.commit()
            else :
                print "+++++++++++++++++++++++++++self.erreurTGroupee+++++++++++++++++"
                self.erreurTGroupee += e + " journal non mise à jour"
        if self.erreurTGroupee!="" :
            etatInsertion = "TRANSFORMATION INACCOMPLIE"
        else:
            etatInsertion="TRANSFORMATION REUSSITE - CF num: " +self.numeroCertificat.strip()
        self.dataToLog.append(
            {"code_parcelle": code_parcelle, "numero_demande": numdemande, "etat_insertion": etatInsertion,
             "erreur": self.erreurTGroupee})

    def insertIntoHistorique(self, idCF):
        from .HistoriqueRun import HistoriqueRun
        datenow = datetime.datetime.now()
        dateOp = datetime.date(datenow.year, datenow.month, datenow.day)
        historique = HistoriqueRun(self.connection, self)
        historique.writeInHistorique(idCF, u"Création initiale", dateOp)

    def controlData(self,data):
        error = ""
        print 'controledata eto'
        print list(data)
        print data[0]
        idemande = data[0]
        numdemande = data[1]
        datedemande = data[2]
        numdecision = data[3]
        datedecision = data[4]
        categorie = data[5]
        consistance = data[6]
        datereconnaissance = data[7]
        idfokontany = data[8]
        geom = data[9]

        if datedemande is None or datedemande == "":
            error += " Date demande -"
        if datereconnaissance is None or datereconnaissance == "":
            error += " Date reconnaissance -"
        if consistance is None or consistance == "":
            error += " Consistance -"
        if categorie is None or categorie == "":
            error += " Catégorie -"
        if datedecision is None or datedecision == "":
            error += " Date décision -"
        if numdecision is None or numdecision == "":
            error += " Numéro décision -"
        if idfokontany is None or idfokontany == "":
                error += " IdFOKONTANY -"
        if geom is None or geom == "":
                error += " Géométrie -"

        if error != "":
            if numdemande is None or numdemande == "":
                print " Num demande inexistant(e)(s) - demande concernée " + idemande
                self.erreurTGroupee+=" Num demande inexistant(e)(s) - demande concernée " + idemande
                #QMessageBox.critical(self, "Erreur", self.erreurTGroupee)
            else:
                print error + " inexistant(s) - demande concernée " + numdemande
                self.erreurTGroupee += error + " inexistant(e)(s) - demande concernée " + numdemande
                #QMessageBox.critical(self, "Erreur", self.erreurTGroupee)

        print 'controledata vita eto'

    def handleItemClicked(self, item):
        print 'récupération ligne coché'
        if item.checkState() == QtCore.Qt.Checked:
            print('"%s" Checked' % item.row())
            #self._list.append(item.row())
            #self.ui.tableWidgetDemande.selectRow(item.row())
            for j in range( self.ui.tableWidgetDemande.columnCount()):
                self.ui.tableWidgetDemande.item(item.row(), j).setBackground(QtCore.Qt.green)
             #   print self.ui.tableWidgetDemande.selectedItems()
        else:
            print('"%s" unClicked' % item.row())
            for j in range( self.ui.tableWidgetDemande.columnCount()):
                self.ui.tableWidgetDemande.item(item.row(), j).setBackground(QtCore.Qt.transparent)

    def cocherTout(self):
        rowCount = self.ui.tableWidgetDemande.rowCount()
        if self.ui.checkBoxCocherTous.isChecked():
            for i in range(0, rowCount):
                self.ui.tableWidgetDemande.item(i, 0).setCheckState(QtCore.Qt.Checked)
                for j in range(self.ui.tableWidgetDemande.columnCount()):
                    self.ui.tableWidgetDemande.item(i, j).setBackground(QtCore.Qt.green)
                i = i + 1
        else:
            for i in range(0, rowCount):
                self.ui.tableWidgetDemande.item(i, 0).setCheckState(QtCore.Qt.Unchecked)
                for j in range(self.ui.tableWidgetDemande.columnCount()):
                    self.ui.tableWidgetDemande.item(i, j).setBackground(QtCore.Qt.transparent)
                i = i + 1

    def chargeFKT(self):
        print ("chargeFKT")
        self.changeFieldsStatus()
        isCheckedFkt = self.ui.checkBoxFkt.isChecked()
        if isCheckedFkt == False:
            self.ui.checkBoxHameau.setChecked(False)
            self.ui.comboBoxHameau.setEnabled(False)
        self.selectFkt()

    def changeFKT(self):
        print ("changeFKT et")
        textFkt = self.ui.comboBoxFokontany.currentText()
        self.ui.comboBoxHameau.clear()
        print (textFkt)
        if not (textFkt) :  print ()
        else :
            self.hameauFkt(textFkt)

    def selectFkt(self):
        self.ui.comboBoxFokontany.clear()
        try:
            self.cur.execute("SELECT nomfokontany, idfokontany, codefokontany FROM fokontany WHERE idcommune = %s",
                             (globalvars.id_commune,))
            fkts = self.cur.fetchall()
            self.ui.comboBoxFokontany.addItem("", "")
            for fkt in fkts:
                self.ui.comboBoxFokontany.addItem(fkt[0], fkt[1])

        except StandardError as e:
            print e

    def hameauFkt(self, fkt):
        self.ui.comboBoxHameau.clear()
        test=str(fkt)
        try:
            self.cur.execute("SELECT nomhameau, idhameau, h.idfokontany FROM public.hameau h INNER JOIN fokontany  f on f.idfokontany=h.idfokontany where f.nomfokontany=%s",
                             (test,))
            hmx = self.cur.fetchall()
            self.ui.comboBoxHameau.addItem("", "")
            for hm in hmx:
                self.ui.comboBoxHameau.addItem(hm[0], hm[1])

        except StandardError as e:
            print e

    def chargeHameau(self):
        self.ui.comboBoxHameau.clear()
        print ("Tokony hamafa")
        self.changeFieldsStatus()
        self.textFkt=self.ui.comboBoxFokontany.currentText()
        if not (self.textFkt) :  print ()
        else :
            self.hameauFkt(self.textFkt)

    def rechercher(self):
        print 'jklj'
        #self.ui.tableWidgetDemande.setRowCount(0)
        #self.ui.checkBoxCocherTous.setChecked(False)
        #self.ui.tableWidgetDemande.horizontalHeader().font().bold()
        self.cur=self.connection.cursor()
        listeParams = []
        SQL = "SELECT d.iddemande, d.numdemande,d.datedemande,d.numdecision,d.datedecision,d.categorie,d.consistance,d.datereconnaissance,d.idfokontany,d.cqe,pd.idcertificat FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid  "
        firstOne = True
        #print SQL
        if self.ui.checkBoxFkt.isChecked():
            SQL="SELECT d.iddemande, d.numdemande,d.datedemande,d.numdecision,d.datedecision,d.categorie,d.consistance,d.datereconnaissance,d.idfokontany , d.cqe ,f.nomfokontany,pd.idcertificat" \
                " FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid" \
                " INNER JOIN fokontany f on d.idfokontany=f.idfokontany"
            if self.ui.checkBoxHameau.isChecked():
                SQL=" SELECT d.iddemande, d.numdemande,d.datedemande,d.numdecision,d.datedecision,d.categorie,d.consistance,d.datereconnaissance,d.idfokontany , d.cqe ,f.nomfokontany,h.idhameau,h.nomhameau,pd.idcertificat" \
                    " FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid " \
                    " INNER JOIN fokontany f on d.idfokontany=f.idfokontany" \
                    " INNER JOIN hameau h on h.idhameau=pd.idhameau"

        if self.ui.checkBoxNumDemande.isChecked():
            numDemandeBrut = str(self.ui.lineEditNumeroDemande.text()).strip()
            numdemandeToQuery = self.prepareNumDemande(numDemandeBrut)
            if numDemandeBrut!="" :
                for numDmd in numdemandeToQuery:
                    #print numDmd
                    if numDmd.find('-') == -1:
                        if firstOne == True:
                            firstOne = False
                            listeParams.append(numDmd)
                            SQL = SQL + " WHERE CAST(TRIM(SPLIT_PART(d.numdemande,'-','4')) as integer) = %s"
                        else:
                            listeParams.append(numDmd)
                            SQL = SQL + " OR CAST(TRIM(SPLIT_PART(d.numdemande,'-','4')) as integer) = %s"
                    else:
                        params = numDmd.split('-')
                        num_debut = params[0]
                        num_fin = params[1]
                        listeParams.append(num_debut)
                        listeParams.append(num_fin)
                        if firstOne == True:
                            firstOne = False
                            SQL = SQL + " WHERE CAST(TRIM(SPLIT_PART(d.numdemande,'-','4')) as integer) BETWEEN %s AND %s"
                        else:
                            SQL = SQL + " OR CAST(TRIM(SPLIT_PART(d.numdemande,'-','4')) as integer) BETWEEN %s AND %s"
        if self.ui.checkBoxFkt.isChecked():
            print "id_fokontany"
            nfokontany=str(self.ui.comboBoxFokontany.currentText())
            listeParams.append(nfokontany)
            print listeParams
            if firstOne == True:
                firstOne = False
                SQL = SQL + " WHERE nomfokontany  = %s "
            else:
                SQL = SQL + " AND nomfokontany = %s "
            print SQL

        if self.ui.checkBoxHameau.isChecked():
            print "id_hameau"
            nhameau = str(self.ui.comboBoxHameau.currentText())
            listeParams.append(nhameau)
            if firstOne == True:
                firstOne = False
                SQL = SQL + " WHERE nomhameau = %s "
            else:
                SQL = SQL + " AND nomhameau = %s "

        if self.ui.checkBoxNumdecision.isChecked():
            numeroDecision = str(self.ui.lineEditNumdecision.text()).strip()
            listeParams.append(numeroDecision)
            if firstOne == True:
                firstOne = False
                SQL = SQL + " WHERE numdecision  = %s "
            else:
                SQL = SQL + " AND numdecision = %s "
            print SQL

        idcommune = globalvars.id_commune
        listeParams.append(idcommune)
        if firstOne == True:
            firstOne = False
            SQL = SQL + " WHERE d.idcommune  = %s "
        else:
            SQL = SQL + " AND d.idcommune = %s "
        print SQL

        print listeParams
        SQL=SQL+" and pd.idcertificat is NULL order by d.iddemande ASC"
        print SQL
        try:
            #print "ato"
            self.cur.execute(SQL,listeParams)
            rows = self.cur.fetchall()
            #print rows
            self.ui.tableWidgetDemande.setRowCount(len(rows))
            for i,r in enumerate(rows):
                if r[1] is None: numdemande = ""
                else: numdemande = str(r[1])
                if r[2] is None: datedemande= ""
                else: datedemande = str(r[2])
                if r[3] is None: numdecision = ""
                else: numdecision = str(r[3])
                if r[4] is None: datedecision = ""
                else: datedecision = str(r[4])
                if r[5] is None: categorie = ""
                else: categorie = str(r[6])
                if r[6] is None: consistance = ""
                else: consistance = str(r[5])
                if r[7] is None: datereconnaissance = ""
                else: datereconnaissance = str(r[7])
                item = QtGui.QTableWidgetItem(True)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(False)
                self.ui.tableWidgetDemande.setItem(i, 0, item)
                self.ui.tableWidgetDemande.setItem(i, 1, QtGui.QTableWidgetItem(str(r[0])))
                self.ui.tableWidgetDemande.setItem(i, 2, QtGui.QTableWidgetItem(numdemande))
                self.ui.tableWidgetDemande.setItem(i, 3, QtGui.QTableWidgetItem(datedemande))
                self.ui.tableWidgetDemande.setItem(i, 4, QtGui.QTableWidgetItem(numdecision))
                self.ui.tableWidgetDemande.setItem(i, 5, QtGui.QTableWidgetItem(datedecision))
                self.ui.tableWidgetDemande.setItem(i, 6, QtGui.QTableWidgetItem(categorie))
                self.ui.tableWidgetDemande.setItem(i, 7, QtGui.QTableWidgetItem(consistance))
                self.ui.tableWidgetDemande.setItem(i, 8, QtGui.QTableWidgetItem(datereconnaissance))
                self.ui.tableWidgetDemande.setItem(i, 9, QtGui.QTableWidgetItem(str(r[8])))
                self.ui.tableWidgetDemande.setItem(i, 10, QtGui.QTableWidgetItem("NON"))
        except Exception as e:
            print(e)
            self.connection.rollback()
            #self.cur.close()

    def prepareNumDemande(self, numDmdBrut):
        numDmdIntermed = numDmdBrut.split(',')
        #print numDmdIntermed
        return numDmdIntermed