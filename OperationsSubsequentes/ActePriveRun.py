from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from .ActePrive import Ui_Dialog

class ActePrive(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
#       self.parent = parent
#       print self.parent.txt
        self.ui.setupUi(self)
        print "init"

        self.parent = parent
        self.details = self.parent.details
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        #       print self.parent.txt
        #self.ui.setupUi(self)
        self.initActions()

    def detailsActes(self):

        import time
        import datetime, globalvars
        import datetime
        from datetime import date

        if len(self.details) == 0:
            print
            "do not nothing"
        else:
            details = self.details
            self.ui.lineEditNumActe.setText(str(details[1]))
            dateEnreg = details[2].isoformat()
            year, month, day = details[2].isoformat().split("-")
            dateEnreg = date(int(year), int(month), int(day))
            self.ui.dateEditEnregistrement.setDate(dateEnreg)

            dateLegalisation = details[3].isoformat()
            year, month, day = details[3].isoformat().split("-")
            dateLegalisation = date(int(year), int(month), int(day))
            self.ui.dateEditEnregistrement.setDate(dateLegalisation)
            self.ui.lineEditValeurTransanction.setText(str(details[5]))
            #self.ui.spinBoxNombreOperations.setText(str(details[4]))

            self.ui.btnOk.setVisible(False)
            self.ui.btnAnnuler.setVisible(False)
            # self.ui.lineEditValeurTransanction.setText(details[6])
    def initActions(self):
        self.detailsActes()
        validator = QtGui.QDoubleValidator()
        #self.ui.lineEditNumActe.setValidator(validator)
        self.ui.lineEditValeurTransanction.setValidator(validator)

        self.ui.dateEditEnregistrement.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditEnregistrement.setDate(QDate.currentDate())

        self.ui.dateEditLegalisationSignature.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditLegalisationSignature.setDate(QDate.currentDate())

        self.ui.btnAnnuler.clicked.connect(self.reject)
        self.ui.btnOk.clicked.connect(self.enregistrer)
        self.ui.btnAide.setVisible(False)

    def enregistrer(self):
        print "enregistrer"
        if not self.check():
            return

        self.save()
        #self.accept()
        self.close()

    def check(self):
        if self.ui.lineEditNumActe.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditNumActe.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.dateEditEnregistrement.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.dateEditEnregistrement.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.dateEditLegalisationSignature.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.dateEditLegalisationSignature.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.lineEditValeurTransanction.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditValeurTransanction.setFocus(Qt.Qt.OtherFocusReason)
            return False

        return True

    def save(self):

        import time
        import datetime
        sql = "INSERT INTO acteprive" \
              "(numeroacteprive, dateenregistrement,datelegalisationsignature,valeurtransaction,nombreoperation,idprojet) " \
              "values" \
              "(%s, %s, %s, %s, %s, %s)"

        numActe = str(self.ui.lineEditNumActe.text()).strip()
        dateEnreg = self.ui.dateEditEnregistrement.text()
        dateEnregistrement = dateEnreg.split('/')
        dateEnreg = datetime.date(int(dateEnregistrement[2]), int(dateEnregistrement[1]), int(dateEnregistrement[0]))

        dateLegalisation = self.ui.dateEditLegalisationSignature.text()
        dateLegalisations = dateLegalisation.split('/')
        dL = datetime.date(int(dateLegalisations[2]), int(dateLegalisations[1]), int(dateLegalisations[0]))

        #nomOfficier = str(self.ui.lineEditNomOfficierPublic.text())
        valeur = int(self.ui.lineEditValeurTransanction.text())
        nombreOperation = int(self.ui.spinBoxNombreOperations.text())
        idprojet = int(self.id_projet)

        # params = (numActe, dateEnreg,nomOfficier,valeur,nombreOperation,idprojet)
        params = (numActe, dateEnreg,dL,valeur, nombreOperation, idprojet)
        # if self.id:
        #    sql = "UPDATE hameau SET nomhameau=%s, codehameau=%s ,idfokontany=%s " \
        #          " WHERE idhameau=%s"
        #    params = params + (self.id,)
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

