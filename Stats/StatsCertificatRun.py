from PyQt4 import QtGui
from .StatsCertificat import Ui_Dialog
import psycopg2
import psycopg2.extras
import pyqtgraph as pg


class StatsCertificatRun(QtGui.QDialog):
    xsql = [
        "EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM datenaissancepersonne)",
        "sexepersonne",
        "",
        ""
    ]

    def __init__(self, connection):
        super(StatsCertificatRun, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connection = connection
        self.init_actions()
        self.ui.graphicsView.setBackground([255, 255, 255])

    def init_actions(self):
        self.ui.pushButtonGenerer.clicked.connect(self.generer)

    def generer(self):
        source = self.ui.comboBoxSource.currentIndex()
        sql = """with proprio as (
            select distinct idpersonne from proprietaireparcelle_d
        )
        select %s X, count(*) Y from personnephysique A
        join proprio B on B.idpersonne = A.idpersonne
        GROUP BY X
        ORDER BY X
        """

        sql = sql % (self.xsql[source])
        rows = self.execute(sql)
        self.fill_table(rows)
        self.fill_graph(rows)

    def execute(self, sql):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        rows = []
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception as e:
            print(e)
            cursor.close()
            self.connection.rollback()
        return rows

    def fill_table(self, rows):
        self.ui.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.ui.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(str(row["x"])))
            self.ui.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(str(row["y"])))

    def fill_graph(self, rows):
        xVals = map(lambda r: r['x'], rows)
        yVals = map(lambda r: r['y'], rows)
        bg1 = pg.BarGraphItem(x=xVals, height=yVals, width=1, brush='#dc3348')
        self.ui.graphicsView.clear()
        self.ui.graphicsView.addItem(bg1)
