# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from .CodeParcelle import Ui_Dialog
from PgCrud import PgSql
import psycopg2, globalvars
import psycopg2.extras

class CodeParcelleRun(QDialog):
    def __init__(self, connection, geom):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection, self.geom = connection, geom
        self.fillFokontany()
        self.fillHameau()
        self.preCode = ""
        self.ui.lineEditCode.setReadOnly(True)
        self.initDB()
        self.ui.pushButtonAnnuler.clicked.connect(self.annuler)
        self.ui.pushButtonOK.clicked.connect(self.ok)
        self.initActions()
        self.getCodeHameau()


    def initActions(self):
        self.ui.comboBoxHameau.currentIndexChanged.connect(self.getCodeHameau)
        self.ui.lineEditNumero.textEdited.connect(self.generateCodeParcelle)

    def getComboValue(self, combo):
        index = combo.currentIndex()
        data = combo.itemData(index)
        if "toInt" in dir(data):
            return data.toInt()[0]
        if data is None:
            return 0
        return data

    def fillFokontany(self):
        pgsql = PgSql.Table(self.connection, "fokontany")
        pgsql.fillComboWithSql(self.ui.comboBoxFokontany, "SELECT idfokontany, nomfokontany from fokontany", "nomfokontany", "idfokontany")
        self.ui.comboBoxFokontany.currentIndexChanged.connect(self.fillHameau)

    def fillHameau(self):
        self.ui.comboBoxHameau.clear()
        rowid = self.getComboValue(self.ui.comboBoxFokontany)
        print(rowid)
        pgsql = PgSql.Table(self.connection, "hameau")
        pgsql.fillComboWithSql(self.ui.comboBoxHameau, "SELECT idhameau, nomhameau from hameau WHERE idfokontany=" + str(rowid), "nomhameau", "idhameau")

    def annuler(self):
        self.reject()

    def ok(self):
        idhameau = self.getComboValue(self.ui.comboBoxHameau)
        if idhameau == 0:
            QMessageBox.critical(self, "Erreur",u"Veuillez séléctionner un Hameau s'il vous plait")
            return
        code = self.ui.lineEditCode.text()
        if code == "":
            return
        numero = self.ui.lineEditNumero.text()
        if self.uniciteCodeParcelle(str(numero).strip(), idhameau) is False:
            QMessageBox.critical(self, "Erreur", u"Ce code hameau existe déjà")
            return
        if numero == "":
            QMessageBox.critical(self, "Erreur", u"Veuillez saisir le numero de la parcelle")
            return
        #wkt = "POLYGON((" + self.geom + "))"

        sql = "INSERT INTO parcelle_d(numero, geom, has_data, estfiscalite,codeparcelle, idhameau) VALUES (%s, ST_GeomFromText(%s, "+str(globalvars.EPSG_SCR)+"), false, 1,%s, %s) returning gid"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (str(numero), str(self.geom.exportToWkt()),str(code), idhameau))
            dm = cursor.fetchone()
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()
        self.accept()

    def initDB(self):
        self.cur = self.connection.cursor()

    def getCodeHameau(self):
        idhameau = self.getComboValue(self.ui.comboBoxHameau)
        try:
            self.cur.execute("SELECT codehameau, codefokontany FROM hameau h, fokontany f WHERE h.idfokontany = f.idfokontany AND h.idhameau = %s", (idhameau,))
            codes = self.cur.fetchone()
            if codes is not None:
                self.preCode = str(codes[1]).strip() + str(codes[0]).strip() + "-"
                self.generateCodeParcelle()
        except StandardError as e:
            print(e)
            self.connection.rollback()

    def generateCodeParcelle(self):
        text = self.preCode + str(self.ui.lineEditNumero.text())
        self.ui.lineEditCode.setText(text)

    def uniciteCodeParcelle(self, numero, idhameau):
        try:
            self.cur.execute("SELECT gid FROM parcelle_d WHERE numero = %s AND idhameau = %s",(numero, idhameau))
            data = self.cur.fetchone()
            if data is not None:
                return False
            else:
                return True
        except StandardError as e:
            print (e)
            self.connection.rollback()