# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from .DecisionAnnulation import Ui_Dialog

class DecisionAnnulation(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
#       print self.parent.txt
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        #self.connection = self.parent.connection
        #self.cur = self.parent.connection.cursor()
        self.ui.setupUi(self)
        self.initActions()
        self.idDecision = 0


    def initActions(self):

        validator = QtGui.QDoubleValidator()
        self.ui.lineEditNumDecision.setValidator(validator)
        self.ui.lineEditNumDecision.setValidator(validator)

        self.ui.dateEditDecision.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditDecision.setDate(QDate.currentDate())

        self.ui.btnAnnuler.clicked.connect(self.reject)
        self.ui.btnOk.clicked.connect(self.enregistrer)



    def enregistrer(self):
        print "enregistrer"
        if not self.check():
            return

        self.save()
        self.accept()


    def check(self):
        if self.ui.lineEditNumDecision.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir le champ Numero Decision")
            self.ui.lineEditNumDecision.setFocus(Qt.Qt.OtherFocusReason)
            return False
        return True


    def save(self):

        import time
        import datetime
        sql = "INSERT INTO decision" \
              "(numerodecision, typedecision,datedecision,idprojet) " \
              "values" \
              "(%s, %s, %s, %s)"

        numActe = int(self.ui.lineEditNumDecision.text())
        DecisionDu = str(self.ui.comboBoxDecisionDu.currentText())
        dateActe = self.ui.dateEditDecision.text()
        dateActes = dateActe.split('/')
        dateActess = datetime.date(int(dateActes[2]), int(dateActes[1]), int(dateActes[0]))
        idprojet = int(self.id_projet)



        # params = (numActe, dateEnreg,nomOfficier,valeur,nombreOperation,idprojet)
        params = (numActe, DecisionDu, dateActess, idprojet)
        print "PARAMS"
        print params
        cursor = self.connection.cursor()
        try:
            print "try in"
            cursor.execute(sql, params)
            print "try out"
            self.connection.commit()
            self.parent.showAll()
        except Exception as e:
            print e
            self.connection.rollback()
        cursor.close()





