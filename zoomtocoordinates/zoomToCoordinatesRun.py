from PyQt4 import QtCore, QtGui
# Import the PyQt and QGIS libraries
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from .ZoomToXY import Ui_ZoomToXY
# create the dialog for qgsPlof

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
class zoomToCoordinates(QtGui.QDialog):

  def __init__(self,connection,canvas,parent):
    QtGui.QDialog.__init__(self)
    # Set up the user interface from Designer.
    self.canvas = canvas
    self.parent = parent
    self.ui = Ui_ZoomToXY ()
    self.ui.setupUi(self)
    self.x = ""
    self.y = ""

    # validations
    validator = QtGui.QDoubleValidator()
    lEditX = self.ui.X_lineEdit
    lEditY = self.ui.Y_lineEdit
    lEditX.setValidator(validator)
    lEditY.setValidator(validator)

    # create rubberband for point..for qgis 1.9 and higher
    self.rubberBand = None

    # create vertex marker for point..older versons..
    self.vMarker = None

    # add rubberbands for cross
    self.crossRb = QgsRubberBand(self.canvas, QGis.Line)
    self.crossRb.setColor(Qt.black)

    if QGis.QGIS_VERSION_INT >= 10900:
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Point)
        self.rubberBand.setColor(Qt.red)
        # self.rubberBand.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
        self.rubberBand.setIconSize(7)
    else:
        self.vMarker = QgsVertexMarker(self.canvas)
        self.vMarker.setIconSize(10)

    self.ui.span.clicked.connect(self.pan)

  def zoomToXY(self):
      print "fdf"

  def keyPressEvent(self, event):

      key = event.key()
      if key == Qt.Key_Escape:
          self._clearSearch()
      else:
          self.zoom()
          #QLineEdit.keyPressEvent(self, event)

  def zoom(self):
      print "zoom button clicked!"
      x = self.ui.X_lineEdit.text()
      y = self.ui.Y_lineEdit.text()

      if not x:
          return

      if not y:
          return

      print
      x + "," + y
      scale = self.ui.spinBox.value()
      #scale = 10
      print
      "scale is - " + str(scale)
      rect = QgsRectangle(float(x) - scale, float(y) - scale, float(x) + scale, float(y) + scale)
      self.canvas.setExtent(rect)
      pt = QgsPoint(float(x), float(y))
      i = 0
      if self.x != str(x):
          self.x = str(x)
          self.y = str(y)
          rowPosition = self.ui.tableWidget.rowCount()
          #self.parent.tableWidget.setColumnCount(columns)
          self.ui.tableWidget.insertRow(rowPosition)
          self.ui.tableWidget.setColumnCount(2)
          item = QtGui.QTableWidgetItem()
          item.setText(_translate("", str(x), None))
          self.ui.tableWidget.setItem(rowPosition, 0, item)

          item = QtGui.QTableWidgetItem()
          item.setText(_translate("", str(y), None))
          self.ui.tableWidget.setItem(rowPosition, 1, item)

          self.highlight(pt)
          self.createVertexMarkerAt(pt)
      else :
          print "xxx"
          self.highlight(pt)
          self.createVertexMarkerAt(pt)

      self.canvas.refresh()

  def addCoordinates(self):
      print "fsdfsdf"

  def createVertexMarkerAt(self, p):
      marker = QgsVertexMarker(self.canvas)
      marker.setColor(QColor(255, 100, 0))
      marker.setIconSize(10)
      marker.setIconType(QgsVertexMarker.ICON_BOX)
      marker.setPenWidth(3)
      marker.hide()
      marker.show()
      marker.setCenter(p)
      self.canvas.refresh()
      return marker
  def pan(self):
      print
      "pan button clicked!"
      x = self.ui.X_lineEdit.text()
      y = self.ui.Y_lineEdit.text()

      if not x:
          return

      if not y:
          return

      print
      x + "," + y

      canvas = self.canvas
      currExt = canvas.extent()

      canvasCenter = currExt.center()
      dx = float(x) - canvasCenter.x()
      dy = float(y) - canvasCenter.y()

      xMin = currExt.xMinimum() + dx
      xMax = currExt.xMaximum() + dx
      yMin = currExt.yMinimum() + dy
      yMax = currExt.yMaximum() + dy

      newRect = QgsRectangle(xMin, yMin, xMax, yMax)
      canvas.setExtent(newRect)
      pt = QgsPoint(float(x), float(y))

      i = 0

      if self.x != str(x):
          self.x = str(x)
          self.y = str(y)
          rowPosition = self.ui.tableWidget.rowCount()
          #self.parent.tableWidget.setColumnCount(columns)
          self.ui.tableWidget.insertRow(rowPosition)
          self.ui.tableWidget.setColumnCount(2)
          item = QtGui.QTableWidgetItem()
          item.setText(_translate("", str(x), None))
          self.ui.tableWidget.setItem(rowPosition, 0, item)

          item = QtGui.QTableWidgetItem()
          item.setText(_translate("", str(y), None))
          self.ui.tableWidget.setItem(rowPosition, 1, item)

          self.highlight(pt)
          self.createVertexMarkerAt(pt)
      else :
          print "xxx"
          self.highlight(pt)
          self.createVertexMarkerAt(pt)
      self.canvas.refresh()

  def flash(self):
      print
      "flash button clicked!"

      x = self.dlg.ui.mTxtX.text()
      y = self.dlg.ui.mTxtY.text()

      if not x:
          return

      if not y:
          return
      pt = QgsPoint(float(x), float(y))
      self.highlight(pt)

  def highlight(self, point):
      print
      "highlighting.."
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
      print
      "resetting rubberbands.."
      canvas = self.canvas

      if QGis.QGIS_VERSION_INT >= 10900:
          self.rubberBand.reset()
      else:
          self.vMarker.hide()
          canvas.scene().removeItem(self.vMarker)

      self.crossRb.reset()
      print
      "completed resetting.."

