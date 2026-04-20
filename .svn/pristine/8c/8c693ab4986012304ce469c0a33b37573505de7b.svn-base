# -*-coding:UTF-8 -*
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *


#from PyQt4 import QtCore, QtGui, uic
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
import qgis
# from qgis.gui import QgsVertexMarker
# import processing
# from DemandeurCertificat import Ui_Dialog
# from CreaDemandeRunn import CreateDemandeRunn
import  globalvars




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

# Capture Tool Class Begin ...............
class CaptureTool(QgsMapTool):
    CAPTURE_LINE = 1
    CAPTURE_POLYGON = 2
    finished = pyqtSignal(QgsPoint)
    locationChanged = pyqtSignal(QgsPoint)

    def __init__(self, canvas, layer, onGeometryAdded, captureMode, Iface, ifc,sender,parent):  # miampy param iray ahafantaran hoe avy aiz le creation parcelle (Salim)

        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        utils = self.canvas.snappingUtils()
        self.layer = layer
        self.onGeometryAdded = onGeometryAdded
        self.captureMode = captureMode
        #self.vertex = QgsVertexMarker(canvas)
        self.started = False
        self.snapper = QgsMapCanvasSnapper(self.canvas)
        self.snapIndicator = None
        self.mCtrl = False
        self.mShift = False
        self.lastPoint = None
        self.pointsProposed = False
        self.propVertCnt = 0
        self.snappedLayer = None
        self.snappedGeometry = None
        self.snappedVertexNr = None
        self.snappedPartNr = None
        self.snappedRingNr = None
        self.snappedRingVertexOffset = None
        self.snappedToPolygon = False
        self.feature = None
        self.SommetSegment = None
        self.allLayers = self.canvas.layers()



        #        self.vertex            = None
        self.rubberBand = None
        self.tempRubberBand = None
        self.capturedPoints = []
        self.capturing = False
        self.current_geom = []
        self.GeomPart = None
        self.iface = Iface
        self.parent = parent
        self.registry = self.parent.registry
        self.recordsGeomPart = None
        try :
            self.DemandeLayer = self.registry.mapLayersByName("Demandes Parcelle")[0]
            self.CFLayer = self.registry.mapLayersByName("Certificats")[0]
            self.FiscaliteLayer = self.registry.mapLayersByName("Fiscalite")[0]
        except Exception as e:
            print(e)
        self.terminatePart = self.parent.terminatePart
        self.idxMode = self.parent.idxMode
        self.registry = self.parent.registry
        self.MainWindow = self.parent.MainWindow
        self.ifc = ifc
        self.setCursor(Qt.ArrowCursor)
        self.sender = sender
        self.markersCP = []
        self.MainWindow = Iface
        self.vertexIndex = None
        self.index = 0
        self.SnappedVertex = 0
        self.closestPtOnSegment = None
        self.snapper = QgsMapCanvasSnapper(self.canvas)

    def snappoint(self, point):
        utils = self.canvas.snappingUtils()
        #utils.LayerConfig(self.layer, QgsPointLocator.Vertex and QgsPointLocator.Edge, 20, QgsTolerance.Pixels)
        match = utils.snapToMap(point)

        if match.isValid():
            mapPt = match.point()
            layerPt = match.point()
            tmpMapPt = match.point()
            m = QgsVertexMarker(self.canvas)
            m.setColor(QColor(0, 255, 0))
            m.setIconSize(5)
            m.setIconType(QgsVertexMarker.ICON_BOX)  # or ICON_CROSS, ICON_X
            m.setPenWidth(3)
            self.parent.markers.append(m)
            self.markersCP.append(m)
            m.setCenter(tmpMapPt)
            self.rubberBand.addPoint(tmpMapPt)
            self.capturedPoints.append(tmpMapPt)
            self.tempRubberBand.reset(self.bandType())

            if self.captureMode == CaptureTool.CAPTURE_LINE:
                self.tempRubberBand.addPoint(tmpMapPt)


            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:

                firstPoint = self.rubberBand.getPoint(0, 0)
                self.tempRubberBand.addPoint(firstPoint)
                self.tempRubberBand.movePoint(tmpMapPt)
                self.tempRubberBand.addPoint(tmpMapPt)

            # self.ifc.mapCanvas().refresh()
            self.canvas.refresh()
            for layer in self.canvas.layers():
                layer.triggerRepaint()

            #return match.point()
        else:
            utils.LayerConfig(self.layer, QgsPointLocator.Vertex and QgsPointLocator.Edge, 20, QgsTolerance.Pixels)
            edge = utils.snapToCurrentLayer(point, QgsPointLocator.Edge)
            if edge.isValid():
                print "Voisin"
                print edge
                mapPt = edge.point()
                self.tempRubberBand.movePoint(mapPt)
                mapPt = edge.point()
                layerPt = edge.point()
                tmpMapPt = edge.point()
                m = QgsVertexMarker(self.canvas)
                m.setColor(QColor(0, 255, 0))
                m.setIconSize(5)
                m.setIconType(QgsVertexMarker.ICON_BOX)  # or ICON_CROSS, ICON_X
                m.setPenWidth(3)
                self.parent.markers.append(m)
                self.markersCP.append(m)
                m.setCenter(tmpMapPt)
                self.rubberBand.addPoint(tmpMapPt)
                self.capturedPoints.append(tmpMapPt)
                self.tempRubberBand.reset(self.bandType())

                if self.captureMode == CaptureTool.CAPTURE_LINE:
                    self.tempRubberBand.addPoint(tmpMapPt)


                elif self.captureMode == CaptureTool.CAPTURE_POLYGON:

                    firstPoint = self.rubberBand.getPoint(0, 0)
                    self.tempRubberBand.addPoint(firstPoint)
                    self.tempRubberBand.movePoint(tmpMapPt)
                    self.tempRubberBand.addPoint(tmpMapPt)

                # self.ifc.mapCanvas().refresh()
                self.canvas.refresh()
                for layer in self.canvas.layers():
                    layer.triggerRepaint()
            else :
                print " indentation test"
                mapPt, layerPt = self.transformCoordinates(point)
                m = QgsVertexMarker(self.canvas)
                m.setCenter(mapPt)
                m.setColor(QColor(255, 40, 0))
                m.setIconSize(5)
                m.setIconType(QgsVertexMarker.ICON_BOX)  # or ICON_CROSS, ICON_X
                m.setPenWidth(3)
                self.parent.markers.append(m)
                self.markersCP.append(m)

                self.rubberBand.addPoint(mapPt)
                self.capturedPoints.append(layerPt)
                self.tempRubberBand.reset(self.bandType())

                if self.captureMode == CaptureTool.CAPTURE_LINE:
                    self.tempRubberBand.addPoint(mapPt)

                elif self.captureMode == CaptureTool.CAPTURE_POLYGON:

                    firstPoint = self.rubberBand.getPoint(0, 0)
                    self.tempRubberBand.addPoint(firstPoint)
                    self.tempRubberBand.movePoint(mapPt)
                    self.tempRubberBand.addPoint(mapPt)

                # self.ifc.mapCanvas().refresh()
                self.canvas.refresh()
                for layer in self.canvas.layers():
                    layer.triggerRepaint()
            #return self.canvas.getCoordinateTransform().toMapCoordinates(point)

    def calcTolerance(self, pos):
        pt1 = QPoint(pos.x(), pos.y())
        import  globalvars
        try :
            t = int(globalvars.Tolerance)
            if t >= 1 :
                print "do not nothing"
            else:
                t = 10 #default value
            pt2 = QPoint(pos.x() + t, pos.y())
            mapPt1, layerPt1 = self.transformCoordinates(pt1)
            mapPt2, layerPt2 = self.transformCoordinates(pt2)
            tolerance = layerPt2.x() - layerPt1.x()
            return tolerance
        except Exception as e:
            print(e)


    def findFeatureAtOld(self, pos):

        #print "at findFeatureAt"
        mapPt, layerPt = self.transformCoordinates(pos)
        #tolerance = self.calcTolerance(pos)
        tolerance = self.canvas.mapUnitsPerPixel() * 10
        searchRect = QgsRectangle(layerPt.x() - tolerance, layerPt.y() - tolerance, layerPt.x() + tolerance,
                                  layerPt.y() + tolerance)
        request = QgsFeatureRequest()
        request.setFilterRect(searchRect)
        request.setFlags(QgsFeatureRequest.ExactIntersect)
        for feature in self.layer.getFeatures(request):
            ft = feature
            return feature
        return None

    def MoveCursorToClickPos(self,pos):
        print "MoveCursorToClickPos"

    def reloadCanvas(self):

        print " reload canvas "
        canvas = self.canvas
        for layer in canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()

        canvas.refresh()

    def canvasReleaseEvent(self, event):
        print " canvasReleaseEvent "
        menu = QMenu()
        valider = menu.addAction(QIcon("icone/accept.png"), _fromUtf8("Terminer la construction "))
        # valider = menu.addAction(QIcon("icone/Terminate.png"), _fromUtf8("Terminer la construction "))
        valider.setShortcut(QtGui.QKeySequence("F2"))

        if event.button() == Qt.LeftButton:

            if not self.capturing:
                self.startCapturing()
            self.setCursor(Qt.ArrowCursor)
            mapPt, layerPt = self.transformCoordinates(event.pos())

            self.addVertex(event.pos())

            self.index = self.index + 1
            self.vertexIndex = self.index

        elif event.button() == Qt.RightButton:
            #parcelle = menu.addAction(QIcon("icone/accept.png"),_fromUtf8("Terminer la parcelle seulement"))

            partieValidate = menu.addAction(QIcon("icone/layer-shape-polygon.png"), _fromUtf8("Terminer la partie"))
            annuler = menu.addAction(QIcon("icone/layer_del.png"),_fromUtf8("Annuler le traçage"))
            delSommet = menu.addAction(QIcon("icone/marker--minus.png"),_fromUtf8("Supprimer le sommet "))
            delSommet.setShortcut(QtGui.QKeySequence("Del"))
            annuler.setShortcut(QtGui.QKeySequence("Del"))
            #deplacer = menu.addAction(_fromUtf8("Déplacer ..."))
            #deplacerVers = menu.addAction(_fromUtf8("Déplacer vers ..."))
            #propriete = menu.addAction(_fromUtf8("Prorpiétés"))
            action = menu.exec_(self.canvas.mapToGlobal(QPoint(event.pos().x() + 5, event.pos().y())))
            #action01 = menu.exec_(self.canvas.mapToGlobal(event.pos()))

            if action == partieValidate :
                print("---------partieValidate---------------")
                try:
                    points = self.getCapturedGeometry()
                    stop = self.stopCapturing1()
                    self.layer.triggerRepaint()
                    self.parent.terminatePart = 1
                    self.parent.ParcelleCreux = True
                    print "self.terminatePart PART TERMINATE"
                    print self.terminatePart
                    self.layer.triggerRepaint()
                    print("---points----")
                    print(points)
                    if points != None:
                        self.geometryCapturedPart(points)
                        #    return
                except Exception as e:
                    print(e)

            if action == valider:
                self.parent.terminatePart = 0
                self.parent.parcelleSeulement = 0
                self.parent.ParcelleCreux = False
                points = self.getCapturedGeometry()
                stop = self.stopCapturing()
                self.layer.triggerRepaint()

                if points != None:
                    self.geometryCaptured(points)
                    if self.rubberBand:
                        self.rubberBand.hide()
                        self.canvas.scene().removeItem(self.rubberBand)
                        self.rubberBand = None

                    if self.tempRubberBand:
                        self.canvas.scene().removeItem(self.tempRubberBand)
                        self.canvas.scene().removeItem(self.vertex)
                        self.tempRubberBand = None

                    for v in self.markersCP:
                        self.canvas.scene().removeItem(v)

                    del self.parent.markers[:]
                    del self.markersCP[:]
                    self.capturing = False
                    # self.canvas.scene().removeItem(self.vertex)
                    self.removeLastVertex()
                    self.layer.triggerRepaint()
                    self.canvas.unsetMapTool(self)
            if action == delSommet :
                self.removeLastVertex()
                self.parent.ParcelleCreux = False
                #del self.parent.markers[:]
                #del self.markersCP[:]

                self.canvas.scene().removeItem(self.markersCP[self.vertexIndex])
                self.layer.triggerRepaint()
                self.canvas.refresh()
                self.canvas.refresh()
                self.canvas.refresh()
                self.canvas.refresh()
                self.canvas.refresh()
                for layer in self.canvas.layers():
                    if layer.type() == layer.VectorLayer:
                        layer.removeSelection()

                self.canvas.refresh()
                self.reloadCanvas()
                self.canvas.unsetMapTool(self)

            if action == annuler:
                self.parent.parcelleSeulement = 1
                self.parent.ParcelleCreux = False
                self.stopCapturing()
                if self.rubberBand:
                    self.rubberBand.hide()
                    self.canvas.scene().removeItem(self.rubberBand)
                    self.rubberBand = None

                if self.tempRubberBand:
                    self.canvas.scene().removeItem(self.tempRubberBand)
                    self.canvas.scene().removeItem(self.vertex)
                    self.tempRubberBand = None

                for v in self.markersCP:
                    self.canvas.scene().removeItem(v)

                for v in self.capturedPoints:
                    self.canvas.scene().removeItem(v)

                del self.parent.markers[:]
                del self.markersCP[:]
                del self.capturedPoints[:]
                self.capturing = False
                #self.canvas.scene().removeItem(self.vertex)
                self.removeLastVertex()
                self.layer.triggerRepaint()
                self.canvas.unsetMapTool(self)


    def snappointMovePoint(self, point):
        utils = self.canvas.snappingUtils()
        match = utils.snapToMap(point)
        print("----Type--Point---")
        print(point)

        if match.isValid():
            mapPt = match.point()
            self.tempRubberBand.movePoint(mapPt)
        else:
            utils.LayerConfig(self.layer, QgsPointLocator.Vertex and QgsPointLocator.Edge, 20, QgsTolerance.Pixels)
            edge = utils.snapToCurrentLayer(point,QgsPointLocator.Edge)
            pointLocator = utils.locatorForLayer(self.layer)
            print 'pointLocator'
            print pointLocator
            if edge.isValid():
                print "Voisin"
                print edge
                mapPt = edge.point()
                self.tempRubberBand.movePoint(mapPt)
            else :
                mapPt, layerPt = self.transformCoordinates(point)
                print("---mapPt---")
                print(mapPt)

                print("---layerPt---")
                print(layerPt)
                self.tempRubberBand.movePoint(mapPt)
            # mapPt = self.snappoint(event.pos())
            #self.finished.emit(mapPt)


    def canvasMoveEvent(self, event):
        #self.canvas.setCenter(self.transformCoordinates(event.pos()))
        #self.canvas.refresh()
        if self.tempRubberBand != None and self.capturing:
            print "canvasMoveEvent"
            pos = event.pos()
            print("------pos.X-------")
            print(event.x())
            print("------pos.Y-------")
            print(event.y())

            self.snappointMovePoint(event.pos())

    def keyPressEvent(self, event):
        print " keyPressEvent "

        if event.key() == Qt.Key_Escape :
            self.parent.parcelleSeulement = 1
            self.stopCapturing()
            if self.rubberBand:
                self.rubberBand.hide()
                self.canvas.scene().removeItem(self.rubberBand)
                self.rubberBand = None

            if self.tempRubberBand:
                self.canvas.scene().removeItem(self.tempRubberBand)
                self.canvas.scene().removeItem(self.vertex)
                self.tempRubberBand = None

            for v in self.markersCP:
                self.canvas.scene().removeItem(v)

            del self.parent.markers[:]
            del self.markersCP[:]
            self.capturing = False
            # self.canvas.scene().removeItem(self.vertex)
            self.removeLastVertex()
            self.layer.triggerRepaint()
            self.canvas.unsetMapTool(self)


        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.removeLastVertex()
            event.ignore()
        # if event.key() == Qt.Key_Control:
        #     self.keyControlPressed = True
        #     if event.key() == Qt.Key_Z :
        #         print("-------Ctrl+Z--------")

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter or  event.key() == Qt.Key_F2:
            points = self.getCapturedGeometry()
            stop = self.stopCapturing()
            if points != None:
                self.geometryCaptured(points)

    def startCapturing(self):
        color = QColor("red")
        color.setAlphaF(0.6)
        self.rubberBand = QgsRubberBand(self.canvas)
        self.rubberBand.setWidth(1.5)
        self.rubberBand.setColor(color)
        self.rubberBand.show()
        self.tempRubberBand = QgsRubberBand(self.canvas)
        self.tempRubberBand.setWidth(1)
        color = QColor("white")
        color.setAlphaF(0.3)
        self.tempRubberBand.setColor(color)
        self.tempRubberBand.setLineStyle(Qt.SolidLine)
       #self.tempRubberBand.setLineStyle
        self.tempRubberBand.show()
        self.capturing = True

    def bandType(self):

        if self.captureMode == CaptureTool.CAPTURE_POLYGON:
            return QGis.Polygon
        else:
            return QGis.Line
    def stopCapturing(self):
        if self.rubberBand:
            print 'test rubberband none'
            #self.canvas.scene().removeItem(self.rubberBand)
            #self.rubberBand = None

        if self.tempRubberBand:
            #´print 'test Temprubberband none'
            self.canvas.scene().removeItem(self.tempRubberBand)
            #self.canvas.scene().removeItem(self.vertex)
            self.tempRubberBand = None

        self.capturing = False
        #self.canvas.scene().removeItem(self.vertex)
        self.capturedPoints = []
        self.canvas.refresh()
        self.canvas.refresh()
        self.canvas.refresh()
        self.canvas.refresh()
        self.canvas.refresh()
        self.canvas.unsetMapTool(self)

    def stopCapturing1(self):
        if self.rubberBand:
            print 'test rubberband none'
            #self.canvas.scene().removeItem(self.rubberBand)
            #self.rubberBand = None

        if self.tempRubberBand:
            #´print 'test Temprubberband none'
            self.canvas.scene().removeItem(self.tempRubberBand)
            #self.canvas.scene().removeItem(self.vertex)
            self.tempRubberBand = None

        self.capturing = False
        #self.canvas.scene().removeItem(self.vertex)
        self.capturedPoints = []
        self.canvas.refresh()
        self.canvas.refresh()
        self.canvas.refresh()
        self.canvas.refresh()
        self.canvas.refresh()
        #self.canvas.unsetMapTool(self)
        #print "out stop capturing "

    def removeLastVertex(self):
        #print "test"
        if not self.capturing: return
        bandSize = self.rubberBand.numberOfVertices()
        tempBandSize = self.tempRubberBand.numberOfVertices()
        numPoints = len(self.capturedPoints)
        if bandSize < 1 or numPoints < 1:
            return
        self.rubberBand.removePoint(-1)

        if bandSize > 1:

            if tempBandSize > 1:
                point = self.rubberBand.getPoint(0, bandSize - 2)
                self.tempRubberBand.movePoint(tempBandSize - 2, point)
        else:
            self.tempRubberBand.reset(self.bandType())

        del self.capturedPoints[-1]
        del self.markersCP[-1]

    def getCapturedGeometry(self):
        points = self.capturedPoints
        #print "at getCapturedGeometry"
        #        prin
        if self.captureMode == CaptureTool.CAPTURE_LINE:
            if len(points) < 2:
                return None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                if len(points) < 3:
                    return None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                #print points[0]
                points.append(points[0])  # Close polygon.

        return points

    def transformCoordinates(self, canvasPt):
        return (self.toMapCoordinates(canvasPt), self.toLayerCoordinates(self.layer, canvasPt))


    def geometryCapturedPart(self, layerCoords):
        if self.captureMode == CaptureTool.CAPTURE_LINE:

            geometry = QgsGeometry.fromPolyline(layerCoords)

        elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
            #                print [layerCoords]
            geometry = QgsGeometry.fromPolygon([layerCoords])
        self.GeomPart = geometry
        self.recordsGeomPart = layerCoords
        #print "geometryCaptured"
        QgsMapLayerRegistry.instance().addMapLayers([self.layer])

        print("----layerCoords geometryCapturedPart-------")
        print(geometry)
        self.parent.geomPart = layerCoords


    def geometryCaptured(self, layerCoords):
        if self.captureMode == CaptureTool.CAPTURE_LINE:

            geometry = QgsGeometry.fromPolyline(layerCoords)

        elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
            print("----layerCoords- ON GEOMETRY ADD---")
            print [layerCoords]
            geometry = QgsGeometry.fromPolygon([layerCoords])
        self.current_geom = geometry
        QgsMapLayerRegistry.instance().addMapLayers([self.layer])
        reply = QMessageBox.question(self.MainWindow, "Confirm", "Voulez-vous enregistrer la parcelle trace?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            geometryPart = None
            try :
                print('-------recorde geometry partie-------')
                if(self.recordsGeomPart is not None):
                    geometryPart = QgsGeometry.fromPolygon([self.recordsGeomPart])
                else :
                    print(" pas de geometrie vide ")
                if(geometryPart is not  None):
                    geomFinal = geometry.difference(geometryPart)
                else :
                    geomFinal = geometry
                #print(self.GeomPart)
                #geomFinal = geometry.difference(geometryPart)
                self.onGeometryAdded(geomFinal, layerCoords, self.sender)
            except Exception as e:
                print(e)
              # renvoyer le sender vers la fonction onGeometryAdded (Salim)
        self.balayerCanvas()




    def balayerCanvas(self):

        if self.rubberBand:
            self.rubberBand.hide()
            self.canvas.scene().removeItem(self.rubberBand)
            self.rubberBand = None

        if self.tempRubberBand:
            self.canvas.scene().removeItem(self.tempRubberBand)
            self.canvas.scene().removeItem(self.vertex)
            self.tempRubberBand = None

        for v in self.markersCP:
            self.canvas.scene().removeItem(v)

        del self.parent.markers[:]
        del self.markersCP[:]
        self.capturing = False
        #self.canvas.scene().removeItem(self.vertex)
        self.removeLastVertex()
        self.layer.triggerRepaint()
        #self.canvas.unsetMapTool(self)

    def createScreenshot4(self, layer):
        global ids
        ids = layer.allFeatureIds()

        def exportMap():
            global ids
            self.ifc.mapCanvas().saveAsImage("D:\\imageCF.png".format(ids.pop()))
            if ids:
                setNextFeatureExtent()
            else:
                self.ifc.mapCanvas().mapCanvasRefreshed.disconnect(exportMap)

        def setNextFeatureExtent():
            reqq = QgsFeatureRequest()
            reqq.setFilterFid(ids[-1])

            for feature in layer.getFeatures(reqq):
                point = feature.geometry().asPoint()
                self.ifc.mapCanvas().setCenter(point)
                self.ifc.mapCanvas().refresh()

        self.ifc.mapCanvas().mapCanvasRefreshed.connect(exportMap)
        setNextFeatureExtent()  # Let's start

    def getNearestPoint(self,ArrayPoints):
        print "aaaaa"

    def findVertexAt(self, feature, pos):
        import math
        newpoint = None
        m = None
        vertex = None
        mapPt, layerPt = self.transformCoordinates(pos)
        tolerance = self.calcTolerance(pos)
        mode = int(globalvars.Mode)
        print "MODE---"
        print mode

        #if (mode == 1) or (mode == 3):
        vertexCoord, vertex, prevVertex, nextVertex, distSquared = feature.geometry().closestVertex(layerPt)

        distance = math.sqrt(distSquared)
        if distance > tolerance:
            vrt = None
            geom = feature.geometry()
            distSquared, closestPt, beforeVertex = geom.closestSegmentWithContext(layerPt)
            d = math.sqrt(distSquared)
            if d > tolerance:
                return None
            else :
                if (mode == 3) or (mode == 2 ):

                    mapPt = self.toMapCoordinates(self.layer, closestPt)
                    self.closestPtOnSegment = closestPt
                    self.SnappedVertex = 1
        else:
            return vertex
        print "VERTEX ---------"
        print vertex

    def createVertexMarkerAt(self, p):
        marker = QgsVertexMarker(self.canvas)
        marker.setColor(QColor(147, 255,124))
        marker.setIconSize(5)
        marker.setIconType(QgsVertexMarker.ICON_BOX)
        marker.setPenWidth(3)
        marker.hide()
        marker.show()
        marker.setCenter(p)
        self.canvas.refresh()
        return marker

    def findFeatureAt(self, pos, excludeFeature=None):
        mapPt, layerPt = self.transformCoordinates(pos)
        tolerance = self.calcTolerance(pos)
        searchRect = QgsRectangle(layerPt.x() - tolerance, layerPt.y() - tolerance, layerPt.x() + tolerance,
                                  layerPt.y() + tolerance)
        request = QgsFeatureRequest()
        request.setFilterRect(searchRect)

        request.setFlags(QgsFeatureRequest.ExactIntersect)

        if globalvars.CurrentLayer == 0:
            for layer in self.allLayers:
                if layer.type() == layer.VectorLayer:
                    if layer is not None:
                        for feature in layer.getFeatures(request):
                            if excludeFeature != None:
                               if feature.id() == excludeFeature.id():
                                    continue
                            return feature
            return None

        if globalvars.CurrentLayer == 1:

            if self.DemandeLayer is not None:
                for feature in self.DemandeLayer.getFeatures(request):
                    if excludeFeature != None:
                        if feature.id() == excludeFeature.id():
                            continue
                    return feature
            return None

        if globalvars.CurrentLayer == 2:

            if self.CFLayer is not None:
                for feature in self.CFLayer.getFeatures(request):
                    if excludeFeature != None:
                        if feature.id() == excludeFeature.id():
                            continue
                    return feature
            return None

        if globalvars.CurrentLayer == 3:

            if self.FiscaliteLayer is not None:
                for feature in self.FiscaliteLayer.getFeatures(request):
                    if excludeFeature != None:
                        if feature.id() == excludeFeature.id():
                            continue
                    return feature
            return None



    def deleteVertexFrom(self,feature, vertex):
        geometry = feature.geometry()
        lineString = geometry.asPolyline()
        if len(lineString) <= 2:
            return
        if geometry.deleteVertex(vertex):
            self.layer.changeGeometry(feature.id(), geometry)
            #self.layer.changeGeometry(feature.id(), geometry)
            self.canvas.refresh()

    def selectedFeature(self, e):
        self.feature = None
        point = self.toLayerCoordinates(self.layer, e.pos())
        d = self.canvas.mapUnitsPerPixel() * 4
        for feat in self.layer.getFeatures():
            if feat.geometry().intersects(QgsRectangle((point.x() - d), (point.y() - d), (point.x() + d), (point.y() + d))):
                self.feature = feat
                return

    def snapToNearestVertex(self,pos, trackLayer, excludeFeature=None) :
        SnapVertexSegment = []
        mapPt, layerPt = self.transformCoordinates(pos)
        feature = self.findFeatureAt(pos, excludeFeature)

        if feature == None:
            self.SnappedVertex = 0
            return layerPt
        else :
            self.SnappedVertex = 1

        vertex = self.findVertexAt(feature, pos)

        if vertex == None:
            self.SnappedVertex = 0
            return layerPt
        else :
            self.SnappedVertex = 1

        print "VERTEX nature"
        print vertex

        #SnapVertexSegment.append(feature.geometry().vertexAt(vertex))
        #SnapVertexSegment.append(self.closestPtOnSegment)

        return feature.geometry().vertexAt(vertex)



    def addVertex(self, canvasPoint):

        #MODE off
        if int(globalvars.Mode) == 0:
            mapPt, layerPt = self.transformCoordinates(canvasPoint)
            m = QgsVertexMarker(self.canvas)
            m.setCenter(mapPt)
            m.setColor(QColor((119, 181, 254)))
            m.setIconSize(5)
            m.setIconType(QgsVertexMarker.ICON_BOX)
            m.setPenWidth(3)

            self.parent.markers.append(m)
            self.markersCP.append(m)

            # self.markers.append(m)

            #            inserer point to rubberBand
            self.rubberBand.addPoint(mapPt)
            self.capturedPoints.append(layerPt)
            self.tempRubberBand.reset(self.bandType())

            if self.captureMode == CaptureTool.CAPTURE_LINE:
                self.tempRubberBand.addPoint(mapPt)

            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:

                firstPoint = self.rubberBand.getPoint(0, 0)
                self.tempRubberBand.addPoint(firstPoint)
                self.tempRubberBand.movePoint(mapPt)
                self.tempRubberBand.addPoint(mapPt)
        else :
         #MODE - sommet / segment / sommet-segment
            snapPt = self.snapToNearestVertex(canvasPoint, self.layer)
            if self.closestPtOnSegment is None:
                mapPt = self.toMapCoordinates(self.layer, snapPt)
            else:
                print "self.SnappedVertex on closestSegment"
                print self.SnappedVertex
                self.SnappedVertex = 1
                mapPt = self.toMapCoordinates(self.layer, self.closestPtOnSegment)
                snapPt = self.closestPtOnSegment
            m = QgsVertexMarker(self.canvas)
            m.setCenter(mapPt)

            if self.SnappedVertex == 0:
                # m.setColor(QColor(0, 255, 0))
                if self.parent.terminatePart == 1:
                    m.setColor(QColor(0, 40, 255))
                else:
                    # m.setColor(QColor(255, 40, 0))
                    # m.setColor(QColor(147, 124, 255))
                    m.setColor(QColor((119, 181, 254)))
                    m.setIconSize(5)
                    m.setIconType(QgsVertexMarker.ICON_BOX)
                    m.setPenWidth(3)
            if self.SnappedVertex == 1:
                m.setColor(QColor(0, 255, 0))

            m.setIconSize(5)
            m.setIconType(QgsVertexMarker.ICON_BOX)  # or ICON_CROSS, ICON_X
            m.setPenWidth(3)
            self.parent.markers.append(m)
            self.markersCP.append(m)

            self.rubberBand.addPoint(mapPt)
            self.capturedPoints.append(snapPt)
            self.tempRubberBand.reset(self.bandType())

            if self.captureMode == CaptureTool.CAPTURE_LINE:
                self.tempRubberBand.addPoint(mapPt)

            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:

                firstPoint = self.rubberBand.getPoint(0, 0)
                self.tempRubberBand.addPoint(firstPoint)
                self.tempRubberBand.movePoint(snapPt)
                self.tempRubberBand.addPoint(mapPt)


        self.canvas.refresh()
        for layer in self.canvas.layers():
            layer.triggerRepaint()
        self.closestPtOnSegment = None

