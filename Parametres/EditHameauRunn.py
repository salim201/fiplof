# -*- coding: utf-8 -*-
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from PyQt4 import QtGui, Qt
from PgCrud import PgSql, PgColumn
from PyQt4 import QtCore, QtGui
from EditHameau import Ui_Dialog

from PyQt4 import QtGui, Qt
import psycopg2
from psycopg2 import extras
from Utils import Utils


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s



class EditHameauRunn(QDialog):

    def __init__(self, connection, id=0,idprojet=0,FenHameauFrom = None):
        Qt.QDialog.__init__(self)
        self.communes = ""
        self.fkt = ""
        self.HmCF = 0
        self.FenHameauFrom = FenHameauFrom
        self.project_id = idprojet
        self.connection, self.id = connection, id
        self.setWindowFlags(Qt.Qt.Tool)
        self.connection = connection
        self.ui = Ui_Dialog()
        self.utils = Utils(self.connection)
        self.ui.setupUi(self)
        #self.prefill()
        self.initActions()
        self.loadCommuneByProject()
        self.populateCommune()


    def populateCommune(self):
        #self.ui.communeComboBox.clear()
        commune = []
        print " POPULATE COMMUNE"
        cursor = self.connection.cursor()
        for item in self.communes :
            idcommune = int(item[1])
            cursor.execute("SELECT *   FROM commune  WHERE idcommune=%s", [idcommune])
            res = cursor.fetchone()
            self.ui.communeComboBox.addItem(_fromUtf8(res[3]), res[0])



        self.fillCommunes()

    def loadCommuneByProject(self):

        cursor = self.connection.cursor()
        cursor.execute("SELECT *   FROM projet_commune  WHERE idprojet=%s", [int(self.project_id)])
        dm = cursor.fetchall()
        if (len(dm) >= 1):
            self.communes = dm
            return dm


    def initComboCommune(self):
        sql = "SELECT idcommune,nomcommune FROM commune"
        self.utils.fillComboWithSql(self.ui.communeComboBox, sql, "nomcommune", "idcommune")
        self.fillFokontany()

    def fillCommune(self):
        idparent = self.utils.getComboValue(self.ui.comboBoxRegion)
        sql = "SELECT * FROM district where idregion=" + str(idparent)
        self.utils.fillComboWithSql(self.ui.comboBoxDistrict, sql, "nomdistrict", "iddistrict")
        self.fillCommunes()

    def fillCommunes(self):
        print "sddsrsrzrsdrsdr "
        idparent = self.utils.getComboValue(self.ui.communeComboBox)
        print "parent in"
        print idparent
        sql = "SELECT * FROM fokontany where idcommune=" + str(idparent)
        self.utils.fillComboWithSql(self.ui.fokontanyComboBox, sql, "nomfokontany", "idfokontany")
        #self.updateButtonsStatus()
    def fillFokontany(self):
        idparent = self.utils.getComboValue(self.ui.communeComboBox)
        sql = "SELECT * FROM fokontany where idcommune=" + str(idparent)
        print idparent
        #self.utils.fillComboWithSql(self.ui.fokontanyComboBox, sql, "nomfokontany","idfokontany")

        #self.fillCommunes()

    def prefill(self):
        if self.project_id == 0 : return
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cursor.execute("SELECT commune.idcommune, commune.nomcommune FROM projet_commune JOIN commune on commune.idcommune=projet_commune.idcommune"
                           " WHERE projet_commune.idprojet=%s", (self.project_id,))
            rows = cursor.fetchall()
            for r in rows:
                self.ui.communeComboBox.addItem(_fromUtf8(r["nomcommune"], r["idcommune"]))
        except Exception as e:
            print(e)
            cursor.close()
        cursor.close()


    def loadAndPopulateFokontany(self,text):
        index = self.ui.communeComboBox.currentIndex()
        idcommune = self.ui.communeComboBox.itemData(index)
        nomcommune = self.ui.communeComboBox.itemText(index)
        cursor = self.connection.cursor()
        cursor.execute("SELECT *   FROM fokontany  WHERE idcommune=%s", [int(self.ui.communeComboBox.itemData(index).toPyObject())])
        res = cursor.fetchall()
        i = 0
        for item in res :
            self.ui.fokontanyComboBox.addItem(_fromUtf8(res[i][3]), res[i][0])
            i = i + 1

        self.getFokontany()

    def getFokontany(self):

        index = self.ui.fokontanyComboBox.currentIndex()
        idfkt = self.ui.fokontanyComboBox.itemData(index)
        self.fkt = self.ui.fokontanyComboBox.itemData(index).toPyObject()
        print " id fokontany in"
        print  self.fkt
        print " id fokontany out "

    def exec_(self):
        if not self.prefill():
            return
        return super(EditHameauRunn, self).exec_()

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonEnregistrer.clicked.connect(self.enregistrer)
        #self.ui.communeComboBox.activated.connect(self.loadAndPopulateFokontany)
        #self.ui.fokontanyComboBox.activated.connect(self.getFokontany)

        self.ui.communeComboBox.currentIndexChanged.connect(self.fillCommunes)
        #self.ui.comboBoxDistrict.currentIndexChanged.connect(self.fillCommunes)

    def enregistrer(self):
        if not self.check():
            return

        if not self.verifyCode():
            return
        self.save()
        if self.FenHameauFrom is not None:
            self.FenHameauFrom.fillHameau()
        self.accept()


    def check(self):
        if self.ui.nomLineEdit.text() == "":
            QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
            self.ui.nomLineEdit.setFocus(Qt.Qt.OtherFocusReason)
            return False
     #   if self.ui.codeLineEdit.text() == "":
     #       QtGui.QMessageBox.warning(self, "FIPLOF", "Veuillez remplir ce champ")
     #       self.ui.codeLineEdit.setFocus(Qt.Qt.OtherFocusReason)
     #       return False
        return True

    def verifyCode(self):


        idcommune = self.utils.getComboValue(self.ui.communeComboBox)
        idfkt = str(self.utils.getComboValue(self.ui.fokontanyComboBox))
        code = str(self.ui.codeLineEdit.text())
        nom = str(self.ui.nomLineEdit.text())


        if not idcommune: return
        if not idfkt: return

        cursor = self.connection.cursor()
        try:
            # cursor.execute("select * from fokontany where idcommune=% AND codefokontany=%",(idc, str(self.ui.lineEditCode.text())))
            if (self.ui.codeLineEdit.text() != ""):

                cursor.execute("SELECT * FROM hameau WHERE idfokontany=%s AND codehameau=%s AND idhameau != %s",(idfkt,code,self.id))
                rows = cursor.fetchall()

                if (len(rows) >= 1):
                    QtGui.QMessageBox.information(self, "Doublon au du code hameau",
                                                  "Ce code existe deja")
                    self.ui.codeLineEdit.setText("")
                    self.ui.codeLineEdit.setFocus(Qt.Qt.OtherFocusReason)
                    cursor.close()
                    return False
            else:
                print("Code HAMEAU NULL")
        except Exception as ex:
            self.connection.rollback()
            print(ex)
        return True
        cursor.close()
    def save(self):
        sql = "INSERT INTO hameau" \
              "(nomhameau, codehameau,idfokontany) " \
              "values" \
              "(%s, %s, %s)"

        idcommune = self.utils.getComboValue(self.ui.communeComboBox)
        idfkt = self.utils.getComboValue(self.ui.fokontanyComboBox)
        code = str(self.ui.codeLineEdit.text())
        nom = str(self.ui.nomLineEdit.text())

        params = (nom,code,int(idfkt))
        if self.id:
            sql = "UPDATE hameau SET nomhameau=%s, codehameau=%s ,idfokontany=%s " \
                  " WHERE idhameau=%s"
            params = params + (self.id,)
        else:
            if self.checkHameauByName(nom, idfkt):
                return
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
        except:
            self.connection.rollback()
        cursor.close()

    def prefill(self):

        print "self.id"
        print self.id
        if self.id == 0:
            return True
        sql = "SELECT * FROM hameau WHERE idhameau = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (self.id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return False
        self.ui.codeLineEdit.setText(row['codehameau'])
        self.ui.nomLineEdit.setText(row['nomhameau'])
        self.ui.fokontanyComboBox.setCurrentIndex(self.ui.fokontanyComboBox.findData(row['idfokontany']))

        #reglage commune via idfokontany
        sql = "select * from fokontany WHERE idfokontany = %s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (row['idfokontany'],))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return False
        self.ui.communeComboBox.setCurrentIndex(self.ui.communeComboBox.findData(row['idcommune']))
        #set selected commune
        #set selected fokontany
        return True

    def checkHameauByName(self, nomHameau, idfkt):
        cur = self.connection.cursor()
        print "check hameau"
        try:
            cur.execute("SELECT idhameau, nomfokontany FROM hameau INNER JOIN fokontany ON hameau.idfokontany = fokontany.idfokontany WHERE UPPER(TRIM(nomhameau)) = %s AND hameau.idfokontany = %s", (nomHameau.upper(), idfkt))
            res = cur.fetchall()
            print res
            if res is not None:
                text = "Le Hameau " + nomHameau.upper() + u" existe déjà dans le fokontany " + str(res[0][1])
                print text
                QtGui.QMessageBox.critical(None, "Erreur", text)
                return True
            else:
                return False
        except Exception as err:
            print err
            self.connection.rollback()
            return False