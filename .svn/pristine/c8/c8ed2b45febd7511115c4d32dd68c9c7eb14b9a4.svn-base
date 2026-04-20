from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
import time
import datetime, globalvars
import datetime
from datetime import date
from .ActeDeces import Ui_Dialog

class ActeDeces(QtGui.QDialog):
    def __init__(self,parent):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.parent = parent
        self.details = self.parent.details
        self.id_projet = self.parent.id_projet
        self.connection = self.parent.connection
#       print self.parent.txt
        self.ui.setupUi(self)
        self.initActions()

    def detailsActes(self):
        if len(self.details) == 0 :
            print "do not nothing"
        else :
            print " SELF.DETAILS "
            print self.details
            details = self.details

            self.ui.lineEditNumActe.setText(details[1])
            dateActe = details[2].isoformat()
            year, month, day = details[2].isoformat().split("-")
            dateActe = date(int(year), int(month), int(day))
            self.ui.dateEditActe.setDate(dateActe)
            self.ui.lineEditNumActeNotoriete.setText(details[3])

            dateActeNotoriere = details[4].isoformat()
            year, month, day = details[4].isoformat().split("-")
            dateActeNotoriere = date(int(year), int(month), int(day))
            self.ui.dateEditActeNotoriete.setDate(dateActeNotoriere)

            self.ui.btnOk.setVisible(False)
            self.ui.btnAnnuler.setVisible(False)


    def initActions(self):
        self.detailsActes()
        validator = QtGui.QDoubleValidator()
        #self.ui.lineEditNumActe.setValidator(validator)
        #self.ui.lineEditNumActeNotoriete.setValidator(validator)
        self.ui.btnAide.setVisible(False)

        self.ui.dateEditActe.setDisplayFormat("dd/MM/yyyy")
        if len(self.details) == 0:
            self.ui.dateEditActe.setDate(QDate.currentDate())
            print "do not nothing"
        else:
            print "do not nothing"
            #self.ui.dateEditActe.setDate(QDate.currentDate())

        self.ui.dateEditActeNotoriete.setDisplayFormat("dd/MM/yyyy")
        if len(self.details) == 0:
            self.ui.dateEditActeNotoriete.setDate(QDate.currentDate())
            print "do not nothing"
        else:
            print "do not nothing"
        #self.ui.dateEditActeNotoriete.setDate(QDate.currentDate())

        self.ui.btnAnnuler.clicked.connect(self.reject)
        self.ui.btnOk.clicked.connect(self.enregistrer)

    def enregistrer(self):
        print "enregistrer"
        if not self.check():
            return

        self.save()
        self.accept()

    def check(self):
        if self.ui.lineEditNumActe.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditNumActe.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.dateEditActe.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.dateEditActe.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.lineEditNumActeNotoriete.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditNumActeNotoriete.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.dateEditActeNotoriete.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.dateEditActeNotoriete.setFocus(Qt.Qt.OtherFocusReason)
            return False

        return True

    def save(self):

        import time
        import datetime
        sql = "INSERT INTO actedeces" \
              "(numeroactedeces, dateactedeces,numeroactenotoriete,dateactenotoriete,idprojet) " \
              "values" \
              "(%s, %s, %s, %s, %s)"

        numActe = str(self.ui.lineEditNumActe.text()).strip()
        dateActe = self.ui.dateEditActe.text()
        dateActes = dateActe.split('/')
        dateActess = datetime.date(int(dateActes[2]), int(dateActes[1]), int(dateActes[0]))
        numActeNotoriete = str(self.ui.lineEditNumActeNotoriete.text()).strip()

        dateActeNote = self.ui.dateEditActeNotoriete.text()
        dateActeNotes = dateActeNote.split('/')
        dateActeNotess = datetime.date(int(dateActeNotes[2]), int(dateActeNotes[1]), int(dateActeNotes[0]))

        idprojet = int(self.id_projet)

        # params = (numActe, dateEnreg,nomOfficier,valeur,nombreOperation,idprojet)
        params = (numActe, dateActess, numActeNotoriete, dateActeNotess, idprojet)
        # if self.id:
        #    sql = "UPDATE hameau SET nomhameau=%s, codehameau=%s ,idfokontany=%s " \
        #          " WHERE idhameau=%s"
        #    params = params + (self.id,)
        cursor = self.connection.cursor()
        try:
            print
            "try in"
            cursor.execute(sql, params)
            print
            "try out"
            self.connection.commit()
            self.parent.showAll()
        except Exception as e:
            print e
            self.connection.rollback()
        cursor.close()

