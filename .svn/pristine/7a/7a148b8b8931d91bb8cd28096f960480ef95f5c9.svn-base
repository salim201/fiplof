# coding: utf8
import os, os.path, sys, datetime, time
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
import globalvars

from .montant import Ui_Dialog
from AreaConvert import AreaConvert

class montant(QDialog):
    def __init__(self, connection = None, montant = 0, idcontribuable = 0, parent = None):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setModal(True)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.montant = montant
        self.idcontribuable = idcontribuable
        self.ui.buttonBox.hide()
        self.parent = parent
        if self.montant != 0:
            self.ui.lineEdit.setText(str(self.montant))
        self.ui.comboBoxTypePaiement.currentIndexChanged.connect(self.updateMethodePaiement)
        #self.ui.buttonBox.accepted.connect(self.readValue)
        self.setWindowTitle(u"Montant payé")
        self.ui.label_2.setText(u"Numéro quittance")

        self.initActions()
        self.initMasks()

    def initActions(self):
        self.ui.pushButtonFermer.clicked.connect(self.close)
        #self.ui.pushButtonEnregistrer.connect(self.makeAll)

    def updateMethodePaiement(self):
        if self.ui.comboBoxTypePaiement.currentIndex() == 0:
            self.ui.lineEdit.setText(str(self.montant))
            self.ui.lineEdit.setReadOnly(True)
        else:
            self.ui.lineEdit.setReadOnly(False)
            self.ui.lineEdit.clear()

    def makeAll(self):
        if str(self.ui.lineEditNumEquitance.text()).strip() == "":
            QMessageBox.critical(None, "Erreur", "Le numero de quittance est obligatoire")
        else:
            if float(self.ui.lineEdit.text()) > self.montant:
                QMessageBox.critical(None, "Erreur", u"Montant superieure au total de l'impôt à payer")
            else:
                cur = self.connection.cursor()
                montant = float(self.ui.lineEdit.text())
                numquittance = str(self.ui.lineEditNumEquitance.text())
                dateJour = datetime.datetime.now().date()
                self.parent.valeurImpotPayee = float(montant)
                try:
                    cur.execute("INSERT INTO fi_paiement_impot (date, montant, numquittance, idpersonne) "
                                "VALUES(%s, %s, %s, %s)", (dateJour, montant, numquittance, str(self.idcontribuable)))
                    self.connection.commit()
                except Exception as err:
                    print "erreur insertion paiement"
                    print err

                self.close()

    def readValue(self):
        #print "read value"
        return self.ui.lineEdit.text()

    def readNumQuittance(self):
        return self.ui.lineEditNumEquitance.text()

    def readMontant(self):
        try:
            return float(self.ui.lineEdit.text())
        except:
            return 0.0

    def initMasks(self):
        validatorAlpha = QRegExpValidator(globalvars.regexpAlpha)
        validatorAlphaNum = QRegExpValidator(globalvars.regexpAlphaNum)
        validatorNum = QRegExpValidator(globalvars.regexpNum)

        self.ui.lineEdit.setValidator(validatorNum)
