from PyQt4 import Qt, QtGui
from .EditFokontany import Ui_Dialog
import psycopg2.extras
from Utils import Utils


class EditFokontanyRun(Qt.QDialog):
    def __init__(self, connection, idrow=0,FenFromFktCF = None):
        Qt.QDialog.__init__(self)
        self.connection, self.idrow = connection, idrow
        self.ui = Ui_Dialog()

        self.FenFromFktCF = FenFromFktCF
        self.ui.setupUi(self)
        self.utils = Utils(self.connection)
        self.ui.lineEditCode.setFocus(True)
        self.initCommunes()
        self.initActions()

    def exec_(self):
        if not self.prefill():
            return
        return super(EditFokontanyRun, self).exec_()

    def initCommunes(self):
        sql = "SELECT idcommune,nomcommune FROM commune"
        self.utils.fillComboWithSql(self.ui.comboBoxCommune, sql, "nomcommune", "idcommune")

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonOK.clicked.connect(self.enregistrer)

    def enregistrer(self):
        if not self.check():
            return

        if not self.verifyCode():
            return
        self.save()
        if self.FenFromFktCF is not None :
            self.FenFromFktCF.fillFkt()
        self.accept()


    def verifyCode(self):
        idc = self.utils.getComboValue(self.ui.comboBoxCommune)
        print str(self.ui.lineEditCode.text())
        if not idc: return
        cursor = self.connection.cursor()
        try:
            if (self.ui.lineEditCode.text() != ""):
                cursor.execute("SELECT * FROM fokontany WHERE idcommune=%s AND codefokontany=%s AND idfokontany != %s",(idc, str(self.ui.lineEditCode.text()), self.idrow))
                rows = cursor.fetchall()
                print "at try"
                if len(rows) >= 1:
                    QtGui.QMessageBox.information(self, "Doublon au du code fokontany",
                                                  "Ce code existe deja")
                    self.ui.lineEditCode.setText("")
                    self.ui.lineEditCode.setFocus(Qt.Qt.OtherFocusReason)
                    cursor.close()
                    return False
            else :
                print("code NULL")
        except Exception as ex:
            self.connection.rollback()
            print(ex)
        return True
        cursor.close()

    def check(self):
        print("CHECK FOKONTANY RUN")

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
        idc = self.utils.getComboValue(self.ui.comboBoxCommune)
        if not idc: return
        sql = "INSERT INTO fokontany" \
              "(idcommune, codefokontany, nomfokontany) " \
              "values" \
              "(%s, %s, %s)"
        params = (idc,
            str(self.ui.lineEditCode.text()),
            str(self.ui.lineEditNom.text()))
        if self.idrow:
            sql = "UPDATE fokontany SET idcommune=%s, codefokontany=%s, nomfokontany=%s" \
                  " WHERE idfokontany=%s"
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

        sql = "SELECT * FROM fokontany WHERE idfokontany = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute(sql, (self.idrow,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return False
        #try:
            #self.utils.alert(str(row["idcommune"]))
        #except Exception as err:
            #print (err)
        print ('prefill')
        self.utils.setComboValue(self.ui.comboBoxCommune, row["idcommune"])
        self.ui.lineEditCode.setText(row['codefokontany'])
        self.ui.lineEditNom.setText(row['nomfokontany'])

        return True
