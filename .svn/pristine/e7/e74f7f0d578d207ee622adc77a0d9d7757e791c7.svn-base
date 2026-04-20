from PyQt4 import QtGui, Qt
from .FondImage import Ui_Dialog
from Configuration import AppConfig


class FondImageRun(Qt.QDialog):
    def __init__(self, p):
        Qt.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.MainWindow = p
        self.initActions()
        self.initValue()

    def initActions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonBrowse.clicked.connect(self.browse)
        self.ui.pushButtonOK.clicked.connect(self.save)

    def initValue(self):
        conf = AppConfig.AppConfig()
        self.ui.lineEditFilename.setText(conf.fondimage)

    def browse(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Choisissez un fichier raster")
        if not filename:
            return
        self.ui.lineEditFilename.setText(filename)

    def save(self):
        conf = AppConfig.AppConfig()
        conf.fondimage = str(self.ui.lineEditFilename.text())
        conf.write()
        Qt.QMessageBox.warning(self, "Redemarrage", "Vous devez redemarrer l'application\npour que la configuration prenne effet", Qt.QMessageBox.Ok)
        self.accept()