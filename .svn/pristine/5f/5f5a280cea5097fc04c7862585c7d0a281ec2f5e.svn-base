from PyQt4 import QtGui, Qt
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from .zoomTo import Ui_Dialog
#from PgCrud import PgSql, PgColumn


class zoomRun(QtGui.QDialog):
    def __init__(self,connection,canvas, parent):
        QtGui.QDialog.__init__(self)

        #self.connection = connection
        #self.pgsql = PgSql.Table(self.connection, "consistance")
        #self.pgsql.addColumn("idconsistance", "Id", True, PgColumn.ColumnType.INTEGER)
        #self.pgsql.addColumn("libelleconsistance", "Consistance")
        #self.pgsql.addColumn("parcelleoubatiment", "Momba Ny Tany")
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.move(720, 45)
        validator = QtGui.QDoubleValidator()
        self.ui.lineEdit_2.setValidator(validator)
        self.ui.lineEdit.setValidator(validator)
        self.canvas = canvas

        if QGis.QGIS_VERSION_INT >= 10900:
            self.rubberBand = QgsRubberBand(self.canvas, QGis.Point)
            self.rubberBand.setColor(Qt.red)
            # self.rubberBand.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
            self.rubberBand.setIconSize(7)
        else:
            self.vMarker = QgsVertexMarker(self.canvas)
            self.vMarker.setIconSize(10)
        self.initActions()
        #add rubberbands for cross
        self.crossRb = QgsRubberBand(self.canvas,QGis.Line)
        self.crossRb.setColor(Qt.black)
        #self.initActions()
        #self.refresh()

    def initActions(self):
        self.ui.pushButton.clicked.connect(self.zoomTo)

    def zoomTo(self):
        print "zoom button clicked!"
        x = self.ui.lineEdit_2.text()
        y = self.ui.lineEdit.text()

        if not x:
            return

        if not y:
            return
        print x + "," + y
        #scale = self.spinBox.value()
        scale = 50
        print "scale is - " + str(scale)
        rect = QgsRectangle(float(x) - scale, float(y) - scale, float(x) + scale, float(y) + scale)
        self.canvas.setExtent(rect)
        pt = QgsPoint(float(x), float(y))
        self.highlight(pt)
        self.canvas.refresh()

    def highlight(self, point):
        print "highlighting.."
        canvas = self.canvas

        currExt = canvas.extent()

        leftPt = QgsPoint(currExt.xMinimum(), point.y())
        rightPt = QgsPoint(currExt.xMaximum(), point.y())

        topPt = QgsPoint(point.x(), currExt.yMaximum())
        bottomPt = QgsPoint(point.x(), currExt.yMinimum())

        horizLine = QgsGeometry.fromPolyline([leftPt, rightPt])
        vertLine = QgsGeometry.fromPolyline([topPt, bottomPt])

        self.crossRb.reset(QGis.Line)
        self.crossRb.addGeometry(horizLine, None)
        self.crossRb.addGeometry(vertLine, None)

        if QGis.QGIS_VERSION_INT >= 10900:
            rb = self.rubberBand
            rb.reset(QGis.Point)
            rb.addPoint(point)
        else:
            self.vMarker = QgsVertexMarker(self.canvas)
            self.vMarker.setIconSize(10)
            self.vMarker.setCenter(point)
            self.vMarker.show()

        # wait .5 seconds to simulate a flashing effect
        QTimer.singleShot(500, self.resetRubberbands)

    def resetRubberbands(self):
        print "resetting rubberbands.."
        canvas = self.canvas

        if QGis.QGIS_VERSION_INT >= 10900:
            self.rubberBand.reset()
        else:
            self.vMarker.hide()
            canvas.scene().removeItem(self.vMarker)

        self.crossRb.reset()
        print "completed resetting.."

    def refresh(self):
        self.pgsql.fillTable(self.ui.tableWidget, [], "idconsistance")


