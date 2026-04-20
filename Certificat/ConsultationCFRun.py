from PyQt4.QtGui import *
from PyQt4.QtCore import *

from .ConsultationCF import Ui_Dialog
import time, datetime
import globalvars
from AreaConvert import AreaConvert
from Utils import Utils
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class ConsultationCFRun(QDialog):
    def __init__(self, connection, parent):
        QDialog.__init__(self)
        self.connection = connection
        self.utils = Utils(self.connection)
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Consultation de certificat foncier")
        self.initActions()
        self.initDB()
        self.initMasks()
        self.parent = parent
        self.numDemande = parent.numDemande
        self.idCF = None
        self.currentConsistance = None
        self.chargercategorie()
        #self.idCertificat = parent.idCertificat
        self.getCFById(parent.idCertificat)
        from .ConsultationProprietaireRun import ConsultationProprietaireRun
        self.proprietaires = ConsultationProprietaireRun(self.connection, parent.idCertificat)
        #from .ChargesRun import ChargesRun
        #self.charges = ChargesRun(self.connection)
        # self.setWindowTitle("Consultation d'un certificat foncier")
        self.ui.btnAide.hide()
        self.ui.btnHtml.hide()
        self.disableAll()


    def initActions(self):
        self.ui.btnProprietaire.clicked.connect(self.ouvrirProprio)
        self.ui.btnCharges.clicked.connect(self.ouvrirListeCharge)
        self.ui.btnRepere.clicked.connect(self.ouvrirLimites)
        self.ui.btnDetailDmd.clicked.connect(self.ouvrirDemande)
        self.ui.btnFermer.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.ouvrirOperations)
        self.ui.pushButton_3.clicked.connect(self.ouvrirHistorique)
        self.ui.btnFiscaliser.clicked.connect(self.fiscaliserCF)

    def chargercategorie(self):

        sql = "SELECT idconsistance,libelleconsistance FROM consistance"
        self.utils.fillComboWithSql(self.ui.comboBoxConsist, sql, "libelleconsistance", "idconsistance")

    def ouvrirProprio(self):
        print "proprio"
        self.proprietaires.show()
        result = self.proprietaires.exec_()


    def ouvrirListeCharge(self):
        print "charges"
        #self.charges.setDisabled(True)
        from .ConsultationChargesRun import ConsultationChargesRun
        self.charges = ConsultationChargesRun(self.connection, self.parent.idCertificat)
        self.charges.show()
        result = self.charges.exec_()

    def ouvrirLimites(self):
        from .ConsultationLimitesRun import ConsultationLimitesRun
        self.listeLimite = ConsultationLimitesRun(self.connection, self.parent.idCertificat)
        self.listeLimite.show()
        result = self.listeLimite.exec_()

    def ouvrirDemande(self):
        print "demande"
        from Demande.DetailsDemandeRunn import DetailsDemandeRunn
        self.consDemande = DetailsDemandeRunn(self.parent)
        #self.consDemande = DetailsDemandeRunn(parent))
        self.consDemande.show()
        result = self.consDemande.exec_()

    def ouvrirOperations(self):
        from .OperationRun import OperationRun
        self.operation = OperationRun(self.connection, self)
        self.operation.show()
        result = self.operation.exec_()

    def ouvrirHistorique(self):
        from .HistoriqueRun import HistoriqueRun
        self.historique = HistoriqueRun(self.connection, self)
        self.historique.show()
        result = self.historique.exec_()

    def initDB(self):
        self.cur = self.connection.cursor()
        # revenir au fichier de depart

    def getCFById(self, idCF):
        print(idCF)
        self.cur.execute("SELECT c.typecertificat, c.numerocertificat, c.numerodemande,  d.consistance, "
                         " p.etat, c.datereconnaissance,"
                         " c.dateedition, c.datedelivrance, p.gid, p.idhameau, ST_Area(p.geom),"
                         " p.estfiscalite, d.categorie "
                         " FROM certificat c, parcelle_d p  "
                         " INNER JOIN demande d ON d.gid = p.gid "
                         " WHERE p.idcertificat = c.idcertificat AND c.idcertificat = %s", (idCF,))
        result = self.cur.fetchone()
        print
        print("RESULT in FROM  ")
        print result
        print("RESULT  out FROM  ")
        self.idCF = idCF

        self.fillFields(result)
        self.fillTerritoire(result[8])
        # Vider les combobox
        self.ui.comboBoxFokontany.clear()
        self.ui.comboBoxHameau.clear()
        if result[10] is not None:
            surfacem2 = round(result[10], 2)
            self.ui.lineEditSurface.setText(str(surfacem2))
            ac = AreaConvert()
            # Area = ac.convertArea(float(data[4]), 'sqmeter', 'Ha')
            Area = ac.convertArea(float(result[10]))
            print Area
            self.ui.lineEditHa.setText(str(Area['Ha']))
            self.ui.lineEditA.setText(str(Area['a']))
            self.ui.lineEditCa.setText(str(Area['Ca']))
        if result[9]  is not None:

            self.fillHameau(result[9])
        if result[11] is not None and result[11] == 1:
            self.ui.btnFiscaliser.hide()
        try:
            self.ui.lineEditEtat.setText(str(result[3]))
            cursor = self.connection.cursor()
            # self.connection.cursor()
            cursor.execute("SELECT *   FROM consistance  WHERE libelleconsistance=%s", [str(result[12])])
            print("DATA FROM CONSISTANCE")
            dm = cursor.fetchone()
            print(dm)
            self.utils.setComboValue(self.ui.comboBoxConsist, int(dm[0]))
        except StandardError as e:
            print e
        #print result

    def fillHameau(self, idhameau):
        # Hameaux
        self.cur.execute("SELECT h.nomhameau, h.idhameau, h.idfokontany, f.nomfokontany FROM hameau h, fokontany f WHERE h.idfokontany = f.idfokontany AND h.idhameau = %s", (idhameau,))
        hmx = self.cur.fetchone()
        try:
            self.ui.comboBoxHameau.addItem(hmx[0], hmx[1])
            # Determiner le fokontany
            self.ui.comboBoxFokontany.addItem(hmx[3], hmx[2])
        except StandardError as e:
            print e



    def fillFields(self, data):
        self.clearAll()
        try:

            if data[0]:
                self.ui.comboBoxTypeCert.addItem(data[0])
            if data[1]:
                self.ui.lineEditNumCert.setText(data[1].strip())
            if data[2]:
                self.ui.lineEditNumDmd.setText(data[2])
        except StandardError as e:
            print e

        if data[3]:
            self.currentConsistance = data[3]


        try:
            if data[4]:
                self.ui.lineEditEtat.setText(data[3])
            if data[5]:
                self.ui.lineEditDateReconnaissance.setText(data[5].strftime('%d/%m/%Y'))
            if data[6]:
                self.ui.lineEditEdition.setText(data[6].strftime('%d/%m/%Y'))
            if data[7]:
                self.ui.lineEditDelivrance.setText(data[7].strftime('%d/%m/%Y'))
        except StandardError as e:
            print e

    def fillConsistance(self):
        self.idsConsistance[:] = []
        self.ui.comboBoxConsist.clear()
        try:
            self.cur.execute("SELECT idconsistance, libelleconsistance FROM consistance")
            consistances = self.cur.fetchall()
            for consistance in consistances:
                print consistance[1]
                self.ui.comboBoxConsist.addItem(consistance[1])
                self.idsConsistance.append(consistance[0])
        except StandardError as e:
            print e

        if self.ui.comboBoxConsist.count() > 0:
            if self.currentConsistance is not None:
                print self.ui.comboBoxConsist.findText(self.currentConsistance)
                self.ui.comboBoxConsist.setCurrentIndex(self.ui.comboBoxConsist.findText(self.currentConsistance))


    def fillTerritoire(self, idParcelle):
        # Recuperer le nom de la commune
        try:
            self.cur.execute("SELECT nomcommune, codecommune FROM commune WHERE idcommune = %s", (globalvars.id_commune, ))
            com = self.cur.fetchone()
            self.ui.comboBoxCommune.addItem(com[0])
        except StandardError as e:
            print e
        # Recuperer le district
        try:
            self.cur.execute("SELECT d.nomdistrict, d.iddistrict, d.codedistrict FROM district d, commune c WHERE d.iddistrict = c.iddistrict AND c.idcommune = %s", (globalvars.id_commune, ))
            dist = self.cur.fetchone()
            self.ui.comboBoxDistrict.addItem(dist[0])
        except StandardError as e:
            print e
        # Region
        try:
            self.cur.execute("SELECT r.nomregion FROM region r, district d WHERE d.idregion = r.idregion AND d.iddistrict = %s", (dist[1],))
            reg = self.cur.fetchone()
            self.ui.comboBoxRegion.addItem(reg[0])
        except StandardError as e:
            print e

        #try:
        #    self.cur.execute("SELECT nomfokontany, idfokontany FROM fokontany WHERE idcommune = %s",(globalvars.id_commune, ) )
        #    fkts = self.cur.fetchall()
        #    for fkt in fkts:
        #        self.ui.comboBoxFokontany.addItem(fkt[0], fkt[1])
        #except StandardError as e:
        #    print e
        #print "apres fokontany"
        #Hameaux
        #self.cur.execute("SELECT h.nomhameau, h.idhameau FROM hameau h, fokontany f WHERE h.idfokontany = f.idfokontany AND f.idfokontany = %s", (fkt[1],))
        #hmx = self.cur.fetchall()
        #for hm in hmx:
        #    self.ui.comboBoxHameau.addItem(hm[0], hm[1])
        #print "apres hameau"

    def clearAll(self):
        self.ui.comboBoxTypeCert.clear()
        self.ui.comboBoxHameau.clear()
        self.ui.comboBoxFokontany.clear()
        self.ui.comboBoxCommune.clear()
        self.ui.comboBoxDistrict.clear()
        self.ui.comboBoxRegion.clear()

    def disableAll(self):
        self.ui.comboBoxRegion.setDisabled(True)
        self.ui.comboBoxDistrict.setDisabled(True)
        self.ui.comboBoxCommune.setDisabled(True)
        self.ui.comboBoxFokontany.setDisabled(True)
        self.ui.comboBoxHameau.setDisabled(True)
        self.ui.comboBoxConsist.setDisabled(True)
        self.ui.comboBoxTypeCert.setDisabled(True)
        self.ui.lineEditDelivrance.setReadOnly(True)
        self.ui.lineEditEdition.setReadOnly(True)
        self.ui.lineEditDateReconnaissance.setReadOnly(True)
        self.ui.lineEditEtat.setReadOnly(True)
        self.ui.lineEditNumDmd.setReadOnly(True)
        self.ui.lineEditNumCert.setReadOnly(True)
        self.ui.lineEditInscriptionReg.setReadOnly(True)
        self.ui.lineEditA.setReadOnly(True)
        self.ui.lineEditCa.setReadOnly(True)
        self.ui.lineEditHa.setReadOnly(True)
        self.ui.lineEditSurface.setReadOnly(True)

    def fiscaliserCF(self):
        from Fiplof.Saisie.InformationFiscaleRun import InformationFiscaleRun
        isFiscalisation = True
        infofisc = InformationFiscaleRun(self.connection, self.parent, None, isFiscalisation)
        data = []
        data[:] = []
        data.append(self.ui.lineEditNumCert.text())
        data.append(self.ui.lineEditNumDmd.text())
        data.append(self.idCF)
        infofisc.initExtraData(data, 1)
        infofisc.exec_()

    def __del__(self):
        self.cur.close()

    def initMasks(self):
        validatorNumCertificat = QRegExpValidator(globalvars.regexpNumCertificat)
        self.ui.lineEditNumCert.setValidator(validatorNumCertificat)