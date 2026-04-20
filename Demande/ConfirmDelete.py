import datetime
from PyQt4 import Qt
import globalvars
from models.Journal import Journal
from .UiConfirmDelete import Ui_Dialog


class ConfirmDelete(Qt.QDialog):
    def __init__(self, gid, connection):
        Qt.QDialog.__init__(self)
        self.gid, self.connection = gid, connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.pushButtonCancel2.clicked.connect(self.reject)
        self.ui.pushButtonConfirm.clicked.connect(self.confirm)
        self.ui.pushButtonOK.clicked.connect(self.save_motif)

    def confirm(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def save_motif(self):
        if self.ui.lineEditMotif.text().trimmed().isEmpty():
            self.ui.lineEditMotif.setFocus()
            return
        date = datetime.datetime.now()
        model = Journal(self.connection)
        model.idutilisateur = globalvars.id_user
        model.idobjetcible = self.gid
        model.typeobjectcible = "Demande"
        model.description = "Suppression Demande. Motif : %s" % self.ui.lineEditMotif.text().trimmed()
        model.dateaction = date.date()
        model.heureaction = date.time()
        if model.insert():
            self.accept()
