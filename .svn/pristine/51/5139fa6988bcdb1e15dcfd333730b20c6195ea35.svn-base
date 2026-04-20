from PyQt4 import Qt, QtGui
from .EditCommune import Ui_Dialog
import psycopg2.extras
from Utils import Utils

class EditCommuneRun(Qt.QDialog):
    def __init__(self, connection, idrow=0):
        Qt.QDialog.__init__(self)
        self.connection, self.idrow = connection, idrow
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.utils = Utils(self.connection)
        self.ui.lineEditCode.setFocus(True)
        self.initDistrict()
        self.initActions()

    def exec_(self):
        if not self.prefill():
            return
        return super(EditCommuneRun, self).exec_()

    def initDistrict(self):
        sql = "SELECT iddistrict,nomdistrict FROM district"
        self.utils.fillComboWithSql(self.ui.comboBoxDistrict, sql, "nomdistrict", "iddistrict")

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
        if self.ui.spinBoxCodeGuichet.value() == 0:
            self.utils.alert("Veuillez remplir le code guichet")
            self.ui.spinBoxCodeGuichet.setFocus(Qt.Qt.OtherFocusReason)
            return False
        return True


    def verifyCode(self):
        idc = self.utils.getComboValue(self.ui.comboBoxDistrict)
        if not idc:
            return
        cursor = self.connection.cursor()
        try:
            #cursor.execute("select * from fokontany where idcommune=% AND codefokontany=%",(idc, str(self.ui.lineEditCode.text())))
            cursor.execute("SELECT * FROM commune WHERE iddistrict=%s AND codecommune=%s",(idc, str(self.ui.lineEditCode.text())))
            rows = cursor.fetchall()
            print "at try"
            if len(rows) >= 1:
                QtGui.QMessageBox.information(self, "Doublon au du code commune",
                                              "Ce code existe deja")
                self.ui.lineEditCode.setText("")
                self.ui.lineEditCode.setFocus(Qt.Qt.OtherFocusReason)
                cursor.close()
                return False
        except Exception as ex:
            self.connection.rollback()
            print(ex)
        return True

    def save(self):
        idc = self.utils.getComboValue(self.ui.comboBoxDistrict)

        if not idc: return
        params = (idc,
                  str(self.ui.lineEditCode.text()),
                  str(self.ui.lineEditNom.text()),
                  str(self.ui.spinBoxCodeGuichet.value()),
                  str(self.ui.lineEditNomMaire.text()))

        if self.idrow:
            sql = "UPDATE commune SET iddistrict=%s, codecommune=%s, nomcommune=%s , codeg=%s , maire=%s" \
                  " WHERE idcommune=%s"
            params = params + (self.idrow,)
        else:
            if not self.verifyCode():
                return
            sql = "INSERT INTO commune" \
                  "(iddistrict, codecommune, nomcommune,codeg,maire) " \
                  "values" \
                  "(%s, %s, %s, %s,%s)"

        cursor = self.connection.cursor()
        try:

            # cursor.execute("UPDATE parcelle_d SET numdemande = REPLACE(numdemande, '519', '531')")
            # ancien code
            cursor.execute("select codecommune from commune")
            cm = cursor.fetchone()
            print("ancien code commune ")
            if(cm is not None):
                ancienCode = cm[0].strip()
                print(ancienCode)
                # cursor.execute("UPDATE parcelle_d SET numdemande = REPLACE(numdemande, '800', '" + str(self.ui.lineEditCode.text()) + "')")
                cursor.execute("UPDATE parcelle_d SET numdemande = REPLACE(numdemande,'-" + ancienCode + "', '-" + str(self.ui.lineEditCode.text()) + "')")
                cursor.execute("UPDATE demande SET numdemande = REPLACE(numdemande, '-" + ancienCode + "', '-" + str(self.ui.lineEditCode.text()) + "')")
                cursor.execute("UPDATE certificat SET numerodemande = REPLACE(numerodemande,'-" + ancienCode + "', '-" + str(self.ui.lineEditCode.text()) + "')")
                cursor.execute("UPDATE certificat SET numerocertificat = REPLACE(numerocertificat, '-" + ancienCode + "', '-" + str(self.ui.lineEditCode.text()) + "')")

            cursor.execute(sql, params)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            print(ex)
        cursor.close()

    def prefill(self):
        if self.idrow == 0:
            return True
        sql = "SELECT * FROM commune WHERE idcommune = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (self.idrow,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return False
        self.utils.setComboValue(self.ui.comboBoxDistrict, row["iddistrict"])
        self.ui.lineEditCode.setText(row['codecommune'])
        self.ui.lineEditNom.setText(row['nomcommune'])
        if row['codeg'] is not None:
            self.ui.spinBoxCodeGuichet.setValue(row['codeg'])
        if row['maire'] is not None:
            self.ui.lineEditNomMaire.setText(row['maire'])
        return True
