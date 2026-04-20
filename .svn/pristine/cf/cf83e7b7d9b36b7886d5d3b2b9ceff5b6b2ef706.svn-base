
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
from LParcelle import Ui_Lev
import globalvars



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

class lparcelle(QtGui.QDialog):

  def __init__(self,connection,canvas,parent):
    QtGui.QDialog.__init__(self, parent.MainWindow)
    # Set up the user interface from Designer.
    try :
      print('at validator code')
      self.ui = Ui_Lev()

      #self.canvas = parent.canvas
      self.canvas = canvas
      self.parent = parent
      self.MainWindow = self.parent.MainWindow
      self.pid = 0
      self.iddemande = 0
      self.idparcelle = 0
      self.id_projet = globalvars.id_projet
      self.currentGeomIdParcelle = 0
      self.currvalDemande = 0
      self.selectedRow = 0

      self.tabGeom = []
      self.connection = connection
      self.ui.setupUi(self)

      validator = QtGui.QDoubleValidator()
      lEditX = self.ui.X_lineEdit
      lEditY = self.ui.Y_lineEdit
      self.markers = []
      lEditX.setValidator(validator)
      lEditY.setValidator(validator)

      # with open('TempGPS_L.txt') as f:
      #     lines = f.readlines()
      #     print("lines")
      #     print(lines)

    except Exception as e:
        print(e)




#    self.parent = parent
#    print self.parent.txt


    # create rubberband for point..for qgis 1.9 and higher
    self.rubberBand = None

    # create vertex marker for point..older versons..
    self.vMarker = None
    try :
      self.initActions()
      self.ui.TransformDemande.clicked.connect(self.createGeometry)
      self.ui.tableWidget.cellClicked.connect(self.cellSelected)
      #self.ui.removeMarks.triggered.connect(self.removeRow())
    except Exception as e:
      print(e)



    # add rubberbands for cross
    self.crossRb = QgsRubberBand(self.canvas, QGis.Line)
    self.crossRb.setColor(Qt.black)
    #
    if QGis.QGIS_VERSION_INT >= 10900:
         self.rubberBand = QgsRubberBand(self.canvas, QGis.Point)
         self.rubberBand.setColor(Qt.red)
         #self.rubberBand.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
         #self.rubberBand.setIconSize(7)
    else:
         self.vMarker = QgsVertexMarker(self.canvas)
         self.vMarker.setIconSize(10)

  def initActions(self):
    self.ui.xyFromGPS.clicked.connect(self.zoomTo)
    self.ui.removeMarks.clicked.connect(self.removeRow)

  def cellSelected(self,row,column):
      self.selectedRow = row

  def removeRow(self):

      #self.currentIndex = int(self.ui.tableWidget.currentIndex())
      currentRow = self.ui.tableWidget.currentRow()
      rowCount = self.ui.tableWidget.rowCount()
      columnCount = self.ui.tableWidget.columnCount()

      try:
          # Si table Demandeurs
          if currentRow == -1:
              print "dqsd"
              QMessageBox.critical(self.ui.tableWidget, "Erreur", "Veuillez entrer au moins choisir une ligne")
              return
          else:
              print "test"
              self.ui.tableWidget.removeRow(self.selectedRow)
              #if (len(self.data) >= 1):
              #    self.data.pop(self.selectedRow)
          #if self.currentIndex == 0:


          #             # Si table Voisins
          # if self.currentIndex == 1:
          #     if currentRWVoisin == -1:
          #         print "dqsd"
          #         QMessageBox.critical(self.ui.tableVoisin, "Erreur", "Veuillez entrer au moins choisir une ligne")
          #         return
          #     else:
          #         print "test"
          #         self.ui.tableVoisin.removeRow(self.selectedRow)
          #         # if (len(self.data) >= 1) :
          #         #    self.data.pop(self.selectedRow)
      except Exception as e:
          print(e)

  def zoomTo(self):
    print "zoom button clicked!"
    x = self.ui.X_lineEdit.text()
    y = self.ui.Y_lineEdit.text()
    desc = self.ui.lineEdit.text()
    data = []
    data.append(x)
    data.append(y)
    data.append(desc)

    if not x:
      return

    if not y:
      return
    print x + "," + y
    # scale = self.spinBox.value()
    scale = 50
    print
    "scale is - " + str(scale)
    if ((x == str(0)) or (y== str(0))) :
        return

    rect = QgsRectangle(float(x) - scale, float(y) - scale, float(x) + scale, float(y) + scale)
    self.canvas.setExtent(rect)
    pt = QgsPoint(float(x), float(y))
    mk = self.createVertexMarkerAt(pt)
    if mk is not None :
        self.markers.append(mk)
    self.highlight(pt)

    print("---self.markers------")
    print(self.markers)
    try :
        self.addValueTable(data)

        self.ui.X_lineEdit.setText(str(int(0)))
        self.ui.Y_lineEdit.setText(str(int(0)))

    except Exception as e:
        print(e)


  #   self.x = str(x)
  #   self.y = str(y)
  #   rowPosition = self.ui.tableWidget.rowCount()
  # # self.parent.tableWidget.setColumnCount(columns)
  #   self.ui.tableWidget.insertRow(rowPosition)
  #   self.ui.tableWidget.setColumnCount(2)
  #   item = QtGui.QTableWidgetItem()
  #   item.setText(_translate("", str(x), None))
  #   self.ui.tableWidget.setItem(rowPosition, 0, item)
  #
  #   item = QtGui.QTableWidgetItem()
  #   item.setText(_translate("", str(y), None))
  #   self.ui.tableWidget.setItem(rowPosition, 1, item)
  #
  #   item = QtGui.QTableWidgetItem()
  #   item.setText(_translate("", str(desc), None))
  #   self.ui.tableWidget.setItem(rowPosition, 2, item)
    self.canvas.refresh()

  def addValueTable(self, data):
      columns = len(data)
      print "add data in"
      self.isIn = 0
      rowPosition = self.ui.tableWidget.rowCount()
      i = 0
      print("DATA-id")
      # if rowPosition >= 1 :
      #     while (i < rowPosition ) :
      #         j = 0
      #         idD = self.ui.tableDemande.item(i,5).text()
      #         if int(idD) == int(data[5]):
      #             self.isIn = 1
      #             break
      #         i = i + 1
      #
      # if self.isIn == 1:
      #     QMessageBox.critical(self.ui.tableDemande, "Erreur", "Demandeur deja enregistrE")
      #     return
      # else :
      self.ui.tableWidget.setColumnCount(columns)
      self.ui.tableWidget.insertRow(rowPosition)
      self.isIn = 0
      for i in range(len(data)):
          item = QtGui.QTableWidgetItem()
          item.setText(_translate("", str(data[i]), None))
          self.ui.tableWidget.setItem(rowPosition, i, item)


  def keyPressEvent(self, event):

    key = event.key()
    if key == Qt.Key_Escape:
      self._clearSearch()
    else:
      self.zoomTo()
      # QLineEdit.keyPressEvent(self, event)

  def zoom(self):
    print
    "zoom button clicked!"
    x = self.ui.X_lineEdit.text()
    y = self.ui.Y_lineEdit.text()

    if not x:
      return

    if not y:
      return

    print
    x + "," + y
    scale = self.ui.spinBox.value()
    # scale = 10
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
      # self.parent.tableWidget.setColumnCount(columns)
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
    else:
      print
      "xxx"
      self.highlight(pt)

      mk = self.createVertexMarkerAt(pt)
      self.markers.append(mk)

    self.canvas.refresh()

  def addNewGeometri(self, geometry):

      x = None
      self.idparcelle = 0

      strgeom = ""
      self.ok = 0
      if (geometry.isGeosValid()):
          if geometry.wkbType() == QGis.WKBPolygon:
              x = geometry.asPolygon()
          if geometry.wkbType() == QGis.WKBMultiPolygon:
              x = geometry.asMultiPolygon()[0]
          if self.check_geom_equals(geometry.exportToWkt()):
              return -1
          else:
              cur = self.connection.cursor()
              try:
                  num = ""
                  exe = cur.execute(
                      "INSERT INTO parcelle_d (numero,geom,surface ,id_commune)VALUES (%s, ST_GeomFromText(%s, " + str(
                          globalvars.EPSG_SCR) + "),ST_Area(%s), %s) returning gid,surface",
                      (num, str(geometry.exportToWkt()), str(geometry.exportToWkt()), globalvars.id_commune))
                  self.connection.commit()
                  dm = cur.fetchone()
                  if (len(dm) > 0):
                      self.ok = 1
                      self.iddemande = dm[0]
                      self.pid = dm[0]
                      self.idparcelle = dm[0]
                      self.currentGeomIdParcelle = dm[0]
                      self.currvalDemande = self.iddemande
              except Exception as e:
                  self.connection.rollback()
                  return 0
                  print(e)
      return self.idparcelle


  def getNearestPoint(self):
      print(" find point to snapp")
  def createGeometry(self):
      self.tabGeom = []
      from Demande.DemandeFormRun import DemandeFormRun
      rowCount = self.ui.tableWidget.rowCount()
      print('rowPosition')
      print(rowCount)

      if rowCount == 0:
          QMessageBox.critical(self.ui.TransformDemande, "Erreur", "Veuillez au moins inserer trois points ")
          return
      if rowCount <= 2:
          QMessageBox.critical(self.ui.TransformDemande, "Erreur", "Veuillez au moins inserer trois points ")
          return
      i = 0

      try :

          while (i < rowCount):
              j = 0
              x = self.ui.tableWidget.item(i,0).text()
              y = self.ui.tableWidget.item(i,1).text()
              i = i + 1
              print("---X---")
              print(float(x))

              print("---Y---")
              print(float(y))

              self.tabGeom.append(QgsPoint(float(x),float(y)))

          print('self.tabGeom')
          print(self.tabGeom)

          newgeom = QgsGeometry.fromPolygon([self.tabGeom])
          etat = self.addNewGeometri(newgeom)
          if etat == 0 :
              QMessageBox.critical(self.MainWindow.canvas, "Erreur", "Geometry  invalide")
              return
          if etat == -1 :
              QMessageBox.critical(self.MainWindow.canvas, "Erreur", "Geometry  existante")
              return
          demande = DemandeFormRun(self)
          self.removeMarkers()
          self.canvas.refresh()
          result = demande.exec_()
          print("--etat--")
          print(etat)


      except Exception as e:
          print(e)
         #QgsP =
      #if(rowPosition)

      # try:
      #     rows = provider.openFile()
      # except:
      #     QMessageBox.warning(self.iface.mainWindow(), "Unable to open file", "Unable to open file: " + unicode(filename))
      #     return
      # layer = self.createMemoryLayer()
      # if len(rows) == 0:
      #     QMessageBox.warning(self.iface.mainWindow(), "No rows found", "Please choose a spreadsheet with more then one row filled.")
      #     return
      # attrCount = len(rows[0])
      # for col in rows[0]:
      #     layer.dataProvider().addAttributes([QgsField(unicode(col), QVariant.String)])
      # # see: http://osgeo-org.1803224.n2.nabble.com/Add-attributes-to-memory-provider-with-python-td6073149.html
      # if hasattr(layer, 'updateFields'):
      #     layer.updateFields()
      # else: # <= 1.8 compatibility
      #     layer.updateFieldMap()
      # xyOk = False
      # if self.getXyColumns(layer):
      #     xyOk = True
      # # fill rows
      # #print self.layerInfo[self.layer]
      # #print()
      # #geometry = QgsGeometry.fromPolygon(row)
      # print("Geometry FROM XLS")
      # print(xyOk)
      #
      # for row in rows :
      #     print "rows in"
      #     #print row
      #     #print "rows out"
      #     if not row == rows[0]:
      #         f = QgsFeature()
      #         if xyOk:
      #             #x=row[self.layerInfo[self.layer].xIdx]
      #             #y=row[self.layerInfo[self.layer].yIdx]
      #             x = row[0]
      #             y = row[1]
      #             print(x)
      #             print(y)
      #             if type(x) in types.StringTypes or type(y) in types.StringTypes:
      #                 # mmm, we have strings as values... try to cast to float
      #                 try:
      #                     print "at try"
      #                     x = float(x)
      #                     y = float(y)
      #
      #
      #
      #                 except:
      #                     QMessageBox.warning(self.iface.mainWindow(), "Non numeric value found", "This spreadsheet contained non numeric values in one of the x or y columns. Values found: '" + unicode(x) + "' and '" + unicode(y) + "'.\nYou can open it without x and y columns by NOT choosing x and y columns (click Cancel in that dialog).\nRemoving the layer...")
      #                     QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
      #                     return
      #             self.tabGeom.append(QgsPoint(x, y))
      #             f.setGeometry(QgsGeometry.fromPoint( QgsPoint(x,y) ) )
      #             m = self.createVertexMarkerAt(QgsPoint(x,y))
      #             self.markers.append(m)
      #
      #         else:
      #             f.setGeometry( QgsGeometry.fromWkt('POINT(0 0)') )
      #         if QGis.QGIS_VERSION_INT < 10900:
      #             f.setAttributeMap( dict(zip( range(0,len(row)) ,row ))  )
      #         else:
      #             # put row in a list, because UNO returns a tuple, which raises an exception
      #             f.setAttributes( list(row)  )
      #         layer.dataProvider().addFeatures([f])
      # print("Geometry FROM XLS")
      # try:
      #     print(self.tabGeom)
      #     geom = QgsGeometry.fromPolygon([self.tabGeom])
      #     polygon = QgsRubberBand(self.canvas)
      #     polygon.setToGeometry(QgsGeometry.fromPolygon([self.tabGeom]), None)
      #     #polygon.setColor(QColor(0, 0, 255))
      #     #polygon.setFillColor(QColor(255, 255, 0))
      #     polygon.setWidth(1)
      #     #polygon.show()
      #     g = f.geometry()
      #
      #     if geom.wkbType() == QGis.WKBPolygon:
      #         print("POYGON")
      #     if geom.wkbType() == QGis.WKBMultiPolygon:
      #         print("multi POYGON")
      #     idCommune = 3
      #     num =""
      #     consistance = "TRANO"
      #     cursor = self.connection.cursor()
      #     exe = cursor.execute(
      #      "INSERT INTO parcelle_d (numero,geom,surface ,id_commune,consistance)VALUES (%s, ST_GeomFromText(%s, "+str(globalvars.EPSG_SCR)+"),ST_Area(%s), %s, %s) returning gid,surface",
      #       (num, str(geom.exportToWkt()), str(geom.exportToWkt()), idCommune, str(consistance)))
      #     self.connection.commit()
      # except Exception as e:
      #     print(e)
      # layer.updateExtents()
      # layer.reload()
      # self.removeMarkers()
      # # trying to force a repaint
      # self.canvas.updateFullExtent()
      # self.canvas.setDirty(True)
      # self.canvas.refresh()
      # self.canvas.refresh()
      # self.canvas.refresh()
      # self.canvas.refresh()
      # self.canvas.zoomByFactor(0.99)


  def createVertexMarkerAt(self, p):
    marker = QgsVertexMarker(self.canvas)
    marker.setColor(QColor(255, 100, 0))
    marker.setIconSize(10)
    marker.setIconType(QgsVertexMarker.ICON_CROSS) #ICON_CROSS  ICON_X ICON_BOX
    marker.setPenWidth(3)
    marker.hide()
    marker.show()
    marker.setCenter(p)
    self.canvas.refresh()
    return marker
  def removeMarkers(self):
      print "remove Markers"

      for v in self.markers:
          self.canvas.scene().removeItem(v)
      self.canvas.refresh()
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
      # self.parent.tableWidget.setColumnCount(columns)
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
    else:
      print
      "xxx"
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

  def check_geom_equals(self, wkt):
      cur = self.connection.cursor()
      try:
          cur.execute(
              "SELECT pd.gid FROM parcelle_d pd WHERE ST_Equals(pd.geom::geometry, ST_GeomFromText(%s, " + str(
                  globalvars.EPSG_SCR) + ")) ", (str(wkt),))
          res = cur.fetchall()
          print res
          if len(res) > 0:
              return True
          else:
              return False
      except StandardError as e:
          print e
          QMessageBox.critical(self.MainWindow.canvas, "Erreur", " Geometry invalide")
          self.connection.rollback()
          return False