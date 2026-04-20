from PyQt4 import QtGui, QtCore
from .territoire import Ui_Form
try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Failed import psycopg")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class TerritoireWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TerritoireWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.checkBoxRegion.stateChanged.connect(self.setFieldsStatus)
        self.ui.checkBoxDistrict.stateChanged.connect(self.setFieldsStatus)
        self.ui.checkBoxCommune.stateChanged.connect(self.setFieldsStatus)
        self.ui.checkBoxFokontany.stateChanged.connect(self.setFieldsStatus)

        self.ui.comboBoxRegion.currentIndexChanged.connect(self.fillDistricts)
        self.ui.comboBoxDistrict.currentIndexChanged.connect(self.fillCommunes)
        self.ui.comboBoxCommune.currentIndexChanged.connect(self.fillFokontany)

        self.ui.checkBoxRegion.stateChanged.connect(self.fillRegions)
        self.ui.checkBoxDistrict.stateChanged.connect(self.fillDistricts)
        self.ui.checkBoxCommune.stateChanged.connect(self.fillCommunes)
        self.ui.checkBoxFokontany.stateChanged.connect(self.fillFokontany)

    def setFieldsStatus(self):
        self.ui.comboBoxRegion.setEnabled(self.ui.checkBoxRegion.isChecked())
        self.ui.comboBoxDistrict.setEnabled(self.ui.checkBoxDistrict.isChecked())
        self.ui.comboBoxCommune.setEnabled(self.ui.checkBoxCommune.isChecked())
        self.ui.comboBoxFokontany.setEnabled(self.ui.checkBoxFokontany.isChecked())

    def fill(self, connection):
        self.connection = connection
        self.fillRegions()

    def getComboValue(self, combo):
        index = combo.currentIndex()
        data = combo.itemData(index)
        if "toInt" in dir(data):
            return data.toInt()[0]
        if data is None:
            return 0
        return data

    def fillRegions(self):
        self.ui.comboBoxRegion.clear()
        if not self.ui.comboBoxRegion.isEnabled():
            return
        sql = "SELECT idregion, nomregion from region"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            self.ui.comboBoxRegion.addItem(_fromUtf8(row["nomregion"]), row["idregion"])

    def fillDistricts(self):
        self.ui.comboBoxDistrict.clear()
        if not self.ui.comboBoxDistrict.isEnabled():
            return
        rowid = self.getComboValue(self.ui.comboBoxRegion)
        sql = "SELECT iddistrict, nomdistrict from district WHERE idregion=%s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (int(rowid),))
        rows = cursor.fetchall()

        for row in rows:
            self.ui.comboBoxDistrict.addItem(_fromUtf8(row["nomdistrict"]), row["iddistrict"])

    def fillCommunes(self):
        self.ui.comboBoxCommune.clear()
        if not self.ui.comboBoxCommune.isEnabled():
            return
        rowid = self.getComboValue(self.ui.comboBoxDistrict)
        sql = "SELECT idcommune, nomcommune from commune WHERE iddistrict=%s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (int(rowid),))
        rows = cursor.fetchall()
        for row in rows:
            self.ui.comboBoxCommune.addItem(_fromUtf8(row["nomcommune"]), row["idcommune"])

    def fillFokontany(self):
        self.ui.comboBoxFokontany.clear()
        if not self.ui.comboBoxFokontany.isEnabled():
            return
        rowid = self.getComboValue(self.ui.comboBoxCommune)
        sql = "SELECT idfokontany, nomfokontany from fokontany WHERE idcommune=%s"
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql, (int(rowid),))
        rows = cursor.fetchall()
        for row in rows:
            self.ui.comboBoxFokontany.addItem(_fromUtf8(row["nomfokontany"]), row["idfokontany"])