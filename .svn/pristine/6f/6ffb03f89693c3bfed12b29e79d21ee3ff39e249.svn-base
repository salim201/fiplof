from PyQt4 import Qt, QtGui
from .EditDistrict import Ui_Dialog
import psycopg2.extras
from Utils import Utils


class EditDistrictRun(Qt.QDialog):
    def __init__(self, connection, idrow=0):
        Qt.QDialog.__init__(self)
        self.connection, self.idrow = connection, idrow
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.utils = Utils(self.connection)
        self.ui.lineEditCode.setFocus(True)
        self.initRegions()
        self.initActions()

    def exec_(self):
        if not self.prefill():
            return
        return super(EditDistrictRun, self).exec_()

    def initRegions(self):
        sql = "SELECT idregion,nomregion FROM region"
        self.utils.fillComboWithSql(self.ui.comboBoxRegion, sql, "nomregion", "idregion")

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
        idc = self.utils.getComboValue(self.ui.comboBoxRegion)
        if not idc: return
        sql = "INSERT INTO district" \
              "(idregion, codedistrict, nomdistrict) " \
              "values" \
              "(%s, %s, %s)"
        params = (idc,
            str(self.ui.lineEditCode.text()),
            str(self.ui.lineEditNom.text()))
        if self.idrow:
            sql = "UPDATE district SET idregion=%s, codedistrict=%s, nomdistrict=%s" \
                  " WHERE iddistrict=%s"
            params = params + (self.idrow,)
            #sql1 = "UPDATE parcelle_d SET numdemande = REPLACE(numdemande, '519', '531')"

        cursor = self.connection.cursor()

        try:

            #cursor.execute("UPDATE parcelle_d SET numdemande = REPLACE(numdemande, '519', '531')")
            #ancien code
            cursor.execute("select codedistrict from district")
            cd = cursor.fetchone()
            print("ancien code District ")
            if(cd is not None):
                ancienCode = cd[0].strip()
                print(ancienCode)
                #cursor.execute("UPDATE parcelle_d SET numdemande = REPLACE(numdemande, '800', '" + str(self.ui.lineEditCode.text()) + "')")
                cursor.execute("UPDATE parcelle_d SET numdemande = REPLACE(numdemande,'"+ancienCode+"-', '"+str(self.ui.lineEditCode.text())+"-')")
                cursor.execute("UPDATE demande SET numdemande = REPLACE(numdemande, '"+ancienCode+"-', '" + str(self.ui.lineEditCode.text()) + "-')")
                cursor.execute("UPDATE certificat SET numerodemande = REPLACE(numerodemande,'"+ancienCode+"-', '" + str(self.ui.lineEditCode.text()) + "-')")
                cursor.execute("UPDATE certificat SET numerocertificat = REPLACE(numerocertificat, '"+ancienCode+"-', '" + str(self.ui.lineEditCode.text()) + "-')")
            cursor.execute(sql, params)
            self.connection.commit()
        except Exception as ex:
            self.connection.rollback()
            print(ex)
        cursor.close()

    def prefill(self):
        if self.idrow == 0:
            return True
        sql = "SELECT * FROM district WHERE iddistrict = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (self.idrow,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return False
        self.utils.setComboValue(self.ui.comboBoxRegion, row["idregion"])
        self.ui.lineEditCode.setText(row['codedistrict'])
        self.ui.lineEditNom.setText(row['nomdistrict'])
        return True
