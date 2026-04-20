# coding: utf8
from PyQt4.QtGui import QDialog, QApplication
from Synchronisation.syncho_Dialog import Ui_Synchronisation

class synchro_Dialog_run(QDialog):
    def __init__(self):
        super(synchro_Dialog_run, self).__init__()
        self.ui = Ui_Synchronisation()
        self.ui.setupUi(self)
        self.setWindowTitle(u"Synchronisation des données")

if __name__ == "__main__":
    app = QApplication([])
    dialog = synchro_Dialog_run()
    dialog.exec_()


    def updateProgressBar(self,i):
        self.ui.progressBar.setValue(2)