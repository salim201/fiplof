from PyQt4 import Qt, QtGui
from .EditHameau import Ui_Dialog
import psycopg2.extras
from Utils import Utils

class EditHameauRun(Qt.QDialog):
    def __init__(self, connection, idrow=0):
        Qt.QDialog.__init__(self)
        self.connection, self.idrow = connection, idrow
        self.setWindowFlags(Qt.Qt.Tool)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.utils = Utils(self.connection)
        self.initFkt()
        self.initActions()

    def exec_(self):
        if not self.prefill():
            return
        return super(EditHameauRun, self).exec_()

    def initFkt(self):
        sql = "SELECT idfokontany,nomfokontany FROM fokontany"
        self.utils.fillComboWithSql(self.ui.comboBoxFokontany, sql, "nomfokontany", "idfokontany")

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonOK.clicked.connect(self.enregistrer)

    def enregistrer(self):
        if not self.check():
            return
        self.save()
        self.accept()

    def check(self):
        if self.ui.lineEditCode.text() == "":
            self.utils.alert("Veuillez remplir le code")
            self.ui.lineEditCode.setFocus(Qt.Qt.OtherFocusReason)
            return False
        if self.ui.lineEditNom.text() == "":
            self.utils.alert("Veuillez remplir le nom")
            self.ui.lineEditNom.setFocus(Qt.Qt.OtherFocusReason)
            return False
        return True

    def save(self):
        idfkt = self.utils.getComboValue(self.ui.comboBoxFokontany)
        if not idfkt: return
        if self.checkHameauByName(str(self.ui.lineEditNom.text()), idfkt):
            return
        sql = "INSERT INTO hameau" \
              "(idfokontany, codehameau, nomhameau) " \
              "values" \
              "(%s, %s, %s)"
        params = (idfkt,
            str(self.ui.lineEditCode.text()),
            str(self.ui.lineEditNom.text()))
        if self.idrow:
            sql = "UPDATE hameau SET idfokontany=%s, codehameau=%s, nomhameau=%s" \
                  " WHERE idhameau=%s"
            params = params + (self.idrow,)
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            print(ex)
        cursor.close()

    def prefill(self):
        if self.idrow == 0:
            return True
        sql = "SELECT * FROM hameau WHERE idhameau = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (self.idrow,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return False
        self.utils.setComboValue(self.ui.comboBoxFokontany, row["idfokontany"])
        self.ui.lineEditCode.setText(row['codehameau'])
        self.ui.lineEditNom.setText(row['nomhameau'])
        return True

