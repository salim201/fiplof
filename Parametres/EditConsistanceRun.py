from PyQt4 import Qt, QtGui
from .EditConsistance import Ui_Dialog
import psycopg2.extras


class EditConsistanceRun(Qt.QDialog):
    def __init__(self, connection, id=0, isBat = False):
        Qt.QDialog.__init__(self)
        self.connection, self.id,  self.isBat = connection, id, isBat
        self.setWindowFlags(Qt.Qt.Tool)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        if isBat:
            self.ui.label_2.setText("Mombamomban'ny trano")
        self.initActions()
        self.ui.lineEditLibelle.setFocus(Qt.Qt.OtherFocusReason)

    def exec_(self):
        if not self.prefill():
            return
        return super(EditConsistanceRun, self).exec_()

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonEnregistrer.clicked.connect(self.enregistrer)

    def enregistrer(self):
        if not self.check():
            return
        self.save()
        self.accept()

    def check(self):
        if self.ui.lineEditLibelle.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir le libelle")
            self.ui.lineEditLibelle.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.lineEditParcelleOuBatiment.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.lineEditParcelleOuBatiment.setFocus(Qt.Qt.OtherFocusReason)
            return False
        return True

    def save(self):
        sql = ""
        if not self.isBat:
            sql = "INSERT INTO consistance" \
              "(libelleconsistance, parcelleoubatiment) " \
              "values" \
              "(%s, %s)"
        else:
            #print "est batiment"
            sql = "INSERT INTO consistance_batiment" \
                  "(consistance, mombamombanytany) " \
                  "values" \
                  "(%s, %s)"
        params = (str(self.ui.lineEditLibelle.text()),
                  str(self.ui.lineEditParcelleOuBatiment.text()))
        if self.id:
            sql = ""
            if not self.isBat:
                sql = "UPDATE consistance SET libelleconsistance=%s, parcelleoubatiment=%s" \
                  " WHERE idconsistance=%s"
            else:
                #print "Mandalo Id"
                sql = "UPDATE consistance_batiment SET consistance=%s, mombamombanytany=%s" \
                      " WHERE id=%s"
            params = params + (self.id,)
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
        except StandardError as e:
            #print(e)
            self.connection.rollback()
        cursor.close()

    def prefill(self):
        if self.id == 0:
            return True
        sql = ""
        if not self.isBat:
            sql = "SELECT * FROM consistance WHERE idconsistance = %s"
        else:
            sql = "SELECT * FROM consistance_batiment WHERE id = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return False
        if not self.isBat:
            self.ui.lineEditLibelle.setText(row['libelleconsistance'])
            self.ui.lineEditParcelleOuBatiment.setText(row['parcelleoubatiment'])
        else:
            self.ui.lineEditLibelle.setText(row['consistance'])
            self.ui.lineEditParcelleOuBatiment.setText(row['mombamombanytany'])
        return True
