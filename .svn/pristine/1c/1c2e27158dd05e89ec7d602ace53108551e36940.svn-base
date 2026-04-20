# -*- coding: utf-8 -*-
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
import globalvars
import psycopg2
from psycopg2.extensions import *

from .InformationFiscale import Ui_Dialog

from AreaConvert import AreaConvert


class InformationFiscaleRun(QDialog):
    def __init__(self, connection, parent, edition = None, isFiscalisation = False):
        QDialog.__init__(self)
        print "constructeur Infofisc init "

        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tableWidget.setSelectionBehavior(1)
        self.ui.tableWidget.setSelectionMode(1)
        self.ui.tableWidget_2.setSelectionMode(1)
        self.ui.tableWidget_2.setSelectionBehavior(1)
        self.initMasks()
        self.ui.numeroDemandeLineEdit.setReadOnly(True)
        self.ui.numeroCertificatLineEdit.setReadOnly(True)
        self.ui.radioSRI.setChecked(True)
        self.ui.radioAucun.setChecked(True)
        self.ui.lineEditNom.setReadOnly(True)
        self.ui.lineEditPrenom.setReadOnly(True)
        self.ui.lineEditAdresse.setReadOnly(True)
        self.ui.dateEditNaissance.setReadOnly(True)
        self.ui.lineEditLieuNaissance.setReadOnly(True)
        self.ui.lineEditSurfaceM2.setReadOnly(True)
        self.ui.LineEditSutfaceHa.setReadOnly(True)
        self.ui.CIN.setDisabled(True)
        self.codesFokontany = []
        self.registry = parent.registry
        #self.ui.label_16.hide()
        self.ui.label_17.hide()
        self.connection = connection
        self.isFiscalisation = isFiscalisation
        self.parent = parent
        self.areaHa = ""
        self.areaSqm = 0
        self.initDB()
        self.idparcelle = parent.idparcelle
        self.canvas = parent.canvas
        self.limitesParcelle = []
        self.infosBatiments = []
        self.idPointCardinaux = []
        self.idCategories = []
        self.idCategoriesBatiment = []
        self.idConsistances = []
        self.singleIdConsistance = None
        self.idConsistancesBatiment = []
        self.idFokontany = []
        self.singleIdFokontany = None
        self.idHameau = []
        self.singleIdHameau = None
        self.idConsorts = None
        self.codesHameau = []
        self.edition = edition
        self.lastId = None
        self.has_data = None
        self.etatConversion = None
        self.idContribuable = None
        if self.idContribuable == None:
            self.ui.btnConsorts.setEnabled(False)
        self.readInputSenderName = None

        from Personnes.ListePersonnePqueRun import ListePersonnePqueRun
        self.listePersonne = ListePersonnePqueRun(self.connection)

        print "fin constructeur infofisc"
        from .VoirListeContribuableRun import VoirListeContribuableRun
        self.listeContribuable = VoirListeContribuableRun(self.connection)
        self.ui.radioSRA.hide()
        self.ui.radioSRI.hide()

        from Fiplof.Saisie.EditionConsortsRun import EditionConsorts
        self.listeConsorts = EditionConsorts(self.connection, self.idparcelle, 2, self)

        self.setModal(True)
        self.initDB()

        self.ui.comboConsistanceParcelle.setVisible(False)
        self.ui.consistanceLabel_4.setVisible(False)
        self.ui.comboConsistanceBatiment.setVisible(False)
        self.ui.consistanceLabel_3.setVisible(False)

        self.initActions()
        self.ui.tabWidget.setCurrentIndex(0)
        self.fillComboCategorieParcelle()
        self.fillComboCategorieBatiment()
        self.fillComboConsistance()
        self.fillComboPosition()
        #self.ui.convertirDemande.hide()

        if isFiscalisation:
            self.ui.convertirDemande.hide()
            self.traiterContribuableCF()
            self.updateFields()

        self.fillTerritoire()
        self.fillHameau()
        if edition is None:
            pass
            #self.fillLineEditcode()
        if edition is not None:
            self.updateFields()

        self.getSurface()
        #self.fillLineEditcode()
        self.fillComboClasse()


        #self.idcontribuable

    def initActions(self):
        self.ui.classeLabel_2.setVisible(False)
        self.ui.comboBoxClasse.hide()
        self.ui.classeLabel_4.setVisible(False)
        self.ui.comboBoxClasseBatiment.hide()
        self.ui.radioButton_Surface.setChecked(True)
        self.ui.radioButton_SurfaceBatiment.setChecked(True)
        self.ui.btnConsorts.clicked.connect(self.ouvrirListeConsorts)
        #self.ui.btnRechercher.clicked.connect(self.ouvrirListeContribuable)
        self.ui.btnRechercher.clicked.connect(self.ouvrirListePersonne)
        self.ui.btnAnnuler.clicked.connect(self.close)
        self.listeConsorts.ui.pushButton_4.clicked.connect(self.enregConsorts)
        #self.listeContribuable.ui.btnSelectionner.clicked.connect(self.getContribuableInfo)
        self.listePersonne.ui.btnSelectionner.clicked.connect(self.setIdContribuable)
        self.ui.btnAjouter2.clicked.connect(self.addLimite)
        self.ui.btnSupprimer2.clicked.connect(self.deleteLimite)

        self.ui.btnAjouter.clicked.connect(self.addOneBat)
        self.ui.btnSupprimer.clicked.connect(self.deleteOneBat)
        self.ui.btnEnregistrer.clicked.connect(self.readInput)
        #if self.edition is None:
        #self.ui.comboFokontany.activated.connect(self.fillLineEditcode)
        #self.ui.comboHameau.activated.connect(self.fillLineEditcode)
        self.ui.comboFokontany.activated.connect(self.fillHameau)
        self.ui.convertirDemande.clicked.connect(self.ouvrirDemande)
        #self.ui.lineEditNumParcelle.textEdited.connect(self.fillLineEditcode)
        #self.ui.lineEditNumParcelle.textChanged.connect(self.fillLineEditcode)
        self.ui.radioButton_Venale.clicked.connect(self.inputVenale)
        self.ui.radioButton_Surface.clicked.connect(self.inputSurface)
        self.ui.radioButton_Classe.clicked.connect(self.inputClasse)
        self.ui.radioButton_LocativeBatiment.clicked.connect(self.inputLocativeBatiment)
        self.ui.radioButton_SurfaceBatiment.clicked.connect(self.inputSurfaceBatiment)
        self.ui.radioButton_ClasseBatiment.clicked.connect(self.inputClasseBatiment)

    def inputSurface(self):
        self.ui.comboBoxClasse.hide()
        self.ui.classeLabel_2.setVisible(False)

    def inputClasse(self):
        self.ui.classeLabel_2.setVisible(True)
        self.ui.comboBoxClasse.setVisible(True)

    def inputVenale(self):
        self.ui.classeLabel_2.setVisible(False)
        self.ui.comboBoxClasse.hide()

    def inputSurfaceBatiment(self):
        self.ui.comboBoxClasseBatiment.hide()
        self.ui.classeLabel_4.setVisible(False)

    def inputClasseBatiment(self):
        self.ui.classeLabel_4.setVisible(True)
        self.ui.comboBoxClasseBatiment.setVisible(True)

    def inputLocativeBatiment(self):
        self.ui.classeLabel_4.setVisible(False)
        self.ui.comboBoxClasseBatiment.hide()

    def enregConsorts(self):
        self.idConsorts = self.listeConsorts.getProprioPhysique()
        print "ids des consorts = " + str(self.idConsorts)
        self.listeConsorts.close()
        #self.idPersMorale = self.proprietaires.getProprioMorale()

    def ouvrirListeConsorts(self):
        self.listeConsorts.exec_()

    def ouvrirListeContribuable(self):
        self.listeContribuable.isFromConsort()
        self.listeContribuable.exec_()

    def setIdContribuable(self):
        self.idContribuable = self.listePersonne.getIdPersonne()
        print "id contribuable = " + str(self.idContribuable)
        if self.idContribuable is not None:
            self.getContribuableById(self.idContribuable)
        self.listePersonne.close()

    def ouvrirListePersonne(self):
        self.listePersonne.exec_()

    #def getContribuableInfo(self):
        #idContribuable = self.listeContribuable.selectContribuable()
        #self.idContribuable =  idContribuable
        #self.getContribuableById(idContribuable)
        #self.listeContribuable.close()

    def initDB(self):
        self.cur = self.connection.cursor()

    def getContribuableById(self, id):
        self.ui.btnConsorts.setEnabled(True)
        self.listeConsorts.setIdContribuableToPass(self.idContribuable)
        self.listeConsorts.proprietairePhysiques()
        self.cur.execute("SELECT * FROM personne WHERE idpersonne = %s", (id,))
        data = self.cur.fetchone()
        print data
        self.fillFields(data)

    def fillFields(self, data):
        self.idContribuable = data[0]
        if data[1]:
            self.ui.lineEditNom.setText(data[1])
        if data[2]:
            self.ui.lineEditPrenom.setText(data[2])
        if data[13]:
            self.ui.lineEditAdresse.setText(data[13])
        if data[4]:
            self.ui.dateEditNaissance.setDate(data[4])
        if data[6]:
            self.ui.lineEditLieuNaissance.setText(data[6])
        if data[7]:
            self.ui.CIN.setCurrentIndex(0)
            self.ui.lineEditCIN1.setText(data[7][0:3])
            self.ui.lineEditCIN2.setText(data[7][3:6])
            self.ui.lineEditCIN3.setText(data[7][6:9])
            self.ui.lineEditCIN4.setText(data[7][9:len(data[7])])
            if data[8]:
                self.ui.dateEditCIN.setDate(data[8])
            if data[9]:
                self.ui.lineEditLieuCIN.setText(data[9])
        if data[10]:
            self.ui.CIN.setCurrentIndex(1)
            self.ui.lineEditNumActeNaissance.setText(data[10])
            if data[11]:
                self.ui.dateEditActeNaissance.setDate(data[11])
            if data[12]:
                self.ui.lineEditLieuActeNaissance.setText(data[12])
        if data[3]:
            if data[3] == "masculin":
                self.ui.radioSexeHomme.setChecked(True)
            if data[3] == "feminin":
                self.ui.radioSexeFemme.setChecked(True)

    def fillComboCategorieParcelle(self):
        self.idCategories[:] = []
        self.ui.comboCategorieParcelle.clear()
        self.cur.execute("SELECT * FROM categorie where typeimposition='ift' order by idcategorie ASC ")
        results = self.cur.fetchall()
        i=1
        for result in results:
            categorie="Catégorie "+ str(i)
            self.ui.comboCategorieParcelle.addItem(unicode(categorie+":"+result[1]), result[0])
            self.idCategories.append(result[0])
            i=i+1

    def fillComboCategorieBatiment(self):
        self.idCategoriesBatiment[:] = []
        self.ui.comboCategorieBatiment.clear()
        self.cur.execute("SELECT * FROM categorie where typeimposition='ifpb' order by idcategorie ASC")
        results = self.cur.fetchall()
        i = 1
        for result in results:
            categorie = "Catégorie " + str(i)
            self.ui.comboCategorieBatiment.addItem(unicode(categorie+":"+result[1]), result[0])
            self.idCategoriesBatiment.append(result[0])
            i = i + 1

    def fillComboConsistance(self):
        self.idConsistances[:] = []
        self.idConsistancesBatiment[:] = []
        self.ui.comboConsistanceParcelle.clear()
        self.ui.comboConsistanceBatiment.clear()
        self.cur.execute("SELECT * FROM consistance")
        results = self.cur.fetchall()
        for result in results:
            self.ui.comboConsistanceParcelle.addItem(str(result[1]), result[0])
            self.idConsistances.append(result[0])

        self.cur.execute("SELECT * FROM consistance_batiment")
        results = self.cur.fetchall()
        for result in results:
            self.ui.comboConsistanceBatiment.addItem(str(result[1]), result[0])
            self.idConsistancesBatiment.append(result[0])

    def fillComboPosition(self):
        self.ui.positionComboBox.clear()
        self.cur.execute("SELECT * FROM pointscardinaux")
        results = self.cur.fetchall()
        for result in results:
            self.idPointCardinaux.append(result[0])
            self.ui.positionComboBox.addItem(str(result[1]), result[0])

    def fillTerritoire(self):
        self.ui.comboFokontany.clear()
        self.codesFokontany[:] = []
        self.idFokontany[:] = []
        # Fokontany
        try:
            self.cur.execute("SELECT nomfokontany, idfokontany, codefokontany FROM fokontany WHERE idcommune = %s",
                             (globalvars.id_commune,))
            fkts = self.cur.fetchall()
            for fkt in fkts:
                self.ui.comboFokontany.addItem(fkt[0])
                self.idFokontany.append(fkt[1])
                self.codesFokontany.append(fkt[2])
        except StandardError as e:
            print e

        self.fillHameau()
        self.lastId = self.getLastInsert()

    def getLastInsert(self):
        self.cur.execute("SELECT MAX(gid) FROM parcelle_d")
        max = self.cur.fetchone()
        if max is not None:
            return max[0]
        else:
            return 0

    def fillHameau(self):
        self.idHameau[:] = []
        self.ui.comboHameau.clear()
        self.codesHameau[:] = []
        idFokontany = self.idFokontany[self.ui.comboFokontany.currentIndex()]
        try:
            self.cur.execute("SELECT idhameau, codehameau, nomhameau FROM hameau WHERE idfokontany = %s", (idFokontany,))
            hmx = self.cur.fetchall()
            for hm in hmx:
                self.idHameau.append(hm[0])
                self.ui.comboHameau.addItem(hm[2])
                self.codesHameau.append(hm[1])
        except StandardError as e:
            print e


    def fillTablePosition(self):
        limiteparcelle = []
        limiteparcelle.append(self.idPointCardinaux[self.ui.positionComboBox.currentIndex()])
        #self.limitesParcelle.append(self.ui.positionComboBox.itemData(1))
        #print self.idsPositions
        rowPosition = self.ui.tableWidget_2.rowCount()
        self.ui.tableWidget_2.insertRow(rowPosition)
        # idpersonnes.append(data[i][0])
        #self.listeIdConsorts.append(self.currData[0])
        #print self.listeIdConsorts
        if self.ui.descriptionLineEdit.text() != "":
            self.ui.tableWidget_2.setItem(rowPosition, 0, QTableWidgetItem(self.ui.positionComboBox.currentText()))
            self.ui.tableWidget_2.setItem(rowPosition, 1, QTableWidgetItem(self.ui.descriptionLineEdit.text()))
            limiteparcelle.append(unicode(self.ui.descriptionLineEdit.text()).encode('utf-8'))
            self.limitesParcelle.append(limiteparcelle)

        print self.limitesParcelle

        self.ui.descriptionLineEdit.clear()

    def fillTableBatiment(self):
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        infoBatiment = []
        infoBatiment.append(unicode(self.ui.lineEditCode.text()).encode('utf-8'))
        infoBatiment.append(self.idCategoriesBatiment[self.ui.comboCategorieBatiment.currentIndex()])
        infoBatiment.append(self.idConsistancesBatiment[self.ui.comboConsistanceBatiment.currentIndex()])
        if self.ui.surfaceLineEdit_3.text() == "":
            infoBatiment.append(0)
        else:
            infoBatiment.append(float(self.ui.surfaceLineEdit_3.text()))
        if self.ui.nombrePiCesLineEdit_2.text() == "":
            infoBatiment.append(0)
        else:
            infoBatiment.append(int(self.ui.nombrePiCesLineEdit_2.text()))
        self.ui.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(self.ui.lineEditCode.text()))
        self.ui.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(self.ui.comboCategorieBatiment.currentText()))
        self.ui.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(self.ui.comboConsistanceBatiment.currentText()))
        self.ui.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(self.ui.surfaceLineEdit_3.text()))
        self.ui.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(self.ui.nombrePiCesLineEdit_2.text()))
        #self.ui.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(self.ui.ra.currentText()))
        #self.ui.tableWidget.setItem(rowPosition, 6, QTableWidgetItem(self.ui.nombrePiCesLineEdit_2.text()))

        self.ui.lineEditCode.clear()
        self.ui.surfaceLineEdit_3.clear()
        self.ui.nombrePiCesLineEdit_2.clear()
        self.ui.comboConsistanceBatiment.setCurrentIndex(0)
        self.ui.comboCategorieBatiment.setCurrentIndex(0)

        self.infosBatiments.append(infoBatiment)
        print self.infosBatiments

    def readInput(self, edition = None):
        self.readInputSenderName = str(self.sender().objectName())
        data = {}
        if str(self.ui.lineEditCodeParcelle.text()).strip() == "":
            QMessageBox.critical(None, "Erreur", "Le champ code de la parcelle est obligatoire")
            return
        if str(self.ui.lineEditNumParcelle.text()).strip() == "":
            QMessageBox.critical(None, "Erreur", "Le champ numero de la parcelle est obligatoire")
            return
        if self.ui.comboCategorieParcelle.currentIndex() == -1:
            QMessageBox.critical(self, "Erreur", u"Veuillez paramétrer les catégories fiscalité")
            return
        else:
            data['categorieparcelle'] = self.idCategories[self.ui.comboCategorieParcelle.currentIndex()]
            if self.ui.radioSRI.isChecked():
                data['srisra'] = "sri"
            elif self.ui.radioSRA.isChecked():
                data['srisra'] = "sra"

            #data['etatparcelle'] = 0
            if self.ui.radioAucun.isChecked():
                data['etatparcelle_d'] = int(0)
            elif self.ui.radioTitree.isChecked():
                data['etatparcelle_d'] = int(1)
            elif self.ui.radioCadastree.isChecked():
                data['etatparcelle_d'] = int(2)
            elif self.ui.radioCertifiee.isChecked():
                data['etatparcelle_d'] = int(3)

            if self.ui.comboConsistanceParcelle.currentIndex() != -1:
                data['consistance'] = str(self.ui.comboConsistanceParcelle.currentText())
            else:
                data['consistance'] = ""
            #if self.ui.comboConsistanceBatiment.currentIndex() != -1:
                #data['consistancebat'] = self.ui.comboConsistanceBatiment.itemData()

            if self.ui.lineEditCodeParcelle.text() != "":
                data['code'] = unicode(self.ui.lineEditCodeParcelle.text()).encode('utf-8')
            data['obs'] = unicode(self.ui.textEditObservation.toPlainText()).encode('utf-8')

            if self.ui.radioButton_Surface.isChecked():
                data['fi_forfait']='surface'
            if self.ui.radioButton_Classe.isChecked():
                data['fi_forfait'] = 'classe'
            if self.ui.radioButton_Venale.isChecked():
                data['fi_forfait'] = 'valeur_venale'

            if self.ui.radioTitree.isChecked():
                data['numtitre'] = unicode(self.ui.lineEditNumParcelle.text()).encode('utf-8')
                self.writeData(data, 0, edition)
            elif self.ui.radioCadastree.isChecked() or self.ui.radioAucun.isChecked():
                data['numparcelle'] = unicode(self.ui.lineEditNumParcelle.text()).encode('utf-8')
                self.writeData(data, 1, edition)
            elif self.ui.radioCertifiee.isChecked():
                data['numcertificat'] = unicode(self.ui.lineEditNumParcelle.text()).encode('utf-8')
                self.writeData(data, 2, edition)


    def writeData(self, data, value, edition = None):
        #idClasse = None
        idClasse = self.ui.comboBoxClasse.itemData(self.ui.comboBoxClasse.currentIndex()).toInt()[0]
        idHameauC = None
        if self.ui.comboHameau.currentIndex() != -1:
            idHameauC = self.idHameau[self.ui.comboHameau.currentIndex()]
        else:
            QMessageBox.critical(self, "Erreur sur hameau", u"Veuillez séléctionner un Hameau ")
        if idHameauC is not None:
            try:
                if value == 0: # Parcelle titree
                    self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idhameau = %s, has_data = TRUE, srisraparcelle = %s, etatparcelle_d = %s,"
                                     " consistance = %s, idclasse = %s,fi_forfait= %s, estfiscalite = 1 "
                                     "WHERE gid = %s",(data['numtitre'], data['code'], data['categorieparcelle'],idHameauC, data['srisra'], data['etatparcelle_d'],data['consistance'], idClasse,data['fi_forfait'], self.idparcelle))
                    self.connection.commit()
                elif value == 1: # parcelle cadastree
                    self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idhameau = %s, has_data = TRUE, srisraparcelle = %s, etatparcelle_d = %s, "
                                     "consistance = %s, idclasse = %s,fi_forfait= %s, estfiscalite = 1 "
                                     " WHERE gid = %s ",(data['numparcelle'], data['code'], data['categorieparcelle'],idHameauC, data['srisra'], data['etatparcelle_d'],data['consistance'], idClasse,data['fi_forfait'], self.idparcelle))
                    self.connection.commit()
                elif value == 2: # parcelle certifiee
                    self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idhameau = %s, has_data = TRUE, srisraparcelle = %s, etatparcelle_d = %s, consistance = %s,"
                                     " idclasse = %s,fi_forfait= %s, estfiscalite = 1 "
                                     " WHERE gid = %s",(data['numcertificat'], data['code'], data['categorieparcelle'], idHameauC, data['srisra'], data['etatparcelle_d'], data['consistance'], idClasse,data['fi_forfait'], self.idparcelle))
                    self.connection.commit()
                #print "SAVING PARCELLE"
                consortsDeleted = False
                try:
                    #print "TAKING CARE OF THE PERSONS"
                    if self.idConsorts is not None:
                        self.cur.execute("DELETE FROM contribuables_parcelle WHERE idparcelle = %s ", (self.idparcelle,))
                        self.connection.commit()
                        consortsDeleted = True

                        for idcons in self.idConsorts:
                            print "id consort = " + str(idcons)
                            try:
                                self.cur.execute("INSERT INTO contribuables_parcelle (idpersonne, idparcelle, contribuable) VALUES (%s, %s, %s)", (idcons, self.idparcelle, False))
                                self.connection.commit()
                            except StandardError as e:
                                print(e)
                                self.connection.rollback()
                    try:
                        if self.idContribuable is not None:
                            print "id contribuable = " + str(self.idContribuable)
                            self.cur.execute("INSERT INTO contribuables_parcelle (idpersonne, idparcelle, contribuable) "
                                                 "VALUES (%s, %s, %s)",(self.idContribuable, self.idparcelle, True) )
                            self.connection.commit()
                    except psycopg2.Error as e:
                        print(e)
                        if e.pgcode == "2305":
                            try:
                                self.cur.execute("UPDATE contribuables_parcelle idpersonne = %s "
                                             "WHERE idparcelle = %s AND contribuable = %s",
                                             (self.idContribuable, self.idparcelle, True))
                                self.connection.commit()
                            except StandardError as e:
                                print (e)
                        self.connection.rollback()

                except StandardError as e:
                    print(e)
                    self.connection.rollback()



                #i = 0
                #while i < len(self.infosBatiments):
                    #try:
                        #self.cur.execute(
                            #"INSERT INTO public.batiment (codebatiment, idparcelle, idconsistance, surfacebatiment, nbpiecebatiment) VALUES (%s, %s, %s, %s, %s)",
                            #(self.infosBatiments[i][0], self.idparcelle, self.infosBatiments[i][2],
                            # self.infosBatiments[i][3], self.infosBatiments[i][4]))
                        #self.connection.commit()
                    #except StandardError as e:
                        #print "Info batiment " + str(e)
                        #self.connection.rollback()

                    #i = i + 1

                #i = 0
                #while i < len(self.limitesParcelle):
                    #try:
                        #self.cur.execute(
                            #"INSERT INTO public.limitesparcelle (idpointscardinaux, idparcelle, description) VALUES (%s, %s, %s)",
                            #(self.limitesParcelle[i][0], self.idparcelle, self.limitesParcelle[i][1]))
                        #self.connection.commit()
                    #except StandardError as e:
                        #print "Limites parcelles " + str(e)
                        #self.connection.rollback()
                    #i = i + 1

                #msgBox = QMessageBox()
                #msgBox.setText("Enregistrement de la parcelle fiplof reussi")
                #msgBox.show()
                #msgBox.exec_()
                if edition is None:
                    QMessageBox.information(self, u"Parcelle avec données", "Enregistrement de la parcelle reussi")
                    self.close()
                if edition is not None and self.readInputSenderName == "btnEnregistrer":
                    QMessageBox.information(self, u"Parcelle avec données", "Enregistrement de la parcelle reussi")
                    self.updateFields()
                self.refreshCanvas()
            except StandardError as e:
                print "Enregistrement parcelle " + str(e)
                if str(e).__contains__('duplicate key value'):
                    QMessageBox.critical(None, "Erreur", u"Code parcelle déjà existant dans la commune.")
                else:
                    QMessageBox.critical(None, "Erreur", u"Erreur lors de l'enregistrement des informations fiscales.")
                print(e)
                self.connection.rollback()


        #else:
            #try:
                #if value == 0: # Parcelle titree
                    #self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idcontribuable = %s, has_data = TRUE WHERE gid = %s",(data['numtitre'], data['code'], data['categorieparcelle'], self.idContribuable, self.idparcelle))
                    #self.connection.commit()
                #elif value == 1: # parcelle cadastree
                    #self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idcontribuable = %s, has_data = TRUE WHERE gid = %s",(data['numparcelle'], data['code'], data['categorieparcelle'], self.idContribuable, self.idparcelle))
                    #self.connection.commit()
                #elif value == 2: # parcelle certifiee
                    #self.cur.execute("UPDATE parcelle_d SET numero = %s, codeparcelle = %s, idcategorie = %s, idcontribuable = %s, has_data = TRUE WHERE gid = %s",(data['numcertificat'], data['code'], data['categorieparcelle'], self.idContribuable, self.idparcelle))
                    #self.connection.commit()
            #except StandardError as e:
                #print "Enregistrement parcelle " + str(e)
                #self.connection.rollback()



    def refreshCanvas(self):

        for layer in self.canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()

        self.canvas.refresh()

    def getSurface(self):
        SQL = "SELECT ST_Area(geom) FROM parcelle_d WHERE gid = %s;"
        param = (self.idparcelle,)
        try:
            self.cur.execute(SQL, param)
            data = self.cur.fetchone()
            print "affichage de la surface"
            ac = AreaConvert()
            self.areaSqm = round(data[0], 2)
            Area = ac.convertArea(data[0], 'sqmeter', 'Ha')
            print "fin affichage"
            self.areaHa = str(Area['Ha'])+ " Ha " + str(Area['a']) + " a " + str(Area['Ca']) + " Ca "
            self.areaHa_d = round(ac.convertAreaToHa(data[0]), 2)
            print self.areaHa
            self.ui.lineEditSurfaceM2.setText(str(self.areaSqm))
            self.ui.LineEditSutfaceHa.setText(self.areaHa)
            print "Apres affichage"
        except StandardError as e:
            print e

    def initExtraData(self, data, fromCertificat = None):
        if fromCertificat is not None:
            if fromCertificat == 1:
                self.ui.radioCertifiee.setChecked(True)
                self.ui.lineEditNumParcelle.setText(str(data[0]).strip())
                self.ui.numeroCertificatLineEdit.setText(str(data[0]).strip())
                self.ui.numeroDemandeLineEdit.setText(str(data[1]).strip())
                self.getAllLimites(data[2])


    def getAllLimites(self, idCertificat):
        self.cur.execute("select pc.idpointscardinaux, pc.position, lp.description "
                         "from pointscardinaux pc, limitesparcelle lp, parcelle_d pd "
                         "WHERE lp.idparcelle = pd.gid "
                         "and lp.idpointscardinaux = pc.idpointscardinaux "
                         "and pd.idcertificat = %s", (idCertificat,))
        results = self.cur.fetchall()
        if results is not None:
            self.showInTable(results)

    def showInTable(self, data):
        self.ui.tableWidget_2.setRowCount(0)
        i = 0
        while i < len(data):
            rowPosition = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(rowPosition)
            #self.idPersonnePhysiques.append(data[i][0])
            j = 1
            while j < len(data[i]) :
                self.ui.tableWidget_2.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def showInTableBatiment(self, data):
        self.ui.tableWidget.setRowCount(0)

        i = 0

        while i < len(data):
            rowPosition = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            # self.idPersonnePhysiques.append(data[i][0])
            j = 0
            print '---len data i------'
            print len(data[i])
            while j < len(data[i]):
                self.ui.tableWidget.setItem(rowPosition, j , QTableWidgetItem(unicode(data[i][j])))
                j = j + 1
            i = i + 1

    def fillLineEditcode(self):
        code = ""
        numero = ""
        if self.ui.comboFokontany.currentIndex() != -1:
            code = str(self.codesFokontany[self.ui.comboFokontany.currentIndex()])
           # code = code + "-" + str(self.lastId + 1)
            if self.ui.comboHameau.currentIndex() != -1:
                code = code + str(self.codesHameau[self.ui.comboHameau.currentIndex()])
        else:
            code = ""

        numero = str(self.ui.lineEditNumParcelle.text()).strip()
        code = code + "-" + numero
        self.ui.lineEditCodeParcelle.setText(code)


    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEditNom.setValidator(validatorAlpha)
        self.ui.lineEditPrenom.setValidator(validatorAlpha)
        self.ui.lineEditAdresse.setValidator(validatorAlphaNum)
        self.ui.lineEditLieuNaissance.setValidator(validatorAlpha)
        self.ui.lineEditCIN1.setValidator(validatorNum)
        self.ui.lineEditCIN2.setValidator(validatorNum)
        self.ui.lineEditCIN3.setValidator(validatorNum)
        self.ui.lineEditCIN4.setValidator(validatorNum)
        self.ui.lineEditLieuCIN.setValidator(validatorAlphaNum)
        self.ui.lineEditNumActeNaissance.setValidator(validatorNum)
        self.ui.lineEditLieuActeNaissance.setValidator(validatorAlphaNum)
        self.ui.lineEditNumParcelle.setValidator(validatorAlphaNum)
        self.ui.lineEditCodeParcelle.setValidator(validatorAlphaNum)
        self.ui.nombrePiCesLineEdit_2.setValidator(validatorNum)
        self.ui.surfaceLineEdit_3.setValidator(validatorNum)
        #self.ui.lineEditCIN.setMaxLength(3)
        self.ui.lineEditCIN1.setMaxLength(3)
        self.ui.lineEditCIN2.setMaxLength(3)
        self.ui.lineEditCIN3.setMaxLength(3)
        self.ui.lineEditCIN4.setMaxLength(3)

    def updateFields(self):
        try:
            self.cur.execute("SELECT numero, codeparcelle, cp.idpersonne, idhameau, has_data, conversion,etatparcelle_d, srisraparcelle, consistance, idcertificat, cp.contribuable, idcategorie, idclasse, fi_forfait  "
                             "FROM parcelle_d pd LEFT JOIN contribuables_parcelle cp ON pd.gid = cp.idparcelle "
                             "WHERE gid = %s", (self.idparcelle,))
            data = self.cur.fetchall()
            #print "Donnees fiscales"
            #print data
            print "data for parcelle is " + str(data)
            self.useData(data)
        except StandardError as e:
            print (e)
            self.connection.rollback()

    def useData(self, data):
        if data[0][0] is not None:
            self.ui.lineEditNumParcelle.setText(data[0][0])
        if data[0][1] is not None:
            self.ui.lineEditCodeParcelle.setText(data[0][1])
        if data[0][3] is not None:
            try:
                self.cur.execute("SELECT h.nomhameau, f.nomfokontany FROM hameau h, fokontany f WHERE h.idfokontany = f.idfokontany AND idhameau = %s", (data[0][3],))
                hm = self.cur.fetchone()
                print hm
                self.ui.comboHameau.setCurrentIndex(self.ui.comboHameau.findText(str(hm[0]).strip()))
                self.ui.comboFokontany.setCurrentIndex(self.ui.comboFokontany.findText(str(hm[1].strip())))
            except StandardError as e:
                print (e)
                self.connection.rollback()
        if data[0][4] is True:
            if data[0][9] is not None:
                self.ui.convertirDemande.hide()
            else:
                if data[0][5] is not None:
                    self.ui.convertirDemande.show()
                    self.etatConversion = data[0][5]
                    if data[0][5] == 1: # deja converti en demande
                        self.ui.convertirDemande.setText("Convertir en Certificat")
                        #self.ui.convertirDemande.clicked.connect
                    elif data[0][5] == 2: # deja converti en CF
                        self.ui.convertirDemande.hide()

        if data[0][13] is not None:
            if str(data[0][13]).strip() == "surface":
                self.ui.radioButton_Surface.setChecked(True)
            if str(data[0][13]).strip() == "classe":
                self.ui.radioButton_Classe.setChecked(True)
            if str(data[0][13]).strip() == "valeur_venale":
                self.ui.radioButton_Venale.setChecked(True)

        if data[0][11] is not None:#idcategorie
            self.ui.comboCategorieParcelle.setCurrentIndex(int(data[0][11]) - 1)
        if data[0][12] is not None:
            self.ui.comboBoxClasse.setCurrentIndex(int(data[0][12]) - 1)



        for pers in data:
            if pers[2] is not None:
                if pers[10] is True:
                    self.idContribuable = int(pers[2])
                    self.getContribuableById(pers[2])
        # afficher les limites de la parcelle ##
        try:
            self.cur.execute("SELECT pc.idpointscardinaux, pc.position, l.description FROM limitesparcelle l, pointscardinaux pc WHERE l.idpointscardinaux = pc.idpointscardinaux AND l.idparcelle = %s", (self.idparcelle,))
            limites = self.cur.fetchall()
            print limites
            self.showInTable(limites)
        except StandardError as e:
            self.connection.rollback()
            print(e)
        # afficher les batiments sur la parcelle ##
        try:
            #self.cur.execute("SELECT b.codebatiment,c.consistance, b.surfacebatiment, b.nbpiecebatiment  FROM batiment b, consistance_batiment c WHERE b.idconsistance = c.id AND b.idparcelle = %s", (self.idparcelle,))
            self.cur.execute(
                "SELECT b.codebatiment,c.libellecategorie, b.surfacebatiment, b.nbpiecebatiment, b.idparcelle ,b.fi_forfait,b.idclasse, b.idcategorie FROM batiment b, categorie c WHERE b.idcategorie = c.idcategorie AND b.idparcelle = %s",
                (self.idparcelle,))
            bats = self.cur.fetchall()
            self.showInTableBatiment(bats)
        except StandardError as e:
            self.connection.rollback()
            print(e)
        #Etat parcelle
        if data[0][6] is not None:
            if data[0][6] == 0:
                self.ui.radioAucun.setChecked(True)
            elif data[0][6] == 1:
                self.ui.radioTitree.setChecked(True)
            elif data[0][6] == 2:
                self.ui.radioCadastree.setChecked(True)
            elif data[0][6] == 3:
                self.ui.radioCertifiee.setChecked(True)
        else:
            self.ui.radioAucun.setChecked(True)
        #SRI SRA parcelle
        if data[0][7] is not None:
            if str(data[0][7]).strip() == "sri":
                self.ui.radioSRI.setChecked(True)
            elif str(data[0][7]).strip() == "sra":
                self.ui.radioSRA.setChecked(True)
        if data[0][8] is not None:
            self.ui.comboConsistanceParcelle.setCurrentIndex(self.ui.comboConsistanceParcelle.findText(str(data[0][8]).strip()))

    def ouvrirDemande(self):
        if self.ui.comboHameau.currentIndex() == -1:
            QMessageBox.critical(self, "Erreur sur hameau", u"Veuillez séléctionner un Hameau ")
            return
        else:
            if self.etatConversion is None:
                if str(self.ui.lineEditNom.text()).strip() == "":
                    QMessageBox.critical(self, "Conversion en demande", "Le champ Nom de la rubrique contribuable est obligatoire")
                    return
                elif self.areaHa_d >=  10:
                    QMessageBox.critical(self, "Conversion en demande", u"La surface doit être inférieeure à 10 Ha pour pouvoir être convertie en demande")
                    return
                else:
                    if self.ui.comboFokontany.currentIndex() != -1:
                        self.singleIdFokontany = self.idFokontany[self.ui.comboFokontany.currentIndex()]
                        if self.ui.comboHameau.currentIndex() != -1:
                            self.singleIdHameau = self.idHameau[self.ui.comboFokontany.currentIndex()]
                            self.readInput(1)
                            print "idFokontany = " + str(self.singleIdFokontany)
                            print "idhameau = " + str(self.singleIdHameau)
                            self.nomDemandeur = unicode(self.ui.lineEditNom.text()).encode('utf-8').strip()
                            self.prenomDemandeur = unicode(self.ui.lineEditPrenom.text()).encode('utf-8').strip()
                            from .NumeroDmdeRun import NumeroDmde
                            num = NumeroDmde(self.connection, self)
                            num.exec_()
                        else:
                            QMessageBox.critical(self, "Conversion en demande", u"Veuillez séléctionner un Hameau s'il vous plait")
                    else:
                        QMessageBox.critical(self, "Conversion en demande", u"Veuillez séléctionner un Fokontany s'il vous plait")
            elif self.etatConversion == 1:
                if self.ui.comboFokontany.currentIndex() != -1:
                    self.singleIdFokontany = self.idFokontany[self.ui.comboFokontany.currentIndex()]
                    if self.ui.comboHameau.currentIndex() != -1:
                        self.singleIdHameau = self.idHameau[self.ui.comboFokontany.currentIndex()]
                        self.readInput(1)
                        print "idFokontany = " + str(self.singleIdFokontany)
                        print "idhameau = " + str(self.singleIdHameau)
                        self.nomDemandeur = unicode(self.ui.lineEditNom.text()).encode('utf-8').strip()
                        self.prenomDemandeur = unicode(self.ui.lineEditPrenom.text()).encode('utf-8').strip()

                from .NumeroCFRun import NumeroCF
                numCF = NumeroCF(self.connection, self)
                numCF.exec_()

    #### Gestion des batiments sur une parcelle ####
    def deleteOneBat(self):
        if self.ui.tableWidget.currentRow() == -1:
            QMessageBox.critical(self, u"Suppression d'un batiment", u"Veuillez au moins séléctionner une ligne dans le tableau")
        else:
            row = self.ui.tableWidget.currentRow()
            codeBat = self.ui.tableWidget.item(row, 0).data(0).toString()
            #self.ui.tableWidgetBatiment.removeRow(row)
            try:
                self.cur.execute("DELETE FROM batiment WHERE codebatiment = %s", (str(codeBat),))
                self.connection.commit()
                # afficher les batiments sur la parcelle ##
                try:
                    self.cur.execute(
                        "SELECT b.codebatiment,c.consistance, b.surfacebatiment, b.nbpiecebatiment, b.idparcelle  FROM batiment b, consistance_batiment c WHERE b.idconsistance = c.id AND b.idparcelle = %s",
                        (self.idparcelle,))
                    bats = self.cur.fetchall()
                    self.infosBatiments[:] = []
                    for bat in bats:
                        if bat not in self.infosBatiments:
                            self.infosBatiments.append(bat)
                    print self.infosBatiments
                    self.showInTableBatiment(bats)
                except StandardError as e:
                    self.connection.rollback()
                    print(e)
                #self.showInTableBatiment()
            except StandardError as e:
                self.connection.rollback()
                print(e)

    def addOneBat(self):
        rowPosition = self.ui.tableWidget.rowCount()
        print rowPosition
        infoBatiment = []
        infoBatiment[:] = []
        if self.ui.lineEditCode.text() == "":
            QMessageBox.critical(self, "Erreur", u"Le champ code doit être renseigné")
        else:
            infoBatiment.append(str(self.ui.lineEditCode.text()).encode('utf-8'))
        infoBatiment.append(self.idCategoriesBatiment[self.ui.comboCategorieBatiment.currentIndex()])
        if self.ui.comboConsistanceBatiment.currentIndex() != -1:
            infoBatiment.append(self.idConsistancesBatiment[self.ui.comboConsistanceBatiment.currentIndex()])
        else:
            infoBatiment.append(None)
        if self.ui.surfaceLineEdit_3.text() == "" and self.ui.nombrePiCesLineEdit_2.text() == "":
            QMessageBox.critical(self, "Erreur", u"Veuillez renseigné au moins le champ Surface (m2) ou Nombre pièces")
        else:
            if self.ui.surfaceLineEdit_3.text() == "":
                infoBatiment.append(0)
            else:
                infoBatiment.append(float(self.ui.surfaceLineEdit_3.text()))
            if self.ui.nombrePiCesLineEdit_2.text() == "":
                infoBatiment.append(0)
            else:
                infoBatiment.append(int(self.ui.nombrePiCesLineEdit_2.text()))

        if self.idparcelle is not None:
            infoBatiment.append(self.idparcelle)
        classe=0
        if self.ui.radioButton_SurfaceBatiment.isChecked():
            infoBatiment.append('surface')
        if self.ui.radioButton_ClasseBatiment.isChecked():
            infoBatiment.append('classe')
            classe=int(self.ui.comboBoxClasseBatiment.currentIndex())+1
        if self.ui.radioButton_LocativeBatiment.isChecked():
            infoBatiment.append('valeur_locative')

        infoBatiment.append(classe)
        #self.infosBatiments.append(infoBatiment)

        try:
            self.cur.execute(
                "INSERT INTO public.batiment (codebatiment, idparcelle, idconsistance, surfacebatiment, nbpiecebatiment, locationbatiment, idcategorie,fi_forfait,idclasse ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (infoBatiment[0], infoBatiment[5], infoBatiment[2],
                 infoBatiment[3], infoBatiment[4], self.ui.avecLocationCheckBox_2.isChecked(), infoBatiment[1], infoBatiment[6], infoBatiment[7]))
            self.connection.commit()
            self.ui.lineEditCode.clear()
            self.ui.tableWidget.setRowCount(0)
            self.ui.nombrePiCesLineEdit_2.clear()
            self.ui.comboConsistanceBatiment.setCurrentIndex(0)
            self.ui.comboCategorieBatiment.setCurrentIndex(0)
            self.ui.comboBoxClasseBatiment.setCurrentIndex(0)
            self.ui.avecLocationCheckBox_2.setChecked(False)
            # afficher les batiments sur la parcelle ##
            try:
                self.cur.execute(
                    "SELECT b.codebatiment,c.libellecategorie, b.surfacebatiment, b.nbpiecebatiment, b.idparcelle ,b.fi_forfait,b.idclasse FROM batiment b, categorie c WHERE b.idcategorie = c.idcategorie  AND b.idparcelle = %s",
                    (self.idparcelle,))
                bats = self.cur.fetchall()
                self.infosBatiments[:] = []
                for bat in bats:
                    if bat not in self.infosBatiments:
                        self.infosBatiments.append(bat)
                print '-----------------------info bat-----------'
                print self.infosBatiments
                self.showInTableBatiment(bats)
            except StandardError as e:
                self.connection.rollback()
                print(e)
            #self.showInTableBatiment()
        except StandardError as e:
            print e
            self.connection.rollback()
        #except psycopg2.Error as e:
            #print "Info batiment " + str(e)
            #if e.pgcode == "23505":
                #QMessageBox.critical(self, u"Erreur", u"Le code batiment existe déjà")
                #self.connection.rollback()
        #print self.infosBatiments

    #### Gestion des limites ####
    def addLimite(self):
        limiteparcelle = []
        limiteparcelle.append(self.idPointCardinaux[self.ui.positionComboBox.currentIndex()])
        #self.limitesParcelle.append(self.ui.positionComboBox.itemData(1))
        #print self.idsPositions
        rowPosition = self.ui.tableWidget_2.rowCount()
        # idpersonnes.append(data[i][0])
        #self.listeIdConsorts.append(self.currData[0])
        #print self.listeIdConsorts
        if self.ui.descriptionLineEdit.text() != "":
            limiteparcelle.append(unicode(self.ui.descriptionLineEdit.text()).encode('utf-8'))
            self.limitesParcelle.append(limiteparcelle)
            try:
                self.cur.execute("INSERT INTO limitesparcelle(idpointscardinaux, idparcelle, description) VALUES(%s, %s, %s)",
                                 (limiteparcelle[0], self.idparcelle, limiteparcelle[1]))
                self.connection.commit()
                self.ui.tableWidget_2.insertRow(rowPosition)
                self.ui.tableWidget_2.setItem(rowPosition, 0, QTableWidgetItem(self.ui.positionComboBox.currentText()))
                self.ui.tableWidget_2.setItem(rowPosition, 1, QTableWidgetItem(self.ui.descriptionLineEdit.text()))
            except psycopg2.Error as e:
                print(e)
                if e.pgcode == "23505":
                    QMessageBox.critical(self, u"Erreur", u"La combinaison position et parcelle existe déjà")
                    self.connection.rollback()
        else:
            QMessageBox.critical(self, "Erreur", u"Le champ description doit être renseigné")

        #print self.limitesParcelle

        self.ui.descriptionLineEdit.clear()

    def deleteLimite(self):
        if self.ui.tableWidget_2.currentRow() == -1:
            QMessageBox.critical(self, u"Suppression d'une limire", u"Veuillez au moins séléctionner une ligne dans le tableau")
        else:
            row = self.ui.tableWidget_2.currentRow()
            position = self.ui.tableWidget_2.item(row, 0).data(0).toString()
            try:
                self.cur.execute("SELECT idpointscardinaux FROM pointscardinaux WHERE position = %s", (str(position),))
                idPointCardinal = self.cur.fetchone()
                print idPointCardinal
                self.ui.tableWidget_2.removeRow(row)
                try:
                    self.cur.execute("DELETE FROM limitesparcelle WHERE idpointscardinaux = %s and idparcelle = %s",
                                     (idPointCardinal[0],self.idparcelle))
                    self.connection.commit()
                    # afficher les limites sur la parcelle ##
                    try:
                        self.cur.execute(
                            "SELECT pc.idpointscardinaux, pc.position, l.description FROM limitesparcelle l, pointscardinaux pc WHERE l.idpointscardinaux = pc.idpointscardinaux AND l.idparcelle = %s",
                            (self.idparcelle,))
                        limites = self.cur.fetchall()
                        print limites
                        self.showInTable(limites)
                        for limite in limites:
                            if limite not in self.infosBatiments:
                                self.limitesParcelle.append(limite)
                        print self.limitesParcelle
                        self.showInTable(limites)
                    except StandardError as e:
                        self.connection.rollback()
                        print(e)
                        # self.showInTableBatiment()
                except StandardError as e:
                    self.connection.rollback()
                    print(e)
            except StandardError as e:
                self.connection.rollback()
                print(e)

            print position

    def traiterContribuableCF(self):
        # Traitement des contribuables
        if self.isFiscalisation:
            try:
                self.cur.execute(
                    "SELECT * FROM proprietaireparcelle WHERE idparcelle = %s",
                    (self.idparcelle,))
                dataPersonne = self.cur.fetchall()
                for dataP in dataPersonne:
                    if dataP[2] is True:
                        self.idContribuable = dataP[0]
                        self.ui.btnConsorts.setEnabled(True)
                    self.cur.execute("INSERT INTO contribuables_parcelle (idpersonne, idparcelle, contribuable) "
                                     "VALUES (%s, %s, %s)", (dataP[0], dataP[1], dataP[2]))
                    self.connection.commit()

            except StandardError as e:
                print(e)
                self.connection.rollback()
                # FIN TRAITEMENT CONTRIBUABLE


    def fillComboClasse(self):
        self.ui.comboBoxClasse.clear()
        self.ui.comboBoxClasseBatiment.clear()
        self.cur.execute('SELECT * FROM public.classe')
        res = self.cur.fetchall()
        for value in res:
           self.ui.comboBoxClasse.addItem(value[1], value[0])
           self.ui.comboBoxClasseBatiment.addItem(value[1], value[0])
        self.ui.comboBoxClasse.setCurrentIndex(0)
        self.ui.comboBoxClasseBatiment.setCurrentIndex(0)

    def __del__(self):
        self.cur.close()
