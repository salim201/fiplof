from PyQt4 import Qt, QtGui
from .login import Ui_Dialog
import psycopg2
import psycopg2.extras
import globalvars
from Utils import Utils
import hashlib


class loginRun(QtGui.QDialog):
    def __init__(self, connection):
        QtGui.QDialog.__init__(self)
        self.setModal(True)
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.utils = Utils(self.connection)
        self.fill_projects()
        self.init_actions()
        self.ui.lineEditLogin.setFocus(Qt.Qt.OtherFocusReason)

    def init_actions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.close)
        self.ui.pushButtonConnecter.clicked.connect(self.checklogin)
        self.ui.comboBoxProjet.currentIndexChanged.connect(self.fill_communes)

    def fill_projects(self):
        self.utils.fillComboWithSql(self.ui.comboBoxProjet, "SELECT idprojet,nom FROM projet", "nom", "idprojet")
        self.fill_communes()

    def fill_communes(self):
        pid = self.utils.getComboValue(self.ui.comboBoxProjet)
        if pid is None or pid == 0:
            return
        self.utils.fillComboWithSql(
            self.ui.comboBoxCommune,
            "SELECT C.idcommune,nomcommune FROM projet_commune P"
            " JOIN commune C ON C.idcommune = P.idcommune"
            " WHERE P.idprojet = " + str(pid),
            "nomcommune",
            "idcommune"
        )

    def checklogin(self):
        login = str(self.ui.lineEditLogin.text())
        pwd = hashlib.md5(str(self.ui.lineEditPwd.text())).hexdigest().upper()
        print(pwd)
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                "SELECT * FROM utilisateur WHERE loginutilisateur=%s AND upper(passwordutilisateur)=%s",
                (login, pwd)
            )
            row = cursor.fetchone()
            if not row:
                QtGui.QMessageBox.information(
                    self,
                    "Erreur d'authentification", "Veuillez verifier votre login et mot de passe"
                )
                self.ui.lineEditLogin.setFocus(Qt.Qt.OtherFocusReason)
                cursor.close()
                return
        except Exception as e:
            print(e)
            self.connection.rollback()
            return
        cursor.close()
        globalvars.id_projet = self.utils.getComboValue(self.ui.comboBoxProjet)
        globalvars.id_commune = self.utils.getComboValue(self.ui.comboBoxCommune)
        globalvars.login = str(self.ui.lineEditLogin.text())
        globalvars.id_user = row["idutilisateur"]
        globalvars.groupe_id = int(row["groupe_id"])
        self.initTerritoire(globalvars.id_commune)
        self.initCouches(globalvars.id_projet, globalvars.id_commune)
        self.accept()

    def initTerritoire(self, id_commune):
        sql = "select * from commune C "\
            "join district D on D.iddistrict = C.iddistrict "\
            "join region R on R.idregion = D.idregion WHERE C.idcommune=%s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(sql, (id_commune,))
            row = cursor.fetchone()
            if row:
                globalvars.nomcommune, globalvars.nomdistrict, globalvars.nomregion =\
                    row["nomcommune"], row["nomdistrict"], row["nomregion"]
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()

    def initCouches(self, id_projet, id_commune):
        sql = "SELECT * FROM projet_commune WHERE idcommune=%s AND idprojet=%s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(sql, (id_commune, id_projet,))
            row = cursor.fetchone()
            if row:
                globalvars.fond_image, globalvars.couche_limites = row["fond_image"], row["couche_limites"]
                globalvars.couche_cadastres, globalvars.couche_titres = row["couche_cadastres"], row["couche_titres"]
                globalvars.id_projet_commune = row["idprojet_commune"]
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()
