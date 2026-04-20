from PyQt4 import QtGui, QtCore
from .AddLayerRun import AddLayerRun
from .AddLayerAdministrationRun import AddLayerAdministrationRun
from .ParamProjets import Ui_Dialog
from models.ProjetCouche import ProjetCouche
from Utils import Utils
import globalvars

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Commune:
    def __init__(self, fi, ct, cc, cl):
        self.fond_image = "" if fi is None else fi
        self.couche_titres = "" if ct is None else ct
        self.couche_cadastres = "" if cc is None else cc
        self.couche_limites = "" if cl is None else cl

    def __setitem__(self, key, value):
        if key == "fond_image":
            self.fond_image = value
        if key == "couche_titres":
            self.couche_titres = value
        if key == "couche_cadastres":
            self.couche_cadastres = value
        if key == "couche_limites":
            self.couche_limites = value


class ParamProjetsRun(QtGui.QDialog):
    def __init__(self, connection):
        self.communes = {}  # type: list[Commune]
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.utils = Utils(self.connection)
        self.fillProjets()
        self.initActions()
        header = self.ui.tableWidget.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        self.senderName = self.sender().objectName()
        print self.senderName

    def initActions(self):
        self.ui.comboBoxProjets.currentIndexChanged.connect(self.fillCommunes)
        self.ui.comboBoxCommunes.currentIndexChanged.connect(self.fillProperties)
        self.ui.pushButtonAddLayer.clicked.connect(self.addLayer)
        self.ui.pushButtonDelLayer.clicked.connect(self.delLayer)
        self.ui.pushButtonAppliquer.clicked.connect(self.accept)
        self.ui.pushButtonUp.clicked.connect(self.order_up)
        self.ui.pushButtonDown.clicked.connect(self.order_down)
        self.ui.tableWidget.cellDoubleClicked.connect(self.editLayer)
        self.ui.tableWidget.cellClicked.connect(self.updateToolbar)

    def fillProjets(self):
        self.utils.fillComboWithSql(self.ui.comboBoxProjets, "SELECT idprojet, nom FROM projet", "nom", "idprojet")
        self.fillCommunes()

    def fillCommunes(self):
        projetid = self.utils.getComboValue(self.ui.comboBoxProjets)
        if projetid is None or projetid < 0:
            return
        self.utils.fillComboWithSql(
            self.ui.comboBoxCommunes,
            "SELECT C.nomcommune, P.idprojet_commune FROM"
            " projet_commune P"
            " JOIN commune C ON C.idcommune = P.idcommune"
            " WHERE P.idprojet = " + str(projetid),
            "nomcommune",
            "idprojet_commune"
        )
        self.fillProperties()

    def fillProperties(self):
        idprojet_commune = self.utils.getComboValue(self.ui.comboBoxCommunes)
        couches = ProjetCouche.find_by_projet_commune(self.connection, idprojet_commune)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setRowCount(len(couches))
        for i, couche in enumerate(couches):
            t = 'Shapefile'
            if couche.type_couche == 'R':
                t = 'Raster'
            icon = Utils.create_icon(QtGui.QColor(couche.couleur_bg))
            item_icon = QtGui.QTableWidgetItem()
            item_icon.setIcon(icon)
            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(couche.libelle))
            self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(t))
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(couche.fichier))
            self.ui.tableWidget.setItem(i, 3, item_icon)
            item_icon.setData(QtCore.Qt.UserRole, couche.id)
        for i in range(0, 4):
            Utils.setTableWidgetColumnReadOnly(self.ui.tableWidget, i)
        self.updateToolbar()

    def addLayer(self):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
        idprojet_commune = self.utils.getComboValue(self.ui.comboBoxCommunes)
        if not idprojet_commune:
            return
        if self.senderName == "actionAjout_couche_administration_Fonci_re":
            dialog = AddLayerAdministrationRun(self.connection, idprojet_commune)
            if dialog.exec_():
                self.fillProperties()
        else:
            dialog = AddLayerRun(self.connection, idprojet_commune)
            if dialog.exec_():
                self.fillProperties()

    def selected_couche_id(self):
        index = self.ui.tableWidget.currentIndex()
        if not index.isValid():
            return None
        rowid = index.row()
        couche_id = self.ui.tableWidget.item(rowid, 3).data(QtCore.Qt.UserRole).toInt()[0]
        return couche_id

    def delLayer(self):
        res = QtGui.QMessageBox.question(
            self, "Confirmation", "Voulez-vous vraiment supprimer la couche ?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        )
        if res == QtGui.QMessageBox.No:
            return
        couche_id = self.selected_couche_id()
        if not couche_id:
            return
        couche = ProjetCouche.find_by_id(self.connection, couche_id)
        if couche.certifiable != 1:
            ProjetCouche.delete_by_id(self.connection, couche_id)
        else:
            if globalvars.groupe_id == 1:
                ProjetCouche.delete_by_id(self.connection, couche_id)
            else:
                QtGui.QMessageBox.critical(None, "Erreur", "Impossible de supprimer cette couche!")
        self.fillProperties()

    def editLayer(self, rowid):
        idprojet_commune = self.utils.getComboValue(self.ui.comboBoxCommunes)
        if not idprojet_commune:
            return
        couche_id = self.selected_couche_id()
        if not couche_id:
            return
        dialog = AddLayerRun(self.connection, idprojet_commune, couche_id)
        if dialog.exec_():
            self.fillProperties()

    def updateToolbar(self):
        index = self.ui.tableWidget.currentIndex()
        enabled = index.isValid()
        enable_down = index.isValid() and index.row() < self.ui.tableWidget.rowCount() - 1
        enable_up = index.isValid() and index.row() > 0
        self.ui.pushButtonDown.setEnabled(enable_down)
        self.ui.pushButtonUp.setEnabled(enable_up)
        self.ui.pushButtonDelLayer.setEnabled(enabled)

    def reorder(self, sens):
        current_couche = self.selected_couche_id()
        couches = []
        for i in range(0, self.ui.tableWidget.rowCount()):
            couche_id = self.ui.tableWidget.item(i, 3).data(QtCore.Qt.UserRole).toInt()[0]
            couches.append(couche_id)
        current_pos = couches.index(current_couche)
        if current_pos >= len(couches) - 1 and sens > 0:
            return
        if current_pos == 0 and sens < 0:
            return
        new_pos = current_pos + sens
        couches.insert(new_pos, couches.pop(current_pos))
        ProjetCouche.reorder(self.connection, couches)
        self.fillProperties()
        self.ui.tableWidget.selectRow(new_pos)
        self.updateToolbar()

    def order_down(self):
        self.reorder(+1)

    def order_up(self):
        self.reorder(-1)
