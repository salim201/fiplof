from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from .ActePublic import Ui_Dialog

class ActePublic(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        print "init"
        self.parent = parent
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
        self.details = self.parent.details
#       print self.parent.txt
        self.ui.setupUi(self)
        self.initActions()

    def detailsActes(self):

        import time
        import datetime, globalvars
        import datetime
        from datetime import date

        if len(self.details) == 0:
            print "do not nothing"
        else:
            print " SELF.DETAILS "
            print self.details
            details = self.details
            print details
            self.ui.lineEditNumActe.setText(str(details[5]))
            dateEnreg = details[1].isoformat()
            year, month, day = details[1].isoformat().split("-")
            dateEnreg = date(int(year), int(month), int(day))
            self.ui.dateEditEnregistrement.setDate(dateEnreg)
            self.ui.lineEditNomOfficierPublic.setText(details[2])
            self.ui.btnOk.setVisible(False)
            self.ui.btnAnnuler.setVisible(False)

           # self.ui.lineEditValeurTransanction.setText(details[6])

    def initActions(self):
        self.detailsActes()
        validator = QtGui.QDoubleValidator()
        #self.ui.lineEditNumActe.setValidator(validator)
        self.ui.lineEditValeurTransanction.setValidator(validator)
        self.ui.btnAide.setVisible(False)

        self.ui.dateEditEnregistrement.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditEnregistrement.setDate(QDate.currentDate())

        self.ui.btnAnnuler.clicked.connect(self.reject)
        self.ui.btnOk.clicked.connect(self.enregistrer)

    def enregistrer(self):
        if not self.check():
            return

        self.save()
        self.accept()

    def check(self):
        if self.ui.lineEditNumActe.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditNumActe.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.dateEditEnregistrement.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.dateEditEnregistrement.setFocus(Qt.Qt.OtherFocusReason)
            return False

        if self.ui.lineEditNomOfficierPublic.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditNomOfficierPublic.setFocus(Qt.Qt.OtherFocusReason)
            return False

        if self.ui.lineEditValeurTransanction.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditValeurTransanction.setFocus(Qt.Qt.OtherFocusReason)
            return False

        return True

    def save(self):

        import time
        import datetime
        sql = "INSERT INTO actepublic" \
              "(numeroactepublic, dateenregistrement,nomofficierpublic,valeurtransaction,nombreoperation,idprojet) " \
             "values" \
              "(%s, %s, %s, %s, %s, %s)"

        numActe = str(self.ui.lineEditNumActe.text()).strip()
        dateEnreg = self.ui.dateEditEnregistrement.text()
        print dateEnreg
        dateEnregistrement = dateEnreg.split('/')
        print dateEnregistrement
        dateEnreg = datetime.date(int(dateEnregistrement[2]), int(dateEnregistrement[1]), int(dateEnregistrement[0]))
        nomOfficier = str(self.ui.lineEditNomOfficierPublic.text())
        valeur = int(self.ui.lineEditValeurTransanction.text())
        print "valeur in"
        print valeur
        print " valeur out"
        nombreOperation = int(self.ui.spinBoxNombreOperations.text())
        idprojet = int(self.id_projet)

        #params = (numActe, dateEnreg,nomOfficier,valeur,nombreOperation,idprojet)
        params = (numActe, dateEnreg,nomOfficier,valeur,nombreOperation,idprojet)
        #if self.id:
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

