# coding: utf-8
import os

from PyQt4 import Qt,QtGui, QtCore
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *


from Etats.ListingDemande import Ui_Dialog
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

import psycopg2.extras

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class ListingDemandeRun(QDialog):
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
        try:
            self.initDB()
            self.initActions()
        except Exception as e:
            print(e)
        self.template=''
        self.orientation='Landscape'

    def initDB(self):
        self.cur = self.connection.cursor()
        print self.cur
        print "vita cur"

    def initActions(self):
        self.ui.checkBoxNumDemande.clicked.connect(self.changeFieldsStatus)
        self.ui.checkBoxNumdecision.clicked.connect(self.changeFieldsStatus)
        self.ui.checkBoxHameau.stateChanged.connect(self.chargeHameau)
        self.ui.checkBoxFkt.stateChanged.connect(self.chargeFKT)
        self.ui.checkBoxFkt.stateChanged.connect(self.chargeFKT)
        self.ui.comboBoxFokontany.currentIndexChanged.connect(self.changeFKT)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercher)
        self.ui.tableWidgetDemande.setColumnWidth(0, 25)
        self.ui.tableWidgetDemande.setColumnWidth(1, 110)
        self.ui.tableWidgetDemande.setColumnWidth(2, 110)
        self.ui.tableWidgetDemande.setColumnWidth(3, 110)
        self.ui.tableWidgetDemande.setColumnWidth(4, 110)
        self.ui.tableWidgetDemande.setColumnWidth(5, 140)
        self.ui.tableWidgetDemande.setColumnWidth(6, 120)
        self.ui.tableWidgetDemande.setColumnWidth(7, 100)
        self.ui.tableWidgetDemande.setColumnWidth(8, 60)
        self.ui.pushButtonExport.clicked.connect(self.exportlisting)
        self.ui.checkBoxCocherTous.stateChanged.connect(self.cocherTout)
        self.ui.tableWidgetDemande.itemClicked.connect(self.handleItemClicked)

    def changeFieldsStatus(self):
        self.ui.lineEditNumeroDemande.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.comboBoxFokontany.setEnabled(self.ui.checkBoxFkt.isChecked())
        self.ui.comboBoxHameau.setEnabled(self.ui.checkBoxHameau.isChecked())
        self.ui.lineEditNumdecision.setEnabled(self.ui.checkBoxNumdecision.isChecked())

    def readByteA(self, idpersonne):
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute("SELECT * FROM blob_personne WHERE idpersonne = %s ",
                        (idpersonne,))
            res = cur.fetchall()
            print res
        except Exception as err:
            print (err)
            self.connection.rollback()

        path1 = None
        path2 = None
        path3 = None
        path4 = None
        path5 = None
        for colon in res:
            # name = colon[1]
            #Contenus
            file_cin_recto = colon['cin_recto']
            file_cin_verso = colon['cin_verso']
            file_signature = colon['signature']
            file_empreinte_d = colon['empreinte_d']
            file_empreinte_g = colon['empreinte_g']
            #print file_empreinte_d
            name_cin_recto = "cin1"+str(idpersonne)
            name_cin_verso = "cin2"+str(idpersonne)
            name_signature = "sin"+str(idpersonne)
            name_empreinte_g = colon['empreinte_g_name']
            name_empreinte_d = colon['empreinte_d_name']
            #Extensions
            ext_cin_recto = colon['cin_recto_type']
            ext_cin_verso = colon['cin_verso_type']
            ext_signature = colon['signature_type']
            ext_empreinte_g = colon['empreinte_g_type']
            ext_empreinte_d = colon['empreinte_d_type']

            #print("Stocker le fichier sur le disque \n")

            #print '-------------------------------------------------------------------------'
            #print tempfile.gettempdir()
            chemin="images/"
            #print chemin
            path = os.getcwd()
            path=path+"\Etats\images"
            #print path
            if file_cin_recto is not None:
                path1 = os.path.join(path, name_cin_recto + "." + ext_cin_recto)
                self.perscin1=name_cin_recto + "." + ext_cin_recto
            if file_cin_verso is not None:
                path2 = os.path.join(path, name_cin_verso + "." + ext_cin_verso)
                self.perscin2=name_cin_verso + "." + ext_cin_verso
            if file_signature is not None:
                path3 = os.path.join(path, name_signature + "." + ext_signature)
                self.perssignature=name_signature+ "." + ext_signature
            if file_empreinte_d is not None:
                path4 = os.path.join(chemin, name_empreinte_d + "." + ext_empreinte_d)
            if file_empreinte_g is not None:
                path5 = os.path.join(path, name_empreinte_g + "." + ext_empreinte_g)
            print ("after path def")

        # Convertir les donnees binaires au format
        # approprie et les ecrire sur le disque dur
        if path1 is not None:
            try:
                with open(path1, 'wb') as myfile:
                    myfile.write(file_cin_recto)
                #print("Le fichier stockees dans: ", path1, "\n")
                #self.showInScene(path1,self.ui.graphicsViewCinRecto)
                self.paths.append(path1)
            except Exception as err:
                print (err)
        if path2 is not None:
            try:
                with open(path2, 'wb') as myfile:
                    myfile.write(file_cin_verso)
                #print("Le fichier stockees dans: ", path2, "\n")
                #self.showInScene(path2, self.ui.graphicsViewCinVerso)
                self.paths.append(path2)
            except Exception as err:
                print (err)
        if path3 is not None:
            try:
                with open(path3, 'wb') as myfile:
                    myfile.write(file_signature)
                #print("Le fichier stockees dans: ", path3, "\n")
                #self.showInScene(path3, self.ui.graphicsViewSignature, True)
                self.paths.append(path3)
            except Exception as err:
                print (err)
        if path4 is not None:
            with open(path4, 'wb') as myfile:
                myfile.write(file_empreinte_d)
            #print("Le fichier stockees dans: ", path4, "\n")
            #self.showInScene(path4, self.ui.graphicsViewEmpreinteD, True)
            self.paths.append(path4)
        if path5 is not None:
            try:
                with open(path5, 'wb') as myfile:
                    myfile.write(file_empreinte_g)
                #print("Le fichier stockees dans: ", path5, "\n")
                #self.showInScene(path5, self.ui.graphicsViewEmpreinteG, True)
                self.paths.append(path5)
            except Exception as err:
                print (err)

        # fermeture de la connexion à la base de données
        cur.close()

    def exportlisting(self):
        self.merger = PdfFileMerger()
        self.pdflisting()
        try:
            dstFinal = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + "Listing Demande.pdf")
            self.merger.write(dstFinal)
            print 'after merger write'
            webbrowser.open(dstFinal)
            QApplication.restoreOverrideCursor()
        except Exception as err:
            print(err)
        self.reset()
        self.ui.pushButtonExport.setEnabled(True)
        self.rechercher()

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

    def pdflisting(self):
        self.ui.progressBarlisting.setValue(1)
        commune = str(Utils.emptyifnull(self.commune, "nomcommune"))
        self.ui.pushButtonExport.setEnabled(False)
        # recuperation ids demande selectionnés
        self.listiddmdselected()
        # select ids demande selectionnés
        self.selectdemande()
        nbdemande = len(self.demandes)
        self.nbrepetition =int(nbdemande)*2
        if int(self.nbrepetition)>100: self.nbrepetition=100
        self.pas=100/self.nbrepetition
        listdemandes = list(self.demandes)
        self.nbdmdaaffiche = 8
        debut = 0
        fin = 8
        debutco=0
        finco=8
        dic = []
        onedemandeur = None
        while debut < nbdemande:
            if fin > nbdemande:
                fin = nbdemande
            rows = []
            allcin=[]

            allcoodemandeur = []
            whithcoodemandeur = True
            countCIN=0
            for i in range(debut, fin):
                self.perssignature = ''
                self.perscin1 = ''
                self.perscin2 = ''
                self.progress()
                numci = str(listdemandes[i].num_cin)
                numcopie = str(listdemandes[i].num_copie)
                numcicopie = numci + " " + numcopie
                idpersonne=listdemandes[i].idx_idpersonne_principale
                #print 'idpersonne'
                print idpersonne
                self.readByteA(idpersonne)
                """
                signature="<img src=""images/"+self.perssignature+" style=""width:100px;height:50px;"">"
                #cins="<img src=""images/"+self.perssignature+" style=""width:100px;height:50px;"">"
                cins='<img src="images/'+self.perscin1+'" style="width:310px;height:200px;"><img src="images/'+ self.perscin2 + '" style="width:310px;height:200px;">'
                #print signature
                print cins"""

                if len(self.perssignature) < 1:
                    signature = ''
                    print '++++++++++++++++++++++++++++++++++++++++tsy misy+++++++++++++++++++++'
                else:
                    signature = "<img src=""images/" + self.perssignature + " style=""width:100px;height:50px;"">"
                # cins="<img src=""images/"+self.perssignature+" style=""width:100px;height:50px;"">"

                print 'self pers no eto------------------------------------------------------------------'
                print len(self.perscin1)
                print len(self.perscin2)
                print '----------FINself pers no eto------------------------------------------------------------------'
                if len(self.perscin1)> 1 and  len(self.perscin2) > 1:
                    print 'miditra ato'
                    cins = '<img src="images/' + self.perscin1 + '" style="width:310px;height:200px;"><img src="images/' + self.perscin2 + '" style="width:310px;height:200px;">'
                else :
                    cins=''
                    countCIN+=1

                print signature
                print cins
                print '////////////////////////////////////////////////////////////////////////////////////////////////////////////////'
                anneeordate=""
                if listdemandes[i].dateNaissance==None or listdemandes[i].dateNaissance=="":
                    anneeordate = listdemandes[i].ne_vers
                else:
                    anneeordate = listdemandes[i].dateNaissance
                rows.append({
                    "idpersonne": str(idpersonne),
                    "nom": str(listdemandes[i].nom).decode('utf-8'),
                    "genre": str(listdemandes[i].genre).decode('utf-8'),
                    "datenaissance": str(anneeordate),
                    "numcicopie": str(numcicopie),
                    "dateci": str(listdemandes[i].datepi),
                    "consistance": str(listdemandes[i].consistance).decode('utf-8'),
                    "codeParcelle": str(listdemandes[i].codeParcelle).decode('utf-8'),
                    "numdemande": str(listdemandes[i].numdemande).decode('utf-8'),
                    "collecteur": str(listdemandes[i].collecteur).decode('utf-8'),
                    "signature": signature,
                })

                allcin.append({
                    "cin": cins,
                })
                print '*****allcin******'
                print allcin
                #print signature
                try:

                    dic = {
                        "$kaominina": commune,
                        "$distrika": str(Utils.emptyifnull(self.district, "nomdistrict")),
                        "$faritra": str(Utils.emptyifnull(self.region, "nomregion")),
                        "$fokontany": str(listdemandes[i].nomfokontany),
                        "$vohitra": str(listdemandes[i].nomhameau),
                        "$datereconnaissance": str(listdemandes[i].dateReconnaissance),
                        "$planchePlof": str(listdemandes[i].codePlanche),
                        "$lieudit": str(listdemandes[i].lieudit),
                        "$collecteur": str(listdemandes[i].collecteur),
                        "$proprietaire": rows,
                        "$allcin": allcin
                    }

                    diccin = {
                        "$allcin": allcin
                    }

                except Exception as err:
                    print err

            try:
                converter = Html2Pdf()
                converter.setOrientation(orientation=self.orientation)
                self.template = 'listingdmd.html'
                src = os.path.dirname(__file__) + "/" + self.template
                dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
                #QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
                #QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
                print "Before Generate"
                converter.generate(html=src, pdf=dst, dictionnary=dic)
                print "After generate"
                # webbrowser.open(dst)
                self.merger.append(dst)
            except Exception as err:
                print(err)

            try:
                if countCIN < 8 :
                    converter = Html2Pdf()
                    converter.setOrientation(orientation=self.orientation)
                    self.template = 'listingcindmd.html'
                    src = os.path.dirname(__file__) + "/" + self.template
                    dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
                    #QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
                    #QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
                    print "Before Generate--------------------------------- listingcindmd"
                    converter.generate(html=src, pdf=dst, dictionnary=diccin)
                    #print "After generate"
                    # webbrowser.open(dst)
                    self.merger.append(dst)
            except Exception as err:
                print(err)

            for path in self.paths:
                try:
                    os.remove(path)
                except Exception as err:
                    print err
            print '-------deuxieme page---------'

            for l in range(debut,fin):
                self.progress()
                print '---------------------------------------print coodemandeur-------------------------------------------------------------'
                coodemandeur = []
                #print '---------------------------------------debut-------------------------------------------------------------'
                try :
                    coodem=""

                    if len(listdemandes[l].demandeurs)>0:
                        demandeurs = listdemandes[l].demandeurs
                    else:
                        demandeurs = []
                    print  'eto ny demandeurs '
                    print len(demandeurs)
                    for j, onedemandeur in enumerate(demandeurs):
                        if onedemandeur['datenaissance'] == None or onedemandeur['datenaissance'] == "":
                            anneeordate = onedemandeur['ne_vers']
                        else:
                            anneeordate = onedemandeur['datenaissance']
                        represtant = str(onedemandeur['representant'])
                        if represtant == 'true': represtant = True
                        else: represtant = False
                        if represtant == False:
                            self.readByteA(onedemandeur['idpersonne'])
                            signaturecoo = "<img src=""images/" + self.perssignature + " style=""width:100px;height:50px;"">"
                            genre=''
                            if str(onedemandeur['genre'])=="feminin": genre="V"
                            else:  genre="L"
                            coodemandeur.append({
                                "idpersonne": str(onedemandeur['idpersonne']).decode('utf-8'),
                                "nom": str(onedemandeur['nom']).decode('utf-8'),
                                "genre": str(genre),
                                "datenaissance": str(anneeordate),
                                "numci": str(onedemandeur['numci']),
                                "dateci": str(onedemandeur['dateci']),
                                "lieuci": str(onedemandeur['lieuci']),
                                "numcopie": str(onedemandeur['numacte']),
                                "datecopie": str(onedemandeur['dateacte']),
                                "lieucopie": str(onedemandeur['lieuacte']),
                                "pere": str(onedemandeur['nompere']).decode('utf-8'),
                                "mere": str(onedemandeur['nommere']).decode('utf-8'),
                                "conjoint": str(onedemandeur['conjoint']).decode('utf-8'),
                                "adresse": str(onedemandeur['adresse']).decode('utf-8'),
                                "numdemande": str(listdemandes[l].numdemande).decode('utf-8'),
                                "codeParcelle": str(listdemandes[l].codeParcelle).decode('utf-8'),
                                "datereconnaissance": str(listdemandes[l].dateReconnaissance),
                                "signature": signaturecoo,
                            })
                except Exception as err:
                    print err

                #print  'eto ny coodemandeur '
                #print coodemandeur
                #print listdemandes[l].numdemande
                #print '-----------------------------------------fin-----------------------------------------------------------'
                try:

                    dicsi = ({
                        "$kaominina": commune,
                        "$distrika": str(Utils.emptyifnull(self.district, "nomdistrict")),
                        "$faritra": str(Utils.emptyifnull(self.region, "nomregion")),
                        "$fokontany": str(listdemandes[l].nomfokontany),
                        "$vohitra": str(listdemandes[l].nomhameau),
                        "$planchePlof":  str(listdemandes[l].codePlanche),
                        "$lieudit": str(listdemandes[l].lieudit),
                        "$numdemande": str(listdemandes[l].numdemande),
                        "$codeParcelle": str(listdemandes[l].codeParcelle),
                        "$datereconnaissance": str(listdemandes[l].dateReconnaissance),
                        "$coodemandeur": coodemandeur
                    })
                    #print 'dicsi'
                    #print dicsi
                except Exception as err:
                    print err
                if len(coodemandeur)>0:
                    try:
                        converter = Html2Pdf()
                        converter.setOrientation(orientation=self.orientation)
                        self.template = 'listingcoodmd.html'
                        src = os.path.dirname(__file__) + "/" + self.template
                        dst = os.path.join(tempfile.gettempdir(), str(randint(10000, 99999)) + "-" + self.template + ".pdf")
                        #QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
                        print "Before Generate"
                        converter.generate(html=src, pdf=dst, dictionnary=dicsi)
                        print "After generate"
                        self.merger.append(dst)
                    except Exception as err:
                            print(err)
            debut = fin
            fin = (debut + self.nbdmdaaffiche)
        QApplication.restoreOverrideCursor()

    def selectdemande(self):
        self.demandes=[]
        #print 'tonga ato selectdemande'
        alls = tuple(self.alliddmdselected)
        withLimite = False
        wheres="demande.iddemande in "+str(alls)+" order by demande.iddemande asc "
        #print wheres
        page=2
        #print "metadata"
        #print wheres
        globalvars.LimitSelect=50
        #print alls
        try:
            self.demandes= Demande.select_dmd(self.connection, self.metadata, wheres, 2, False)
        except Exception as e:
            print(e)
            print 'errur ato selectdemande'
            QMessageBox.critical(self, "Une exeption",
                                 "Erreur lors de la récupération des demandes dans la base de données. veuillez contacter votre administrateur!")


    def listiddmdselected(self):
        self.allrowdmdselected = []
        self.alliddmdselected = []
        for j in range(self.ui.tableWidgetDemande.rowCount()):
            items = self.ui.tableWidgetDemande.item(j, 0)
            if items.checkState() == QtCore.Qt.Checked:
                self.allrowdmdselected.append(j)
                self.alliddmdselected.append(int(self.ui.tableWidgetDemande.item(j, 1).text()))
        print self.alliddmdselected

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
        print ("ato")
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
        self.ui.tableWidgetDemande.setRowCount(0)
        self.ui.checkBoxCocherTous.setChecked(False)
        #self.ui.tableWidgetDemande.horizontalHeader().font().bold()
        self.cur=self.connection.cursor()
        listeParams = []
        SQL = "SELECT d.iddemande, d.numdemande,d.numdecision,d.datedecision, d.debut_affichage, d.fin_affichage ,d.datereconnaissance, d.cqe FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid  "
        firstOne = True
        #print SQL
        if self.ui.checkBoxFkt.isChecked():
            SQL="SELECT d.iddemande, d.numdemande,d.numdecision,d.datedecision, d.debut_affichage, d.fin_affichage ,d.datereconnaissance, d.cqe ,f.idfokontany ,f.nomfokontany" \
                " FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid" \
                " INNER JOIN fokontany f on d.idfokontany=f.idfokontany"
            if self.ui.checkBoxHameau.isChecked():
                SQL=" SELECT d.iddemande, d.numdemande,d.numdecision,d.datedecision, d.debut_affichage,d.datereconnaissance, d.cqe , d.fin_affichage,f.idfokontany ,f.nomfokontany,h.idhameau,h.nomhameau" \
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
            nfokontany=str(self.ui.comboBoxFokontany.currentText())
            listeParams.append(nfokontany)
            if firstOne == True:
                firstOne = False
                SQL = SQL + " WHERE nomfokontany  = %s "
            else:
                SQL = SQL + " AND nomfokontany = %s "


        if self.ui.checkBoxHameau.isChecked():
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


        idcommune = globalvars.id_commune
        listeParams.append(idcommune)
        if firstOne == True:
            firstOne = False
            SQL = SQL + " WHERE d.idcommune  = %s "
        else:
            SQL = SQL + " AND d.idcommune = %s "



        SQL=SQL+" order by d.iddemande ASC"

        try:
            self.cur.execute(SQL,listeParams)
            rows = self.cur.fetchall()
            self.ui.tableWidgetDemande.setRowCount(len(rows))
            for i,r in enumerate(rows):
                if r[1] is None: numdemande = ""
                else: numdemande = str(r[1])
                if r[2] is None: numdecision = ""
                else: numdecision = str(r[2])
                if r[3] is None: datedecision = ""
                else: datedecision = str(r[3])
                if r[4] is None: datedebutaffichage = ""
                else: datedebutaffichage = str(r[4])
                if r[5] is None: datefinaffichage = ""
                else: datefinaffichage = str(r[5])
                if r[6] is None: datereconnaissance = ""
                else: datereconnaissance = str(r[6])
                item = QtGui.QTableWidgetItem(True)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(False)
                self.ui.tableWidgetDemande.setItem(i, 0, item)
                self.ui.tableWidgetDemande.setItem(i, 1, QtGui.QTableWidgetItem(str(r[0])))
                self.ui.tableWidgetDemande.setItem(i, 2, QtGui.QTableWidgetItem(numdemande))
                self.ui.tableWidgetDemande.setItem(i, 3, QtGui.QTableWidgetItem(numdecision))
                self.ui.tableWidgetDemande.setItem(i, 4, QtGui.QTableWidgetItem(datedecision))
                self.ui.tableWidgetDemande.setItem(i, 5, QtGui.QTableWidgetItem(datedebutaffichage))
                self.ui.tableWidgetDemande.setItem(i, 6, QtGui.QTableWidgetItem(datefinaffichage))
                self.ui.tableWidgetDemande.setItem(i, 7, QtGui.QTableWidgetItem(datereconnaissance))
                self.ui.tableWidgetDemande.setItem(i, 8, QtGui.QTableWidgetItem("NON"))
        except Exception as e:
            print(e)
            self.connection.rollback()
            #self.cur.close()

    def prepareNumDemande(self, numDmdBrut):
        numDmdIntermed = numDmdBrut.split(',')
        #print numDmdIntermed
        return numDmdIntermed
