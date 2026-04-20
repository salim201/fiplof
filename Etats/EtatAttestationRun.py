from PyQt4 import Qt, QtCore, QtGui
from PyQt4.Qt import QApplication
import os
from .EtatAttestation import Ui_Dialog
import globalvars
from models.Commune import Commune
from models.Certificat import Certificat
from models.Region import Region
from models.District import District
from models.Parcelled import Parcelled
from models.Limiteparcelle import Limiteparcelle
from models.ProprietaireParcelled import ProprietaireParcelled
from .Html2Pdf import Html2Pdf
import webbrowser
from Utils import Utils


class EtatAttestationRun(QtGui.QDialog):
    def __init__(self, parent, connection):
        QtGui.QDialog.__init__(self, parent)
        self.connection = connection
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_actions()
        self.commune = Commune.findById(self.connection, globalvars.id_commune)
        self.ui.lineEditCommune.setText(self.commune.nomcommune)
        self.district = District.findById(self.connection, self.commune.iddistrict)
        self.region = Region.findById(self.connection, self.district.idregion)

    def setup_actions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonRechercher.clicked.connect(self.rechercher)
        self.ui.pushButtonImprimer.clicked.connect(self.doprint)

    def rechercher(self):
        num = str(self.ui.lineEditNumCertificat.text())
        if len(num) > 0:
            rows = Certificat.find_by_num(self.connection, '%' + num + '%')
        else:
            rows = Certificat.find_all(self.connection)
        self.ui.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            item0 = QtGui.QTableWidgetItem(str(row.numerocertificat))
            item1 = QtGui.QTableWidgetItem(str(row.datecreation))
            item0.setFlags(item0.flags() ^ QtCore.Qt.ItemIsEditable)
            item1.setFlags(item1.flags() ^ QtCore.Qt.ItemIsEditable)
            item0.setData(QtCore.Qt.UserRole, row.idcertificat)
            item0.setData(QtCore.Qt.UserRole + 1, row.numerodemande)
            item0.setData(QtCore.Qt.UserRole + 2, row.numerocertificat)
            self.ui.tableWidget.setItem(i, 0, item0)
            self.ui.tableWidget.setItem(i, 1, item1)

    def doprint(self):
        row = self.ui.tableWidget.currentRow()
        if row < 0:
            return
        numdemande = str(self.ui.tableWidget.item(row, 0).data(QtCore.Qt.UserRole + 1).toString())
        numcertificat = str(self.ui.tableWidget.item(row, 0).data(QtCore.Qt.UserRole + 2).toString())
        parcelle = Parcelled.find_by_numdemande(self.connection, numdemande)
        limites = Limiteparcelle.find_by_parcelleid(self.connection, parcelle.gid)
        proprios = ProprietaireParcelled.find_by_parcelleid(self.connection, parcelle.gid)

        array_limites = []
        for i in limites:
            array_limites.append({"position": i.position, "description": i.description})

        array_proprios = []
        for i in proprios:
            array_proprios.append({"nom": i.nom, "prenom": i.prenom, "cin": i.cin})

        dic = {
            "$faritra": str(Utils.emptyifnull(self.region, "nomregion")),
            "$distrika": str(Utils.emptyifnull(self.district, "nomdistrict")),
            "$kaominina": str(Utils.emptyifnull(self.commune, "nomcommune")),
            "$fokontany": "...............",
            "$vohitra": "...............",
            "$superficie": "0" if parcelle is None else str(parcelle.surface),
            "$numero": numcertificat,
            "$limites": array_limites,
            "$proprios": array_proprios
        }
        converter = Html2Pdf()
        src = os.path.dirname(__file__) + "/attestation.html"
        dst = os.path.dirname(__file__) + "/attestation.pdf"
        QApplication.setOverrideCursor(Qt.Qt.WaitCursor)
        converter.generate(html=src, pdf=dst, dictionnary=dic)
        webbrowser.open(dst)
        QApplication.restoreOverrideCursor()