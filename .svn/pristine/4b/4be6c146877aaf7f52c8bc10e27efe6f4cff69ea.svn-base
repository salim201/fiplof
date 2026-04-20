'''
Created on 12/10/2014

@author: ferrari
'''
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4.QtCore import Qt
from qgis.gui import QgsMapTool
#from qgis.utils import iface
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui  import QgsMessageBar
from PyQt4.QtCore import Qt, QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt4.QtGui import QMessageBox, QAction, QIcon, QProgressBar
from PyQt4.QtSql import *

from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *

from PyQt4 import QtCore, QtGui

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



class MultipleLayersEditNodesButton(QgsMapTool):

    def __init__(self, iface, canvas,parent):
        #super(self).__init__()
        #super(QObject,self).__init__()
        self.canvas = canvas
        self.iface = iface

        self.active = False
        self.currentGeom = None
        self.currentVertex = None
        self.dragging = False
        self.parent = parent
        self.dragging = False
        self.MainWindow = self.parent.MainWindow
        self.del_vertex = QtGui.QAction(self.MainWindow)
        self.del_vertex.setShortcut(QtGui.QKeySequence("Del"))
        #self.del_vertex.setShortcut( QtGui.QApplication.translate("MainWindow", "Del", None, QtGui.QApplication.UnicodeUTF8))
        self.del_vertex.triggered.connect(self.removeVertex)
        #self.parent.ui.actiondelVertex.triggered.connect(self.removeVertex)
        self.layer = self.parent.LayerToEdit
        #self.layer = canvas.currentLayer()
        self.CurrIndxLayer =  self.parent.CurrIndxLayer
        self.feature = None
        #self.layer = canvas.currentLayer()

        QgsMapTool.__init__(self,canvas)

    def selectedFeature(self, e):
        self.feature = None
        point = self.toLayerCoordinates(self.layer, e.pos())
        d = self.canvas.mapUnitsPerPixel() * 4
        for feat in self.layer.getFeatures():
            if feat.geometry().intersects(QgsRectangle((point.x() - d), (point.y() - d), (point.x() + d), (point.y() + d))):
                self.feature = feat
                return

    def selectedVertexIndex(self, e):

        self.vertexIndex = None
        if self.feature is None: return

        point = self.toLayerCoordinates(self.layer, e.pos())
        geom = self.feature.geometry()

        x = None
        if geom.wkbType() == QGis.WKBPolygon:
            x = geom.asPolygon()
        if geom.wkbType() == QGis.WKBMultiPolygon:
            x = geom.asMultiPolygon()[0]
        d = self.canvas.mapUnitsPerPixel() * 5
        r = QgsRectangle((point.x() - d), (point.y() - d), (point.x() + d), (point.y() + d))
        index = 0
        if(len(x) == 0):
            return

        for p in x[0]:
            m = self.createVertexMarkerAt(p)
            self.markers.append(m)
        self.parent.featureEdit = self.feature
        self.parent.crrGeom = x
        self.parent.markersMultiEdit = self.markers
        for p in x[0]:
            if r.contains(p):
                self.vertexIndex = index
                print "in loop "
                print self.vertexIndex
                print 'x'
                print x[0][self.vertexIndex].x()
                print 'y'
                print x[0][self.vertexIndex].y()


                self.canvas.scene().removeItem(self.markers[self.vertexIndex])
                self.currentVertex = x[0][self.vertexIndex]
                self.parent.vertexIndex = self.vertexIndex
                self.parent.currentVertex = x[0][self.vertexIndex]
                mn = self.repaintVertexMarkerAt(x[0][self.vertexIndex])
                self.markers.append(mn)
                #self.markers[self.vertexIndex].setColor(QColor(255, 100, 0))
                #self.canvas.refresh()
                return
            index += 1








        #self.canvas.scene().removeItem(self.markers[self.vertexIndex])
        print "selected Vertex"
        print self.vertexIndex
        #mn = self.repaintVertexMarkerAt(x[0][self.vertexIndex])
        #self.markers.append(mn)

        self.currentGeom = x

        if e.button() == Qt.RightButton:
            menu = QMenu()
            delSommet = menu.addAction(QIcon("icone/marker--minus.png"),"Supprimer le sommet")
            action = menu.exec_(self.canvas.mapToGlobal(QPoint(e.pos().x() + 5, e.pos().y())))
            if action == delSommet :
                self.removeVertex()



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

    def repaintVertexMarkerAt(self, p):
        marker = QgsVertexMarker(self.canvas)
        #marker.setColor(QColor(0, 255, 0))
        marker.setCenter(p)
        marker.setColor(QColor(0, 255, 0))
        #marker.setFillColor(QColor(255, 255, 0))
        marker.setIconSize(10)
        marker.setIconType(QgsVertexMarker.ICON_BOX)
        #marker.setIconType(QgsVertexMarker.ICON_DOUBLE_TRIANGLE)
        marker.setPenWidth(3)
        marker.hide()
        marker.show()
        marker.setCenter(p)
        self.canvas.refresh()
        return marker

    def canvasPressEvent(self, e):

        #print "canvasPressEvent in"
        #self.dragging = True
        for m in self.markers:
            self.canvas.scene().removeItem(m)
        self.markers = []
        if e.button() == Qt.RightButton:
            print "Qt.RightButton::"

        self.selectedFeature(e)
        self.selectedVertexIndex(e)

        if e.button() == Qt.RightButton:
            menu = QMenu()
            #annuler = menu.addAction(QIcon("icone/layer_del.png"),"Annuler le tracage")
            delSommet = menu.addAction(QIcon("icone/marker--minus.png"),"Supprimer le sommet")
            #moveVertex = menu.addAction(QIcon("icone/digitizing/prolongline.png"), "Deplacer  sommet")
            action = menu.exec_(self.canvas.mapToGlobal(QPoint(e.pos().x() + 5, e.pos().y())))


            if action == delSommet :
                print "removeVertex"
                self.removeVertex()




        print "canvasPressEvent print self.vertexIndex canvasPressEvent"
        #print self.vertexIndex
        self.mouseDown = True


    def paintCurrentVertex(self):
        print 'test'
    def canvasDoubleClickEvent(self, e):
        print "canvasDoubleClickEvent "
        self.selectedFeature(e)
        if self.feature is None: return
        cursorPoint = self.toLayerCoordinates(self.layer, e.pos())
        geom = self.feature.geometry()
        points = None
        if geom.wkbType() == QGis.WKBPolygon:
            points = geom.asPolygon()
        if geom.wkbType() == QGis.WKBMultiPolygon:
            points = geom.asMultiPolygon()[0]

        self.parent.OldGeometrie = points
        print "points"
        print points
        mindistance, minindex, newpoint = -1, -1, None
        if(len(points) == 0):
            return
        for index, p in enumerate(points[0]):
            if index == len(points[0]) - 1:
                break
            p0 = p
            p1 = points[0][index + 1]
            line = QgsGeometry.fromPolyline([p0, p1])
            distanceToPolygon = QgsGeometry.distance(line, QgsGeometry.fromPoint(cursorPoint))
            if mindistance > distanceToPolygon or mindistance < 0:
                mindistance = distanceToPolygon
                minindex = index + 1
                newpoint = cursorPoint
        if minindex < 0: return
        geom.insertVertex(newpoint.x(), newpoint.y(), minindex)

        self.layer.changeGeometry(self.feature.id(), geom)
        self.markers.append(self.createVertexMarkerAt(cursorPoint))
        self.parent.mk = self.markers
        geom = self.feature.geometry()
        self.parent.geometryeEdit = points
        self.parent.TheGeom = QgsGeometry.fromPolygon(points)

        self.parent.GeomId = self.feature.id()
        self.parent.geom = geom

        self.layer.triggerRepaint()
        self.mouseDown = False



    def canvasReleaseEvent(self, e):
        print "canvasReleaseEvent in"
        self.mouseDown = False
        self.layer.triggerRepaint()

    def removeVertex(self):
        print "delete current Vertex when del pressed"
        print self.vertexIndex
        if self.vertexIndex is None: return
        if self.feature is None: return
        if not self.currentGeom: return
        if not self.currentVertex : return
        x = self.currentGeom[0]
        print "array of self.currentGeom"
        print self.currentGeom
        self.canvas.scene().removeItem(self.markers[self.vertexIndex])
        print self.vertexIndex
        #self.currentGeom.remove(self.currentGeom[0][self.vertexIndex])
        self.currentGeom[0].remove(self.currentGeom[0][self.vertexIndex])
        newgeom = QgsGeometry.fromPolygon(self.currentGeom)
        geom = self.feature.geometry()
        self.layer.changeGeometry(self.feature.id(), newgeom)

        self.parent.geometryeEdit = self.currentGeom
        self.parent.TheGeom = newgeom
        self.parent.GeomId = self.feature.id()
        self.mouseDown = False

        self.canvas.refresh()
        self.layer.triggerRepaint()
        return




    def canvasMoveEvent(self, e):
        #print "canvasMoveEvent Move when drag"
        #controle
        #print self.vertexIndex
        if not self.mouseDown: return
        if self.vertexIndex is None: return
        if not self.feature: return

        point = self.toLayerCoordinates(self.layer, e.pos())
        geom = self.feature.geometry()
        x = None
        if geom.wkbType() == QGis.WKBPolygon:
            x = geom.asPolygon()
        if geom.wkbType() == QGis.WKBMultiPolygon:
            x = geom.asMultiPolygon()[0]
        self.parent.OldGeometrie = x
        print "x"
        print x
        p = (QgsPoint(point.x(), point.y()))
        if len(x) == 0:
            return

        x[0][self.vertexIndex] = p

        if self.vertexIndex == 0:
            x[0][len(x[0]) - 1] = p
        newgeom = QgsGeometry.fromPolygon(x)

        self.markers[self.vertexIndex].setCenter(p)

        self.parent.mk = self.markers
        geom = self.feature.geometry()
        self.layer.changeGeometry(self.feature.id(), newgeom)

        geom = self.feature.geometry()
        geom = self.feature.geometry()
        self.parent.geometryeEdit = x
        self.parent.GeomId = self.feature.id()
        self.parent.geom = geom
        self.parent.TheGeom = QgsGeometry.fromPolygon(x)



        self.canvas.refresh()
        self.layer.triggerRepaint()





    def deactivate(self):
        self.layer.rollBack()
        for v in self.markers:
            self.canvas.scene().removeItem(v)
        del self.markers[:]
        QgsMapTool.deactivate(self)

    def activate(self):
        self.layer.startEditing()

        renderTitre = self.layer.rendererV2()
        if self.CurrIndxLayer == 2 :
            style1 = {'color': '0,0,255,0',u'outline_width': u'0.3', u'outline_color': u'202,90,208,255'}
        else :
            style1 = {'color': '255,0,0,0', 'outline_color': '93,182,255,255', 'outline_width': '0.3'}

        #style1 = {'color': '255,0,0,0', 'outline_color': '93,182,255,255', 'outline_width': '0.3'}
        mySymbol2 = QgsFillSymbolV2.createSimple(style1)
        if renderTitre:
            renderTitre.setSymbol(mySymbol2)

        self.layer.setCustomProperty("labeling", "pal")
        self.layer.setCustomProperty("labeling/enabled", "true")
        self.layer.setCustomProperty("labeling/fontFamily", "Arial")
        self.layer.setCustomProperty("labeling/fontSize", "8")
        # layer.setCustomProperty("labeling/fontWeight", "Bold")
        # self.layer.setCustomProperty("labeling/fieldName",'numdemande')
        self.layer.setCustomProperty("labeling/placement", "OverPoint")
        self.layer.removeSelection()
        self.layer.triggerRepaint()

        QgsMapTool.activate(self)
        self.setCursor(Qt.CrossCursor)
        self.mouseDown = False
        self.markers = []
