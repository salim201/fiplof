from PyQt4 import QtGui, Qt
from PyQt4.QtCore import QDate
import psycopg2
from psycopg2 import extras
from .EditProjet import Ui_Dialog
from Utils import Utils
import sip


class EditProjetRun(QtGui.QDialog):
    def __init__(self, connection, idprojet=0):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.setWindowFlags(Qt.Qt.Tool)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.project_id = idprojet
        self.utils = Utils(self.connection)
        self.initComboRegion()
        self.prefill()
        self.initActions()

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.comboBoxRegion.currentIndexChanged.connect(self.fillDistricts)
        self.ui.comboBoxDistrict.currentIndexChanged.connect(self.fillCommunes)
        self.ui.pushButtonAjouter.clicked.connect(self.addCommune)
        self.ui.pushButtonSupprimer.clicked.connect(self.removeCommune)
        self.ui.pushButtonEnregistrer.clicked.connect(self.save)
        self.ui.listWidgetCommunes.itemClicked.connect(self.updateButtonsStatus)

        self.ui.dateEditDateLancement.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditDateLancement.setDate(QDate.currentDate())

        self.ui.dateEditDatePremierImport.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditDatePremierImport.setDate(QDate.currentDate())

        self.ui.dateEditDateDernierImport.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEditDateDernierImport.setDate(QDate.currentDate())

    def initComboRegion(self):
        sql = "SELECT idregion,nomregion FROM region"
        self.utils.fillComboWithSql(self.ui.comboBoxRegion, sql, "nomregion", "idregion")
        self.fillDistricts()

    def fillDistricts(self):
        idparent = self.utils.getComboValue(self.ui.comboBoxRegion)
        sql = "SELECT * FROM district where idregion=" + str(idparent)
        self.utils.fillComboWithSql(self.ui.comboBoxDistrict, sql, "nomdistrict", "iddistrict")
        self.fillCommunes()

    def fillCommunes(self):
        idparent = self.utils.getComboValue(self.ui.comboBoxDistrict)
        sql = "SELECT * FROM commune where iddistrict=" + str(idparent)
        self.utils.fillComboWithSql(self.ui.comboBoxCommune, sql, "nomcommune", "idcommune")
        self.updateButtonsStatus()

    def prefill(self):
        if self.project_id == 0 : return
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM projet WHERE idprojet=%s", (self.project_id,))
            row = cursor.fetchone()
            self.ui.lineEditNomProjet.setText(row["nom"])
            self.ui.dateEditDateLancement.setDate(row["date_lancement"])
            self.ui.dateEditDatePremierImport.setDate(row["date_premier_import"])
            self.ui.dateEditDateDernierImport.setDate(row["date_dernier_import"])
        except Exception as e:
            print(e)
            cursor.close()
        try:
            cursor.execute("SELECT commune.idcommune, commune.nomcommune FROM projet_commune JOIN commune on commune.idcommune=projet_commune.idcommune"
                           " WHERE projet_commune.idprojet=%s", (self.project_id,))
            rows = cursor.fetchall()
            for r in rows:
                item = QtGui.QListWidgetItem(r["nomcommune"])
                item.setData(Qt.Qt.UserRole, r["idcommune"])
                self.ui.listWidgetCommunes.addItem(item)
        except Exception as e:
            print(e)
            cursor.close()
        cursor.close()

    def updateButtonsStatus(self):
        self.ui.pushButtonAjouter.setEnabled(self.ui.comboBoxCommune.count() > 0)
        self.ui.pushButtonSupprimer.setEnabled(len(self.ui.listWidgetCommunes.selectedItems()) > 0)

    def addCommune(self):
        if self.ui.comboBoxCommune.count() == 0: return
        idc = self.utils.getComboValue(self.ui.comboBoxCommune)
        text = self.utils.getComboText(self.ui.comboBoxCommune)
        for i in range(0, self.ui.listWidgetCommunes.count()):
            idcommune = self.ui.listWidgetCommunes.item(i).data(Qt.Qt.UserRole)
            if idcommune == idc:
                return
        item = QtGui.QListWidgetItem(text)
        item.setData(Qt.Qt.UserRole, idc)
        self.ui.listWidgetCommunes.addItem(item)

    def removeCommune(self):
        if len(self.ui.listWidgetCommunes.selectedItems()) == 0: return
        for item in self.ui.listWidgetCommunes.selectedItems():
            self.ui.listWidgetCommunes.takeItem(self.ui.listWidgetCommunes.row(item))
        self.updateButtonsStatus()

    def save(self):
        if self.ui.lineEditNomProjet.text() == "":
            QtGui.QMessageBox.information(self, "Champs incomplets",
                                          "Veuillez remplir le nom du projet")
            self.ui.lineEditNomProjet.setFocus(Qt.Qt.OtherFocusReason)
            return
        if self.ui.listWidgetCommunes.count() == 0:
            QtGui.QMessageBox.information(self, "Champs incomplets",
                                          "Veuillez selectionner au moins une commune")
            return
        cursor = self.connection.cursor()
        values = (str(self.ui.lineEditNomProjet.text()),
                  self.ui.dateEditDateLancement.date().toPyDate(),
                  self.ui.dateEditDatePremierImport.date().toPyDate(),
                  self.ui.dateEditDateDernierImport.date().toPyDate(),
                  "MG")
        if self.project_id == 0:
            sql = "INSERT INTO projet(nom,date_lancement,date_premier_import,date_dernier_import,langue)" \
                  " VALUES(%s,%s,%s,%s,%s) RETURNING idprojet"
        else:
            sql = "UPDATE projet SET nom=%s,date_lancement=%s,date_premier_import=%s,date_dernier_import=%s,langue=%s" \
                  " WHERE idprojet=%s RETURNING idprojet"
            values = values + (self.project_id,)
        try:
            cursor.execute(sql, values)
            projetid = cursor.fetchone()[0]
            ids = []
            for idx in range(0, self.ui.listWidgetCommunes.count()):
                ids.append(self.selected_commune(idx))
            cursor.execute(
                "DELETE FROM projet_commune WHERE idprojet=%s AND idcommune NOT IN %s",
                (self.project_id, tuple(ids))
            )
            for i in ids:
                sql = "INSERT INTO projet_commune(idcommune,idprojet) SELECT %s, %s" \
                      " WHERE NOT EXISTS (SELECT 1 FROM projet_commune WHERE idcommune=%s AND idprojet=%s)"
                cursor.execute(sql, (i, projetid, i, projetid))
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()
        self.accept()

    def selected_commune(self, idx):
        item = self.ui.listWidgetCommunes.item(idx)
        if sip.getapi("QVariant") == 1:
            return item.data(Qt.Qt.UserRole).toInt()[0]
        return item.data(Qt.Qt.UserRole)
