# coding: utf8
import os, os.path, sys, datetime, time
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
import globalvars
from Utils import Utils

from .MarquagePaiementImpot import Ui_Dialog
from AreaConvert import AreaConvert

class PaiementImpotRun(QDialog):
    def __init__(self, connection):
        self.connection = connection
        self.initDB()
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.comboBoxEtatPayement.setCurrentIndex(0)
        self.idContribuableAvecImpot = []
        self.valeurImpotTotalParContribuable = []
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.tableWidget.setSelectionBehavior(1)
        self.idsContribuables = None
        self.idContribuable = None
        self.ui.comboBoxMarquagePaiement.setDisabled(True)
        from Fiplof.Saisie.VoirListeContribuableRun import VoirListeContribuableRun
        self.listeContribuable = VoirListeContribuableRun(self.connection)
        from Personnes.ListePersonnePqueRun import ListePersonnePqueRun
        self.listePersonne = ListePersonnePqueRun(self.connection)
        self.valeurImpotPayee = 0
        self.restaApayerParAn = {}
        self.anneeConcernee = 0
        self.initActions()
        self.disableAll()
        self.showAll()
        self.initMasks()
        self.currentIdContribuable = None
        self.dateJour = datetime.datetime.now().date()
        print self.dateJour


    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart

    def __del__(self):
        self.cur.close()

    def initActions(self):
        self.ui.btnVoir.clicked.connect(self.afficherListePersonne)
        self.listePersonne.ui.btnSelectionner.clicked.connect(self.setIdContribuable)
        self.ui.checkBoxPaiement.stateChanged.connect(self.updateFieldsState)
        self.ui.checkBoxContribuable.stateChanged.connect(self.updateFieldsState)
        self.ui.tableWidget.cellClicked.connect(self.getCurrentIdContribuable)
        self.ui.btnModifier.clicked.connect(self.modifierEtatPaiement)
        self.ui.btnRechercher.clicked.connect(self.rechercher)
        self.ui.pushButton_10.clicked.connect(self.close)

    def afficherListePersonne(self):
        print "Bouton Voir Liste Personne"
        self.listePersonne.exec_()

    def setIdContribuable(self):
        self.idContribuable = self.listePersonne.getIdPersonne()
        print "id contribuable = " + str(self.idContribuable)
        if self.idContribuable is not None:
            self.getContribuableById(self.idContribuable)
        self.listePersonne.close()

    def getContribuableById(self, id):
        self.cur.execute("SELECT * FROM personne WHERE idpersonne = %s", (id,))
        data = self.cur.fetchone()
        print data
        self.fillFields(data)

    def fillFields(self, data):
        print "fillFields"
        nom = ""
        if data[1]: # nom
            nom = nom + data[1] + " "
        if data[2]: # prenoms
            nom = nom + data[2] + " "
        self.ui.lineEditContribuable.setText(nom)

    def showAll(self, data = None):
        if data is not None:
            listeParams = []
            listeParams[:] = []
            flag = 0
            nom = ''
            prenoms = ''
            SQL = "SELECT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne, ic.etatpaiement, p.adressepersonne, ic.hetratany::numeric + ic.hetratrano::numeric, ic.annee FROM personne p INNER JOIN impot_contribuable ic " \
                  "ON p.idpersonne = ic.idpersonne "
            i = 0
            if self.ui.checkBoxContribuable.isChecked():
                for contribuableInfo in data['nomprenom'].split(' '):
                    if i == 0 and contribuableInfo != '':
                        nom = nom + contribuableInfo
                        i = i + 1
                    elif i > 0 and contribuableInfo != '':
                        if i == 1:
                            prenoms = prenoms + contribuableInfo
                        else:
                            prenoms = prenoms + " " + contribuableInfo
                        i = i + 1
                if flag == 0:
                    if nom != '' or prenoms != '':
                        nom = "%" + nom.lower() + "%"
                        prenoms = "%" + prenoms.lower() + "%"
                        SQL = SQL + "WHERE LOWER(p.nompersonne) LIKE %s or LOWER(p.prenompersonne) LIKE %s "
                        listeParams.append(nom)
                        listeParams.append(prenoms)
                        flag = 1
                else:
                    if nom != '' or prenoms != '':
                        nom = "%" + nom.lower() + "%"
                        prenoms = "%" + prenoms.lower() + "%"
                        SQL = SQL + "AND LOWER(p.nompersonne) LIKE %s or LOWER(p.prenompersonne) LIKE %s "
                        listeParams.append(nom)
                        listeParams.append(prenoms)

            if self.ui.checkBoxPaiement.isChecked():
                if data['etatpaiement'] == 0:
                    if flag == 0:
                        SQL = SQL + " WHERE ic.etatpaiement = %s or ic.etatpaiement is NULL"
                        listeParams.append(data['etatpaiement'])
                        flag = 1
                    else:
                        SQL = SQL + " AND ic.etatpaiement = %s or ic.etatpaiement is NULL"
                        listeParams.append(data['etatpaiement'])
                else:
                    if flag == 0:
                        SQL = SQL + " WHERE ic.etatpaiement = %s "
                        listeParams.append(data['etatpaiement'])
                        flag = 1
                    else:
                        SQL = SQL + " AND ic.etatpaiement = %s "
                        listeParams.append(data['etatpaiement'])

            #execution de la requete
            params = tuple(listeParams)
            SQL = SQL + " ORDER BY p.idpersonne ASC"
            #print SQL
            try:
                self.cur.execute(SQL, params)
                self.idsContribuables = self.cur.fetchall()
                self.calculImpot()
            except StandardError as e:
                print e

        else:
            try:
                self.cur.execute("SELECT p.idpersonne, p.nompersonne, p.prenompersonne, p.numcipersonne, ic.etatpaiement, p.adressepersonne, ic.hetratany::numeric + ic.hetratrano::numeric, ic.annee"
                                 " FROM personne p INNER JOIN impot_contribuable ic " \
                  "ON p.idpersonne = ic.idpersonne  ORDER BY p.idpersonne ASC")
                self.idsContribuables = self.cur.fetchall()
                #print "CONTRIBUABLES"
                #print self.idsContribuables
                #print "FIN CONTRIBUABLES"
                self.calculImpot()
            except StandardError as e:
                print e

    def calculImpot(self):
        print "RECALCUL IMPOT"
        #self.idContribuableAvecImpot[:] = []
        self.ui.tableWidget.setRowCount(0)
        impotParContribuable = []
        impotParContribuable[:] = []
        print "Eto no manao calcul Impot"
        i = 1
        #k = 0
        for idcontribuable in self.idsContribuables:
            valeurImpot = 0
            idHameau = None
            #impotBatiment[:] = []
            #Calcul de l'impot sur parcelle
            try:
                self.cur.execute(
                    "SELECT pd.gid, pd.surface::numeric::float8,ic.idpersonne, pd.idhameau "
                    "FROM parcelle_d pd, "
                    "impot_contribuable ic, contribuables_parcelle cp "
                    "WHERE cp.idparcelle = pd.gid "
                    "AND ic.idpersonne = %s "
                    "AND cp.idpersonne = %s", (idcontribuable[0],idcontribuable[0]))
                dataImpot = self.cur.fetchall()
                #from .resCalculImpotRun import resCalculImpotRun
                #calc = resCalculImpotRun(self.connection, dataImpot)
                #res = calc.exec_()
                if len(dataImpot) > 0:
                    impotParContribuable[:] = []
                    impotParContribuable.append(idcontribuable[0])
                    self.idContribuableAvecImpot.append(idcontribuable[0])
                    nomEtPrenom = idcontribuable[1] + " " + idcontribuable[2]
                    impotParContribuable.append(nomEtPrenom)
                    impotParContribuable.append(idcontribuable[3]) # CIN
                    if idcontribuable[4] is not None:
                        if idcontribuable[4] == 0: #Non paye
                            impotParContribuable.append(u"Non payé")
                        elif idcontribuable[4] == 1: #Partiellement paye
                            impotParContribuable.append(u"Partiellement payé")
                        elif idcontribuable[4] == 2: #Totalement paye
                            impotParContribuable.append(u"Payé")
                    else:
                        impotParContribuable.append(u"Non payé")


                    impotParcelle = 0
                    impotBatiment = 0
                    print dataImpot
                    ######## CALCUL DE L'IMPOT DE CHAQUE CONTRIBUABLE#######

                    j = 0
                    for values in dataImpot:
                        if len(values) > 0:
                            if idHameau is None:
                                idHameau = values[3]
                            j = j + 1
                            print "tour " + str(j)

                    impotParContribuable.append(idcontribuable[6]) # Valeur total de l'impot par contribuable
                    self.valeurImpotTotalParContribuable.append(idcontribuable[6])
                    impotParContribuable.append(idHameau) #valeur de l'idHameau
                    impotParContribuable.append(idcontribuable[5]) # Valeur de l'adresse
                    impotParContribuable.append(idcontribuable[7]) #annee
                    #print self.idContribuableAvecImpot
                    self.setNewValImpot(impotParContribuable)
                    #k = k + 1

            except StandardError as e:
                print e

            print "impot par contribuable"
            print impotParContribuable
            print i
            print len(self.idsContribuables)
            i = i + 1

    def setNewValImpot(self, tabImpot):
        print "***********ytab impot*******"
        print tabImpot
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        #self.allImpot = self.allImpot + tabImpot[2]
        j = 1
        print len(tabImpot)
        while j <= len(tabImpot):
            #print "j= " + str(j)
            if j <= 4:
                self.ui.tableWidget.setItem(rowPosition, j - 1, QTableWidgetItem(unicode(tabImpot[j])))
            elif j == 5:
                if tabImpot[j] is not None:
                    try:
                        self.cur.execute("SELECT c.nomcommune, h.nomhameau from commune c, fokontany f, hameau h WHERE f.idcommune = c.idcommune AND f.idfokontany = h.idfokontany AND h.idhameau = %s", (tabImpot[j],))
                        res = self.cur.fetchone()
                        self.ui.tableWidget.setItem(rowPosition, j - 1,  QTableWidgetItem(unicode(res[0])))
                        self.ui.tableWidget.setItem(rowPosition, j, QTableWidgetItem(unicode(res[1])))
                    except StandardError as e:
                        print e
                #self.ui.tableWidget.setItem(rowPosition, j , QTableWidgetItem(unicode(tabImpot[j])))
            elif j == 6:
                self.ui.tableWidget.setItem(rowPosition, j , QTableWidgetItem(unicode(tabImpot[j])))
            elif j == 7:
                self.ui.tableWidget.setItem(rowPosition, j , QTableWidgetItem(str(tabImpot[0])))
                self.ui.tableWidget.setItem(rowPosition, j+1 , QTableWidgetItem(str(tabImpot[7])))
            j = j + 1

    def updateFieldsState(self):
        self.ui.lineEditContribuable.setEnabled(self.ui.checkBoxContribuable.isChecked())
        if self.ui.checkBoxContribuable.isChecked() != True:
            self.ui.lineEditContribuable.clear()
        self.ui.comboBoxEtatPayement.setEnabled(self.ui.checkBoxPaiement.isChecked())
        self.ui.dateEdit.setEnabled(self.ui.checkBoxPaiement.isChecked())

    def disableAll(self):
        self.ui.lineEditContribuable.setEnabled(False)
        self.ui.comboBoxEtatPayement.setEnabled(False)
        self.ui.dateEdit.setEnabled(False)

    def getCurrentIdContribuable(self):
        self.currentIdContribuable = Utils.getTableWidgetCellIntvalue(self.ui.tableWidget, self.ui.tableWidget.currentRow(), 7)
        annee = Utils.getTableWidgetCellIntvalue(self.ui.tableWidget, self.ui.tableWidget.currentRow(), 8)
        self.anneeConcernee = annee
        #self.currentIdContribuable =  self.idContribuableAvecImpot[self.ui.tableWidget.currentRow()]
        try:
            self.cur.execute("SELECT etatpaiement FROM impot_contribuable WHERE idpersonne = %s AND annee = %s", (self.currentIdContribuable,annee))
            etat = self.cur.fetchone()
            print etat[0]
            if etat[0] is not None:
                self.ui.comboBoxMarquagePaiement.setCurrentIndex(etat[0])
            else:
                self.ui.comboBoxMarquagePaiement.setCurrentIndex(0)
        except StandardError as e:
            print e

    def modifierEtatPaiement(self):
        self.valeurImpotPayee = 0
        if self.currentIdContribuable is None:
            QMessageBox.critical(None, "Erreur", "Veuillez choisir au moins une ligne")
            return
        else:
            if self.ui.comboBoxMarquagePaiement.currentIndex() == 2:
                QMessageBox.information(None, "Information", u"Le cotribuable n'a plus de d'impôt à payer")
                return
            reply = QMessageBox.question(self, "Confirm",
                                         "Voulez-vous modifier l'etat de paiement de cette impot?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:

                impotAPayer = self.getAllImpotToPay(self.currentIdContribuable)

                print "montant restant par annee"
                print self.restaApayerParAn
                apayerAnnee = float(self.restaApayerParAn[str(self.anneeConcernee)])
                from .montantRun import montant
                self.mnt = montant(self.connection, apayerAnnee, self.currentIdContribuable, self)
                #self.mnt.ui.buttonBox.accepted.connect(self.getValue)
                self.mnt.ui.pushButtonEnregistrer.clicked.connect(self.getValue)
                self.mnt.ui.lineEdit.setReadOnly(True)
                self.mnt.exec_()
                impot_existant = 0
                precedement_paye = 0
                impot_restant = 0

                impoBatParAn = self.getAllImpotBat(self.currentIdContribuable)
                print "******impotbat par an*********"
                print impoBatParAn

                try:
                    impoParcelleParAn = self.getAllImpotParcelle(self.currentIdContribuable)
                except Exception as err:
                    print "erreur call all impot parcelle"
                    print err

                print "******impot parcelle par an*********"
                print impoParcelleParAn

                print self.valeurImpotPayee
                for key, value in self.restaApayerParAn.items():
                    montantpaye = 0
                    etapaiement = 0
                    montant_a_dipatcher = 0.0
                    annee = int(key)

                    if int(annee) == int(self.anneeConcernee):
                        sommeAnnee =  float(value)
                        if self.valeurImpotPayee >= sommeAnnee:
                            print "montant sup a somme annee"
                            print "montant = " + str(self.valeurImpotPayee)
                            print "sommeAnnee = " + str(sommeAnnee)
                            montantpaye = sommeAnnee + self.getMontantPayePrec(self.currentIdContribuable, annee)
                            etapaiement = 2 #EN TOTALITE
                            self.valeurImpotPayee = self.valeurImpotPayee - sommeAnnee
                            print "montant paye = " + str(montantpaye)
                            for ibat in impoBatParAn:
                                code_batiment = None
                                if int(ibat[3]) == annee:
                                    code_batiment = str(ibat[0]).strip()
                                if code_batiment is not None:
                                    self.setTotalPayedBat(code_batiment, annee)

                            for parcelle in impoParcelleParAn:
                                idparcelle = None
                                if int(parcelle[1]) == annee:
                                    idparcelle = int(parcelle[4])
                                if idparcelle is not None:
                                    self.setTotalPayeParcelle(idparcelle, annee)

                        else: #payement partiel
                            print "paie partielle"
                            montantpaye = self.valeurImpotPayee + self.getMontantPayePrec(self.currentIdContribuable, annee)
                            etapaiement = 1 #EN PARTIE
                            montant_a_dipatcher = self.valeurImpotPayee
                            ##Manip paiement en partie des bat et parcelle de chaque annee
                            for ibat in impoBatParAn:
                                code_batiment = None
                                ex_montant_paye = 0.0
                                if int(ibat[3]) == annee:
                                    code_batiment = str(ibat[0]).strip()
                                    impot_bat = float(ibat[2])
                                    if ibat[4] is not None:
                                        ex_montant_paye = float(ibat[4])
                                    diff = impot_bat - ex_montant_paye
                                    print "ibat AN"
                                    if montant_a_dipatcher - diff >= 0.0:
                                        if code_batiment is not None:
                                            self.setTotalPayedBat(code_batiment, annee)
                                            montant_a_dipatcher = montant_a_dipatcher - diff
                                    else:
                                        if montant_a_dipatcher > 0.0:
                                            new_montant_paye = montant_a_dipatcher + ex_montant_paye
                                            self.setPartiallyPayedBat(code_batiment, annee, new_montant_paye)
                                            montant_a_dipatcher == 0.0

                            for parcelle in impoParcelleParAn:
                                idparcelle = None
                                ex_montant_paye = 0.0
                                if int(parcelle[1]) == annee:
                                    idparcelle = int(parcelle[4])
                                    impo_parc = float(parcelle[0])
                                    if parcelle[2] is not None:
                                        ex_montant_paye = float(parcelle[2])
                                    diff = impo_parc - ex_montant_paye
                                    if montant_a_dipatcher - diff >= 0.0:
                                        if idparcelle is not None:
                                            self.setTotalPayeParcelle(idparcelle, annee)
                                            montant_a_dipatcher = montant_a_dipatcher - diff
                                    else:
                                        if montant_a_dipatcher > 0.0:
                                            new_montant_paye = montant_a_dipatcher + ex_montant_paye
                                            self.setPartiallyPayedParc(idparcelle, annee, new_montant_paye)
                                            montant_a_dipatcher == 0.0

                            self.valeurImpotPayee = 0
                        if montantpaye == 0:
                            break
                        else:
                            try:
                                self.cur.execute("UPDATE impot_contribuable SET etatpaiement = %s, datereglement = %s, montantpaye = %s WHERE idpersonne = %s AND annee = %s", (etapaiement, self.dateJour, montantpaye, self.currentIdContribuable, annee))
                                self.connection.commit()
                            except Exception as err:
                                print "erreur update impot"
                                print err
                                self.connection.rollback()

                self.showAll()



    def getValue(self):
        self.mnt.makeAll()
        #self.mnt.close()
        #print "READING VALUE"
        #self.valeurImpotPayee = float(self.mnt.readValue())

    def rechercher(self):
        self.readInput()

    def readInput(self):
        data = {}
        data['nomprenom'] = unicode(self.ui.lineEditContribuable.text()).encode('utf-8')
        data['etatpaiement'] = int(self.ui.comboBoxEtatPayement.currentIndex())
        self.showAll(data)
        #self.rechercher()

    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEditContribuable.setValidator(validatorAlphaNum)

    def setPartiallyPayedParc(self, idparcelle, annee, montant):
        print "call of setPartiallyPayedBat"
        cur = self.connection.cursor()
        try:
            cur.execute("UPDATE impot_parcelle SET montant_paye =  %s"
            "WHERE idparcelle = %s and annee = %s ", (montant,idparcelle, annee))
            self.connection.commit()
        except Exception as err:
            print "Erreur setTotalPayedBat"
            print err
            self.connection.rollback()

    def setPartiallyPayedBat(self, codebatiment, annee, montant):
        print "call of setPartiallyPayedBat"
        cur = self.connection.cursor()
        try:
            cur.execute("UPDATE impot_batiment SET montant_paye =  %s"
            "WHERE codebatiment = %s and annee = %s ", (montant,codebatiment, annee))
            self.connection.commit()
        except Exception as err:
            print "Erreur setTotalPayedBat"
            print err
            self.connection.rollback()

    def setTotalPayeParcelle(self, idparcelle, annee):
        print "call of setTotalPayeParcelle"
        cur = self.connection.cursor()
        try:
            cur.execute("UPDATE impot_parcelle "
                        " SET montant_paye = hetratany "
            "WHERE idparcelle = %s and annee = %s ", (idparcelle, annee))
            self.connection.commit()
        except Exception as err:
            print "Erreur setTotalPayeParcelle"
            print err
            self.connection.rollback()

    def setTotalPayedBat(self, codebatiment, annee):
        print "call of setTotalPayedBat"
        cur = self.connection.cursor()
        try:
            cur.execute("UPDATE impot_batiment SET montant_paye = hetratrano "
            "WHERE codebatiment = %s and annee = %s ", (codebatiment, annee))
            self.connection.commit()
        except Exception as err:
            print "Erreur setTotalPayedBat"
            print err
            self.connection.rollback()

    def getAllImpotParcelle(self, idpersonne):
        curs = self.connection.cursor()
        annee = datetime.datetime.now().strftime('%Y')
        anneanterieur = ()
        anneavant = int(annee)
        anneanterieur=anneanterieur + (str(anneavant),)
        for x in range(1, 4):
            anneavant = anneavant - 1
            anneanterieur = anneanterieur + (str(anneavant),)
        print 'annee ---------------------------------------------------------anterieur'

        res = None
        try:
            curs.execute("SELECT ip.hetratany::numeric, ip.annee, ip.montant_paye::numeric, cp.idpersonne , ip.idparcelle "
            "FROM impot_parcelle ip "
            "INNER JOIN contribuables_parcelle cp ON cp.idparcelle = ip.idparcelle " 
            " WHERE cp.contribuable IS TRUE AND cp.idpersonne = %s AND annee IN %s ORDER BY ip.annee ASC", (str(idpersonne),anneanterieur))
            res = curs.fetchall()
        except Exception as err:
            print "Erreur getAllImpotParcelle"
            print err
            self.connection.rollback()
        return res

    def getAllImpotBat(self, idperssonne):
        cur = self.connection.cursor()
        annee = datetime.datetime.now().strftime('%Y')
        anneanterieur = ()
        anneavant = int(annee)
        anneanterieur=anneanterieur + (str(anneavant),)
        for x in range(1, 4):
            anneavant = anneavant - 1
            anneanterieur = anneanterieur + (str(anneavant),)
        print 'annee ---------------------------------------------------------anterieur'

        res = None
        try:
            cur.execute("SELECT b.codebatiment, cp.idpersonne, ib.hetratrano::numeric, ib.annee,ib.montant_paye::numeric "
            "FROM batiment b "
            "INNER JOIN parcelle_d pd ON  b.idparcelle = pd.gid "
            "INNER JOIN contribuables_parcelle cp ON cp.idparcelle = pd.gid "
            "INNER JOIN impot_batiment ib ON ib.codebatiment = b.codebatiment "
            "WHERE cp.contribuable IS TRUE AND cp.idpersonne = %s AND annee IN %s  ORDER BY ib.annee ASC", (idperssonne,anneanterieur))
            res = cur.fetchall()
        except Exception as err:
            print "Erreur getAllImpotBat"
            print err
            self.connection.rollback()
        return res


    def getAllImpotToPay(self, idcontribuable):
        cur = self.connection.cursor()
        self.restaApayerParAn.clear()
        allImpot = 0.0
        impotPaye = 0.0

        annee = datetime.datetime.now().strftime('%Y')
        anneanterieur = ()
        anneavant = int(annee)
        anneanterieur=anneanterieur + (str(anneavant),)
        for x in range(1, 4):
            anneavant = anneavant - 1
            anneanterieur = anneanterieur + (str(anneavant),)
        print 'annee ---------------------------------------------------------anterieur'
        #anneanterieur=str(anneanterieur)
        try:
            cur.execute("SELECT id, hetratrano::numeric, hetratany::numeric, etatpaiement, annee, montantpaye::numeric FROM public.impot_contribuable "
                        "WHERE idpersonne =  %s AND annee IN %s order by annee", (str(idcontribuable),anneanterieur))
            res = cur.fetchall()

            if res is not None:
                for re in res:
                    impotTotParAn = 0.0
                    impotPayeParAn = 0.0
                    if re[1] is not None:
                        allImpot = allImpot + float(re[1])
                        impotTotParAn = impotTotParAn + float(re[1])

                    if re[2] is not None:
                        allImpot = allImpot + float(re[2])
                        impotTotParAn = impotTotParAn + float(re[2])

                    if re[5] is not None:
                        impotPaye = impotPaye + float(re[5])
                        impotPayeParAn = impotPayeParAn + float(re[5])
                    self.restaApayerParAn[str(re[4])] = impotTotParAn - impotPayeParAn

            print "*******impots total et vita********"
            print allImpot
            print impotPaye
        except Exception as err:
            print "Erreur lecture impot"
            print err
            self.connection.rollback()

        return allImpot - impotPaye

    def getMontantPayePrec(self, idpersonne, annee):
        cur = self.connection.cursor()
        montantEx = 0.0
        try:
            cur.execute("SELECT montantpaye::numeric FROM impot_contribuable WHERE idpersonne = %s AND annee = %s", (idpersonne, annee))
            res = cur.fetchone()
            if res is not None:
                montantEx = float(res[0])
        except Exception as err:
            print "erreur maka montant farany"
            print err

        return montantEx







