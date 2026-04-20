# coding: utf-8
from PyQt4 import QtCore, QtGui
from PyQt4 import QtGui, Qt
import datetime
from popupInfos import Ui_INFORMATIONS
from Utilisateur import AccesManager

# create the dialog for qgsPlof  Qt.QDialog
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class popupInfosRun(Qt.QDialog):
    def __init__(self, parent):
        Qt.QDialog.__init__(self)
        self.parent = parent
        self.connection, self.canvas = self.parent.connection, self.parent.MainWindow.canvas
        self.newParcelleCF = True
        self.gid = self.parent.currentSelect
        self.ui = Ui_INFORMATIONS()
        self.ui.setupUi(self)
        self.ui.pushButtonCreateCert.setVisible(False)
        self.ui.pushButtonEditFisc.setVisible(False)
        self.ui.pushButtonCreateDemande.setVisible(False)
        self.registry = None
        self.iddemande = self.numDemande = self.dateDemande = self.idparcelle = None
        #MODIF SEPT 2023
        self.MainWindow = self.parent.MainWindow
        self.currentGeomIdParcelle = self.gid
        self.idparcelle = self.gid
        self.currvalDemande = self.gid
        self.id_projet = parent.id_projet
        self.geometryeEdit = 0
        self.stateEdition = 1
        self.geomid = self.gid
        self.tool = parent.tool
        self.iface = parent.iface
        self.Mcs = self.MainWindow
        self.idDemande = self.gid
        #FIN MODIF SEPT 2023
        self.getFeatureInfos()
        self.init_actions()

    def init_actions(self):
        manager = AccesManager.AccessManager(self, self.connection)
        manager.activate_widget("CERTIFICAT/CREATE", self.ui.pushButtonCreateCert)
        manager.activate_widget("IMPOT_FONCIER/CREATE", self.ui.pushButtonEditFisc)
        self.ui.pushButtonCreateCert.clicked.connect(self.create_certificat)
        self.ui.pushButtonEditFisc.clicked.connect(self.fisc_edit)
        self.ui.pushButtonCreateDemande.clicked.connect(self.create_demande)

    def getFeatureInfos(self):
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT pd.gid,pd.numdemande,d.datedemande,pd.surface,d.nomdemandeur,"
            "cf.numerocertificat,fkt.nomfokontany,hm.nomhameau,pd.codeparcelle,pd.estfiscalite"
            " FROM parcelle_d pd  "
            " LEFT JOIN demande d ON pd.gid = d.gid   "
            " LEFT JOIN certificat cf ON pd.idcertificat = cf.idcertificat  "
            " LEFT JOIN fokontany  fkt ON d.idfokontany = fkt.idfokontany "
            " LEFT JOIN hameau  hm     ON fkt.idfokontany = hm.idfokontany WHERE pd.gid=%s ", [int(self.gid)])
        dm = cursor.fetchone()
        if len(dm) >= 1:
            if dm[8]:
                self.ui.codeParcelle.setText("Code Parcelle : " + str(dm[8]))
                self.codeParcelle = str(dm[8]).strip()
            else:
                self.codeParcelle = ''
            self.ui.codeParcelle.setReadOnly(True)

            self.ui.numDemandeCF.setText("NUMDEMANDE : " + str(dm[1]))
            self.ui.numDemandeCF.setReadOnly(True)

            num_cf = str(dm[5]) if dm[5] is not None else ""
            self.ui.infos1.setText("NUMCERTIFICAT : " + num_cf)
            self.ui.infos1.setReadOnly(True)
            if not num_cf and dm[1] and not dm[9]:
                self.iddemande = dm[0]
                self.numDemande = str(dm[1])
                self.dateDemande = dm[2]
                self.ui.pushButtonCreateCert.setVisible(True)
            if dm[9]:
                self.idparcelle = dm[0]
                self.ui.pushButtonEditFisc.setVisible(True)
                self.ui.pushButtonEditFisc.setEnabled(not self.parent.ui.action_Connexion.isEnabled())

            if dm[1] is None:
                self.ui.pushButtonCreateDemande.setText("Remplir information")
                self.ui.pushButtonCreateDemande.setVisible(True)

            nom_demandeur = str(dm[4]) if dm[4] is not None else ""
            self.ui.infos2.setText("DEMANDEUR : " + str(nom_demandeur))
            self.ui.infos2.setReadOnly(True)

            surface = str(dm[3]) if dm[3] is not None else ""
            self.ui.infos3.setText("SURFACE : " + str(surface))
            self.ui.infos3.setReadOnly(True)

            fokontany = str(dm[6]) if dm[6] is not None else ""
            self.ui.infos5.setText("FOKONTANY : " + str(fokontany))
            self.ui.infos5.setReadOnly(True)

            hameau = str(dm[7]) if dm[7] is not None else ""
            self.ui.infos6.setText("HAMEAU : " + str(hameau))
            self.ui.infos6.setReadOnly(True)

    def create_certificat(self):
        from MultipleLayersEditNodesButton import MultipleLayersEditNodesButton
        self.parent.tool = MultipleLayersEditNodesButton(self.parent.iface, self.parent.MainWindow.canvas, self.parent)
        from Certificat.ChoixSurParcelleDmdRun import ChoixSurParcelleDmdRun
        choix = ChoixSurParcelleDmdRun(self.connection, self.canvas, self)
        if choix.creation.getEtatOpposition():
            reply = QtGui.QMessageBox.critical(self, "Erreur Opposition",
                                         u"Il existe encore des oppositions non résolues liées à cette demande")
            if reply == QtGui.QMessageBox.Ok:
                choix.close()
        else:
            n_jours = datetime.date.today() - self.dateDemande
            if n_jours.days > 15:
                choix.exec_()
            else:
                print "erreur"
                reply = QtGui.QMessageBox.critical(self, "Erreur",
                                             u"La date du jour doit être superieure à la  date de la demande d'au moins 15 jours !")
                if reply == QtGui.QMessageBox.Ok:
                    choix.close()

    def fisc_edit(self):
        self.registry = self.parent.registry
        from Fiplof.Saisie.InformationFiscaleRun import InformationFiscaleRun
        info_fisc = InformationFiscaleRun(self.connection, self, 1)
        if info_fisc.ui.comboCategorieParcelle.count() == 0 or info_fisc.ui.comboCategorieBatiment.count() == 0:
            QtGui.QMessageBox.critical(self, "Erreur",
                                 u"Veuillez d'abord configiurer les categories au niveau du menu Impot foncier > Paramètres > Catégories")
            return
        else:
            info_fisc.exec_()

    #def create_demande(self):
        #from Demande.DemandeDetailsRun import DemandeDetailsRun
        #demande = DemandeDetailsRun(self, False, True)
        #demande.exec_()

    def create_demande(self):
        from Demande.DemandeFormRun import DemandeFormRun
        demande = DemandeFormRun(self, True, self.codeParcelle)
        demande.exec_()