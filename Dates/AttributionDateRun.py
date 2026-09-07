# coding: utf-8
from PyQt4.QtGui import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QApplication
from qgis.core import *
from qgis.gui import *
import datetime, time
import globalvars
import os
import webbrowser
import tempfile
from random import randint
from AreaConvert import AreaConvert
from Utils import Utils
from attribution_date import Ui_Dialog
from models.Demande import Demande
from models.RoleCrl import RoleCrl
from  role_crlRun import role_crlRun

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class AttributionDateRun(QDialog):
#    def __init__(self, connection, canvas, parent):
    def __init__(self, connection, canvas, parent,slf = None):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.canvas = canvas
        self.idparcelle = None
        self.numDemandes = []
        self.numCF = None
        self.parent = parent
        self.setWindowTitle(u"Attribution des dates aux demandes")
        self.idsFokontany = []
        self.idsHameau = []
        self.initDB()
        self.initActions()
        self.numdecision=None
        self.datedecision=None
        self.iddemande = None
        self.numDemande=None
        self.alldmdselected=[]
        self.isUpdate = False
        self.debutaffichage = None
        self.finaffichage = None
        self.datereconnaissance=None
        self.datedemande=None
        self.ligne=0
        from Dates.role_crlRun import role_crlRun
        self.framecrl = role_crlRun(self, self.connection, 0)
        self.framecrl.ui.pushButton.clicked.connect(self.ajoutclr)
        self.framecrl.ui.lineEditTitulaire.setText("")
        self.framecrl.ui.lineEditSuppleant.setText("")
        self.listcrl = []

    def initDB(self):
        self.cur = self.connection.cursor()

    def initActions(self):
        self.ui.checkBoxNumDemande.clicked.connect(self.changeFieldsStatus)
        self.ui.checkBoxHameau.stateChanged.connect(self.chargeHameau)
        self.ui.checkBoxFkt.stateChanged.connect(self.chargeFKT)
        self.ui.comboBoxFokontany.currentIndexChanged.connect(self.changeFKT)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercher)
        self.ui.pushButtonAttribuerDate.clicked.connect(self.attribuerDate)
        self.ui.tableWidgetDemande.setColumnWidth(0, 25)
        self.ui.tableWidgetDemande.setColumnWidth(1, 110)
        self.ui.tableWidgetDemande.setColumnWidth(2, 110)
        self.ui.tableWidgetDemande.setColumnWidth(3, 110)
        self.ui.tableWidgetDemande.setColumnWidth(4, 110)
        self.ui.tableWidgetDemande.setColumnWidth(5, 140)
        self.ui.tableWidgetDemande.setColumnWidth(6, 100)
        self.ui.tableWidgetDemande.setColumnWidth(7, 100)
        self.ui.tableWidgetDemande.setColumnWidth(8, 100)
        self.ui.tableWidgetDemande.setColumnWidth(9, 60)
        self.ui.tableWidgetCRL.setColumnWidth(0, 250)
        self.ui.tableWidgetCRL.setColumnWidth(1, 300)
        self.ui.tableWidgetCRL.setColumnWidth(2, 300)
        self.ui.tableWidgetDemande.itemClicked.connect(self.handleItemClicked)
        self.ui.checkBoxCocherTous.stateChanged.connect(self.cocherTout)
        self.ui.toolButtonAjouter.clicked.connect(self.openajouterCRL)
        self.ui.pushButtonAssigner.clicked.connect(self.assignerCRL)
        self.ui.toolButtonSupprimer.clicked.connect(self.supprimerCRL)
        self.ui.pushButtonRechercher.setStyleSheet(
            "QPushButton" "{" "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #a6d5e5, stop: 1 #a6d5e5)" "}")
        self.ui.pushButtonAttribuerDate.setStyleSheet(
            "QPushButton" "{" "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #a6d5e5, stop: 1 #a6d5e5)" "}")
        self.ui.pushButtonAssigner.setStyleSheet(
            "QPushButton" "{" "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #a6d5e5, stop: 1 #a6d5e5)" "}")
        #self.ui.tableWidgetDemande.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.ui.groupBoxAffichage.toggled.connect(self.status_Affichage)
        self.ui.groupBoxdateRL.toggled.connect(self.status_RL)
        self.ui.groupBoxDemande.toggled.connect(self.status_Demande)
        self.ui.groupBoxDecision.toggled.connect(self.status_Decision)

    def changeFieldsStatus(self):
        self.ui.lineEditNumeroDemande.setEnabled(self.ui.checkBoxNumDemande.isChecked())
        self.ui.comboBoxFokontany.setEnabled(self.ui.checkBoxFkt.isChecked())
        self.ui.comboBoxHameau.setEnabled(self.ui.checkBoxHameau.isChecked())

    def param_status_desable(self):
        self.ui.groupBoxDecision.setChecked(False)
        self.ui.groupBoxAffichage.setChecked(False)
        self.ui.groupBoxdateRL.setChecked(False)
        self.ui.groupBoxDemande.setChecked(False)

    def status_Demande(self):
        if self.ui.groupBoxDemande.isChecked():
            #print "groupBoxDemande"
            self.ui.groupBoxAffichage.setChecked(False)
            self.ui.groupBoxdateRL.setChecked(False)
            self.ui.groupBoxDecision.setChecked(False)

    def status_Decision(self):
        if self.ui.groupBoxDecision.isChecked():
            #print "groupBoxDecision"
            self.ui.groupBoxAffichage.setChecked(False)
            self.ui.groupBoxdateRL.setChecked(False)
            self.ui.groupBoxDemande.setChecked(False)

    def status_Affichage(self):
        if self.ui.groupBoxAffichage.isChecked():
            #print "groupBoxAffichage"
            self.ui.groupBoxDecision.setChecked(False)
            self.ui.groupBoxdateRL.setChecked(False)
            self.ui.groupBoxDemande.setChecked(False)

    def status_RL(self):
        if self.ui.groupBoxdateRL.isChecked():
            print "groupBoxdateRL"
            self.ui.groupBoxDecision.setChecked(False)
            self.ui.groupBoxAffichage.setChecked(False)
            self.ui.groupBoxDemande.setChecked(False)


    def assignerCRL(self):
        print "assigner"
        try:
            self.lisCRL()
            self.listiddmdselected()
            if len(self.alldmdselected)==0 :
                QMessageBox.critical(self, "Erreur", u"Aucune demande selectionnée",
                                     u"veuillez selectionner les demandes!")
                return

            total = len(self.alldmdselected) * len(self.listcrl)
            if total == 0:
                QMessageBox.critical(self, "Erreur", u"Aucun membre CRL à assigner",
                                     u"veuillez ajouter des membres CRL!")
                return

            progress = QProgressDialog(u"Assignation des CRL en cours...", None, 0, total, self)
            progress.setWindowTitle(u"Assignation CRL")
            progress.setModal(True)
            progress.show()

            insertOK = False
            count = 0
            for oneiddmdselected in self.alldmdselected:
                data = []
                try :
                    self.iddemande = int(self.ui.tableWidgetDemande.item(oneiddmdselected, 1).text())
                    for rowcrl in self.listcrl :
                        QApplication.processEvents()
                        if progress.wasCanceled():
                            return
                        progress.setValue(count)
                        count += 1
                        data.append(self.iddemande)
                        for info in rowcrl:
                            if info=='titulaire':
                                data.append(True)
                            else:
                                if info=='suppleant':
                                    data.append(False)
                                else :
                                    data.append(info)
                        try:
                            data.append(False)  # president
                            RoleCrlModel = RoleCrl(self.connection)
                            res = RoleCrlModel.insert_role(data)
                            data = []
                            insertOK = True
                        except Exception as e:
                            print(e)
                            insertOK = False
                            QMessageBox.critical(self, "Erreur", u"erreur d'enregistrement des crl des demandes",
                                                 u"veuillez selectionner les demandes!")

                except Exception as e:
                    print(e)
                    progress.close()
                    return
            progress.setValue(total)
            progress.close()
            if insertOK :
                QMessageBox.information(self, "INFO",
                                        u"Insertion ou mise à jour CRL réussie!")
            else :
                QMessageBox.critical(self, "Erreur", u"une erreur s'est produite, veuillez vérifier les saisis!")
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Erreur", u"Une erreur inattendue est survenue: %s" % str(e))


    def lisCRL(self):
        self.listcrl=[]
        allrow = self.ui.tableWidgetCRL.rowCount()
        for i in range(0, allrow):
            rolecrl = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetCRL, i, 0)
            if len(rolecrl) != 0:
                RoleCrlModel = RoleCrl(self.connection)
                role = RoleCrlModel.find_by_lib(rolecrl)
                if role is None:
                    print u"Rôle CRL introuvable: %s" % rolecrl
                    continue
                idperstitulaire = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetCRL, i, 3)
                idperssupleant = Utils.getTableWidgetCellStrValue(self.ui.tableWidgetCRL, i, 4)
                if int(idperstitulaire)>0:
                    self.listcrl.append([int(role[0]), int(idperstitulaire), 'titulaire'])
                if int(idperssupleant)>0:
                    self.listcrl.append([int(role[0]), int(idperssupleant), 'suppleant'])
        print '---------DEBUT Liste CRL-------------'
        print self.listcrl
        print '---------FIN Liste CRL-------------'


    def supprimerCRL(self):
        print '-------ato amin ny supprimer CRL---'
        idrow=self.ui.tableWidgetCRL.currentRow()
        self.ui.tableWidgetCRL.removeRow(idrow)

    def ajoutclr(self):
        print "ajoutclr"
        try :
            self.ligne = self.ui.tableWidgetCRL.rowCount()
            self.ui.tableWidgetCRL.insertRow(self.ligne)
            self.ui.tableWidgetCRL.setItem(self.ligne, 0,QtGui.QTableWidgetItem(str(self.framecrl.crlrole)))
            self.ui.tableWidgetCRL.setItem(self.ligne, 1, QtGui.QTableWidgetItem(str(self.framecrl.crltitulaire)))
            self.ui.tableWidgetCRL.setItem(self.ligne, 2, QtGui.QTableWidgetItem(str(self.framecrl.crlsuppleant)))
            self.ui.tableWidgetCRL.setItem(self.ligne, 3, QtGui.QTableWidgetItem(str(globalvars.idpersrolTitulaire)))
            self.ui.tableWidgetCRL.setItem(self.ligne, 4, QtGui.QTableWidgetItem(str(globalvars.idpersrolSupleant)))
            self.ligne=self.ligne+1
            self.framecrl.close()
        except Exception as e:
            print(e)
            return

    def openajouterCRL(self):
        #self.ui.tableDemande.removeRow(self.selectedRow)
        print "ajouter e"
        self.framecrl.ui.lineEditTitulaire.setText("")
        self.framecrl.ui.lineEditSuppleant.setText("")
        globalvars.idpersrolTitulaire=0
        globalvars.idpersrolSupleant=0
        self.framecrl.crltitulaire=""
        self.framecrl.crlsuppleant=""
        try :
            self.framecrl.exec_()
        except Exception as err:
            print err
            return

    def handleItemClicked(self, item):
        #récupération ligne coché
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

    def listiddmdselected(self):
        self.alldmdselected = []
        for j in range(self.ui.tableWidgetDemande.rowCount()):
            items = self.ui.tableWidgetDemande.item(j, 0)
            if items.checkState() == QtCore.Qt.Checked:
                self.alldmdselected.append(j)
        print self.alldmdselected

    def attribuerDate(self):
        #attribuer les informations de la décision d'une ou plusieurs demandes
        self.listiddmdselected()
        print 'attribute date'
        if self.ui.groupBoxDemande.isChecked()==True and self.ui.groupBoxDecision.isChecked()==False and self.ui.groupBoxAffichage.isChecked()==False and self.ui.groupBoxdateRL.isChecked()==False:
            self.attributeDateDemande()
        if self.ui.groupBoxDecision.isChecked()== True and self.ui.groupBoxDemande.isChecked()==False and self.ui.groupBoxAffichage.isChecked()==False and self.ui.groupBoxdateRL.isChecked()==False:
            self.attributeDecision()
        if self.ui.groupBoxAffichage.isChecked()==True and self.ui.groupBoxDemande.isChecked()==False and self.ui.groupBoxDecision.isChecked()==False and self.ui.groupBoxdateRL.isChecked()==False:
            self.attributeAffichage()
        if self.ui.groupBoxdateRL.isChecked()==True and self.ui.groupBoxDemande.isChecked()==False and self.ui.groupBoxDecision.isChecked()==False and self.ui.groupBoxAffichage.isChecked()==False:
            print 'check'
            self.attributeDateRL()

        self.rechercher()
        self.param_status_desable()

    def attributeDateDemande(self):
        print 'datedemande'
        self.datedemande= datetime.date(self.ui.dateDemande.date().year(),
                                                self.ui.dateDemande.date().month(),
                                                self.ui.dateDemande.date().day())
        for onerow in self.alldmdselected:
            print onerow
            self.iddemande = int(self.ui.tableWidgetDemande.item(onerow, 1).text())
            numdemande= str(self.ui.tableWidgetDemande.item(onerow, 3).text()).strip()
            if numdemande != "":
                print "num demande"
                if (self.updatedateDemande()):
                    self.isUpdate = True
            else :
                QMessageBox.critical(self, "Erreur",
                                         u"Numero demande inexistant!")
                return
        if self.isUpdate:
            QMessageBox.information(self, "INFO",
                                    u"Mise à jour date de Demande réussie!")

    def attributeDecision(self):
        print 'decision'
        # récuperation info
        self.numdecision = str(self.ui.lineEditNumeroDecision.text()).strip()
        self.datedecision = datetime.date(self.ui.dateEditDateDecision.date().year(),
                                          self.ui.dateEditDateDecision.date().month(),
                                          self.ui.dateEditDateDecision.date().day())
        for onerow in self.alldmdselected:
            print onerow
            self.iddemande = int(self.ui.tableWidgetDemande.item(onerow, 1).text())
            print self.iddemande
            if (self.updateinfoDecision()):
                self.isUpdate = True
        if self.isUpdate:
            QMessageBox.information(self, "INFO",
                                    u"Mise à jour date de decision réussie!")

    def attributeAffichage(self):
        print 'attribute affichage'
        # récuperation info
        isUpdate = False
        self.debutaffichage = datetime.date(self.ui.dateEditDebutAffichage.date().year(),
                                            self.ui.dateEditDebutAffichage.date().month(),
                                            self.ui.dateEditDebutAffichage.date().day())
        self.finaffichage = datetime.date(self.ui.dateEditFinAffichage.date().year(),
                                          self.ui.dateEditFinAffichage.date().month(),
                                          self.ui.dateEditFinAffichage.date().day())
        if (self.finaffichage-self.debutaffichage).days<15:
            QMessageBox.critical(self, "Erreur",
                                 u"Veuillez verifier les dates affichages: periode affichage 15j!")
            return
        for onerow in self.alldmdselected:
            self.iddemande = int(self.ui.tableWidgetDemande.item(onerow, 1).text())
            datedecision = str(self.ui.tableWidgetDemande.item(onerow, 5).text()).strip()
            print 'datedecision'
            print len(datedecision)
            print 'fin datedecision'
            if len(datedecision)!=0:
                print 'non vide'
                datedecision = datetime.datetime.strptime(datedecision, '%Y-%m-%d')
                datedecision=datedecision.date()
                delta = self.debutaffichage - datedecision
                if delta.days>=0 :
                    if (self.updateinfoAffichage()):
                        isUpdate = True
                else:
                    QMessageBox.critical(self, "Erreur",u"Une anomalie.Date debut affichage anterieur a la date decision!")
                    return
            else:
                QMessageBox.critical(self, "Erreur",u"Une demande avec une date de decision vide veuillez verifier votre selection!")
                return
        if isUpdate:
            QMessageBox.information(self, "INFO",u"Mise à jour info affichage réussie!")
        else :
            QMessageBox.critical(self, "Erreur",u"Une anomalie.Veuillez contacter votre administrateur!")

    def attributeDateRL(self):
        print 'date rl'
        self.isUpdate = False
        self.datereconnaissance = datetime.date(self.ui.dateEditRL.date().year(),
                                                self.ui.dateEditRL.date().month(),
                                                self.ui.dateEditRL.date().day())
        for onerow in self.alldmdselected:
            print onerow
            self.iddemande = int(self.ui.tableWidgetDemande.item(onerow, 1).text())
            dateaffichage = str(self.ui.tableWidgetDemande.item(onerow, 6).text()).strip()
            if len(dateaffichage) != 0:
                print "date affichage"
                if (self.updatedateRL()):
                    self.isUpdate = True
            else :
                QMessageBox.critical(self, "Erreur",
                                         u"Une demande n'a pas de date affichage!")
                return
        if self.isUpdate:
            QMessageBox.information(self, "INFO",
                                    u"Mise à jour date de RL réussie!")

    def updatedateRL(self):
        print 'updatedateRL'
        try:
            if (Demande.updatedateRL(self, self.connection)):
                return True
            else:
                QMessageBox.critical(self, "Erreur",
                                     u"Une exception. Veuillez contacter votre administrateur!")
                return False
        except Exception as err:
            QMessageBox.critical(self, "Une exeption",
                                 u"Une exception. Veuillez contacter votre administrateur!")
            return

    def updatedateDemande(self):
        print 'updatedateDemande'
        try:
            if (Demande.updatedatDemande(self, self.connection)):
                return True
            else:
                QMessageBox.critical(self, "Erreur",
                                     u"Une exception. Veuillez contacter votre administrateur!")
                return False
        except Exception as err:
            QMessageBox.critical(self, "Une exeption",
                                 u"Une exception. Veuillez contacter votre administrateur!")
            return

    def updateinfoDecision(self):
        #méthode information sur la décision dans la table demande
        try:
            if (Demande.updateDecision(self,self.connection)):
                return True
            else:
                QMessageBox.critical(self, "Erreur",
                                     u"Une exception. Veuillez contacter votre administrateur!")
                return False
        except Exception as err:
            QMessageBox.critical(self, "Une exeption",
                                 u"Une exception. Veuillez contacter votre administrateur!")
            return

    def updateinfoAffichage(self):
        print "updateinfoAffichage"
        #méthode information sur l'affichagen dans la table demande
        try:
            if (Demande.updateAffichage(self,self.connection)):
                return True
            else:
                QMessageBox.critical(self, "Erreur",
                                     u"Une exception. veuillez contacter votre administrateur!")
                return False
        except Exception as err:
            QMessageBox.critical(self, "Une exeption",
                                 u"Une exception. veuillez contacter votre administrateur!")
            return

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
        SQL = "SELECT d.iddemande,d.datedemande, d.numdemande,d.numdecision,d.datedecision, d.debut_affichage, d.fin_affichage ,d.datereconnaissance, d.cqe FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid  "
        firstOne = True
        #print SQL
        if self.ui.checkBoxFkt.isChecked():
            SQL="SELECT d.iddemande,d.datedemande, d.numdemande,d.numdecision,d.datedecision, d.debut_affichage, d.fin_affichage ,d.datereconnaissance, d.cqe ,f.idfokontany ,f.nomfokontany" \
                " FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid" \
                " INNER JOIN fokontany f on d.idfokontany=f.idfokontany"
            if self.ui.checkBoxHameau.isChecked():
                SQL=" SELECT d.iddemande,d.datedemande, d.numdemande,d.numdecision,d.datedecision, d.debut_affichage,d.datereconnaissance, d.cqe , d.fin_affichage,f.idfokontany ,f.nomfokontany,h.idhameau,h.nomhameau" \
                    " FROM demande d INNER JOIN parcelle_d pd ON d.gid = pd.gid " \
                    " INNER JOIN fokontany f on d.idfokontany=f.idfokontany" \
                    " INNER JOIN hameau h on h.idhameau=pd.idhameau"

        if not self.ui.checkBoxNumDemande.isChecked() and not self.ui.checkBoxFkt.isChecked() and not self.ui.checkBoxHameau.isChecked():
            QMessageBox.critical(None, "Erreur", u"Aucun critère de recherche! Il faut choisir un critère de recherche en cochant l'une des cases à cocher avant de cliquer sur le bouton rechercher")
            return

        if self.ui.checkBoxNumDemande.isChecked():
            numDemandeBrut = str(self.ui.lineEditNumeroDemande.text()).strip()
            if numDemandeBrut == "":
                QMessageBox.critical(None, "Erreur", u"Numero demande non renseigné!")
                return
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
            print nfokontany
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
            print nhameau
            listeParams.append(nhameau)
            if firstOne == True:
                firstOne = False
                SQL = SQL + " WHERE nomhameau = %s "
            else:
                SQL = SQL + " AND nomhameau = %s "

        idcommune = globalvars.id_commune
        listeParams.append(idcommune)
        if firstOne == True:
            firstOne = False
            SQL = SQL + " WHERE d.idcommune  = %s "
        else:
            SQL = SQL + " AND d.idcommune = %s "
        print SQL

        print listeParams
        SQL=SQL+" order by d.iddemande ASC"
        print SQL
        try:
            print "ato"
            self.cur.execute(SQL,listeParams)
            rows = self.cur.fetchall()
            print rows
            self.ui.tableWidgetDemande.setRowCount(len(rows))
            for i,r in enumerate(rows):
                print r[0]
                if r[1] is None: datedemande = ""
                else: datedemande = str(r[1])
                if r[2] is None: numdemande = ""
                else: numdemande = str(r[2])
                if r[3] is None: numdecision = ""
                else: numdecision = str(r[3])
                if r[4] is None: datedecision = ""
                else: datedecision = str(r[4])
                if r[5] is None: datedebutaffichage = ""
                else: datedebutaffichage = str(r[5])
                if r[6] is None: datefinaffichage = ""
                else: datefinaffichage = str(r[6])
                if r[7] is None: datereconnaissance = ""
                else: datereconnaissance = str(r[7])
                item = QtGui.QTableWidgetItem(True)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(False)
                self.ui.tableWidgetDemande.setItem(i, 0, item)
                self.ui.tableWidgetDemande.setItem(i, 1, QtGui.QTableWidgetItem(str(r[0])))
                self.ui.tableWidgetDemande.setItem(i, 2, QtGui.QTableWidgetItem(datedemande))
                self.ui.tableWidgetDemande.setItem(i, 3, QtGui.QTableWidgetItem(numdemande))
                self.ui.tableWidgetDemande.setItem(i, 4, QtGui.QTableWidgetItem(numdecision))
                self.ui.tableWidgetDemande.setItem(i, 5, QtGui.QTableWidgetItem(datedecision))
                self.ui.tableWidgetDemande.setItem(i, 6, QtGui.QTableWidgetItem(datedebutaffichage))
                self.ui.tableWidgetDemande.setItem(i, 7, QtGui.QTableWidgetItem(datefinaffichage))
                self.ui.tableWidgetDemande.setItem(i, 8, QtGui.QTableWidgetItem(datereconnaissance))
                self.ui.tableWidgetDemande.setItem(i, 9, QtGui.QTableWidgetItem("NON"))
        except Exception as e:
            print(e)
            self.connection.rollback()
            #self.cur.close()

    def prepareNumDemande(self, numDmdBrut):
        numDmdIntermed = numDmdBrut.split(',')
        #print numDmdIntermed
        return numDmdIntermed

