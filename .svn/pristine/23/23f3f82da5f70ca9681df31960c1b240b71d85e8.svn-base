from PyQt4 import Qt, QtGui
from .EditRegion import Ui_Dialog
import psycopg2.extras


class EditRegionRun(Qt.QDialog):
    def __init__(self, connection, id=0):

        Qt.QDialog.__init__(self)
        self.connection, self.id = connection, id
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initActions()
        self.ui.codeRegion.setFocus(Qt.Qt.OtherFocusReason)

    def exec_(self):
        if not self.prefill():
            return
        return super(EditRegionRun, self).exec_()

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonEnregistrer.clicked.connect(self.enregistrer)

    def enregistrer(self):
        if not self.check():
            return
        if not self.verifyCode():
            return
        self.save()
        self.accept()

    def verifyCode(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM region WHERE coderegion=%s AND idregion != %s", (str(self.ui.codeRegion.text()), self.id))
            rows = cursor.fetchall()
            if len(rows) >= 1:
                QtGui.QMessageBox.information(self, "Doublon du code region",
                                              "Ce code ou region existe deja")
                self.ui.codeRegion.setText("")
                self.ui.codeRegion.setFocus(Qt.Qt.OtherFocusReason)
                cursor.close()
                return False
            cursor.execute("SELECT * FROM region WHERE nomregion=%s AND idregion != %s", (str(self.ui.NomRegion.text()), self.id))
            rows = cursor.fetchall()
            if len(rows) >= 1:
                QtGui.QMessageBox.information(self, "Doublon du Nom Region",
                                              "Ce region existe deja")
                self.ui.NomRegion.setText("")
                self.ui.NomRegion.setFocus(Qt.Qt.OtherFocusReason)
                cursor.close()
                return False
        except Exception as ex:
            self.connection.rollback()
            print(ex)
        cursor.close()
        return True

    def check(self):
        if self.ui.codeRegion.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir le libelle")
            self.ui.codeRegion.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.NomRegion.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.NomRegion.setFocus(Qt.Qt.OtherFocusReason)
            return False
        return True

    def save(self):
        sql = "INSERT INTO region" \
              "(coderegion, nomregion) " \
              "values" \
              "(%s, %s)"
        params = (str(self.ui.codeRegion.text()),
                  str(self.ui.NomRegion.text()))
        if self.id:
            sql = "UPDATE region SET coderegion=%s, nomregion=%s" \
                  " WHERE idregion=%s"
            params = params + (self.id, )
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()

    def prefill(self):
        if self.id == 0:
            return True
        sql = "SELECT * FROM region WHERE idregion = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return False
        self.ui.codeRegion.setText(row['coderegion'])
        self.ui.NomRegion.setText(row['nomregion'])
        return True
