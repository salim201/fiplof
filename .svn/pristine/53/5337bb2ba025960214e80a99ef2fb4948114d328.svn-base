from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import psycopg2
from PyQt4 import Qt, QtGui
from .connect import Ui_Dialog


class ConnectRun(QDialog):
    def __init__(self, connection, parent):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.parent = parent
        self.initActions()
        # self.ui.pushButtonConnexion.triggered.connect(self.checkAccessFIPLOF)

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.close)
        self.ui.pushButtonConnexion.clicked.connect(self.checkAccessFIPLOF)

    def checkAccessFIPLOF(self):
        login = str(self.ui.loginLineEdit.text())
        pwd = str(self.ui.motDePasseLineEdit.text())
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM utilisateur WHERE loginutilisateur=%s AND passwordutilisateur=%s",
                           (login, pwd))
            rows = cursor.fetchall()
            if (len(rows) == 0):
                QtGui.QMessageBox.information(self, "Erreur d'authentification",
                                              "Veuillez verifier votre login et mot de passe")
                self.ui.loginLineEdit.setFocus(Qt.Qt.OtherFocusReason)
                cursor.close()
                return
        except Exception as e:
            print(e)
            self.connection.rollback()
            return
        cursor.close()
        self.parent.ui.menu_Saisie_Des_Donn_es.setEnabled(True)
        self.parent.ui.menuCalcul_Impots.setEnabled(True)
        self.parent.ui.menuAutres.setEnabled(True)
        self.parent.ui.menuParam_tres.setEnabled(True)
        self.parent.ui.action_Connexion.setEnabled(False)
        self.parent.ui.actionD_connexion.setEnabled(True)
        self.parent.labelConnectedAs.setText("*FIPLOF*")
        self.accept()
