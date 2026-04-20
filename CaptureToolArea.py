# -*-coding:UTF-8 -*
import os, os.path, sys
from qgis.core import *
from qgis.gui import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from AreaConvert import AreaConvert


#from PyQt4 import QtCore, QtGui, uic
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
import qgis
# from qgis.gui import QgsVertexMarker
# import processing
# from DemandeurCertificat import Ui_Dialog
# from CreaDemandeRunn import CreateDemandeRunn




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

    def __init__(self, canvas, layer, onGeometryAdded, captureMode, Iface, ifc,parent):  # miampy param iray ahafantaran hoe avy aiz le creation parcelle (Salim)

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

        #        self.vertex            = None
        self.rubberBand = None
        self.tempRubberBand = None
        self.capturedPoints = []
        self.capturing = False
        self.current_geom = []
        self.iface = Iface
        self.parent = parent
        self.terminatePart = self.parent.terminatePart
        self.registry = self.parent.registry
        self.MainWindow = self.parent.MainWindow
        self.ifc = ifc
        self.setCursor(Qt.CrossCursor)
        #self.evArea = self.parent.evArea
        self.markersCP = []
        self.MainWindow = Iface
        self.vertexIndex = None
        self.index = 0
        self.snapper = QgsMapCanvasSnapper(self.canvas)
        from EvaluateAreaRun import EvaluateAreaRun
        self.evArea = EvaluateAreaRun()
        self.ConvertirArea = AreaConvert()


    def snappoint(self, point):
        utils = self.canvas.snappingUtils()
        match = utils.snapToMap(point)

        if match.isValid():
            #print " snappoint IN OUT"
            #print match.point()
            #print " snappoint OUT IN"
            #mapPt, layerPt,tmpMapPt = match.point()
            mapPt = match.point()
            layerPt = match.point()
            tmpMapPt = match.point()
            #layerPt = self.snappoint(canvasPoint)
            #self.finished.emit(layerPt)

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

            mapPt, layerPt = self.transformCoordinates(point)

            #layerPt = self.snappoint(canvasPoint)
            #self.finished.emit(layerPt)
            #print "mapPt.x"
            #print mapPt.x()
            #print "layerPt.x"
            #print layerPt.x()



            m = QgsVertexMarker(self.canvas)
            m.setCenter(mapPt)
            m.setColor(QColor(0, 40, 255))
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
        pt2 = QPoint(pos.x() + 10, pos.y())
        mapPt1, layerPt1 = self.transformCoordinates(pt1)
        mapPt2, layerPt2 = self.transformCoordinates(pt2)
        tolerance = layerPt2.x() - layerPt1.x()
        return tolerance

    def findFeatureAt(self, pos):

        #print "at findFeatureAt"
        mapPt, layerPt = self.transformCoordinates(pos)
        #tolerance = self.calcTolerance(pos)
        tolerance = self.canvas.mapUnitsPerPixel() * 10
        searchRect = QgsRectangle(layerPt.x() - tolerance, layerPt.y() - tolerance, layerPt.x() + tolerance,
                                  layerPt.y() + tolerance)
        request = QgsFeatureRequest()
        request.setFilterRect(searchRect)
        request.setFlags(QgsFeatureRequest.ExactIntersect)

        #fiscalite = self.registry.mapLayersByName("Fiscalite")[0]
        for feature in self.layer.getFeatures(request):
            ft = feature
            return feature
        #for feature in fiscalite.getFeatures(request):
        #    ft = feature
        #    return feature
        return None

    def MoveCursorToClickPos(self,pos):
        print "MoveCursorToClickPos"

    def reloadCanvas(self):
        canvas = self.canvas
        for layer in canvas.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
                layer.triggerRepaint()

        canvas.refresh()

    def canvasReleaseEvent(self, event):
        print " canvasReleaseEvent "
        #self.evArea.exec_()
        self.evArea.show()

        #self.evArea.ui.Surface.setText("canvasReleaseEvent")
        if event.button() == Qt.LeftButton:
            if not self.capturing:
                self.startCapturing()
            self.setCursor(Qt.CrossCursor)

            #snapper test
            #point = self.snappoint(event.pos())
            #self.finished.emit(point)

            #end test snapped point
            mapPt, layerPt = self.transformCoordinates(event.pos())
            self.addVertex(event.pos())
            self.index = self.index + 1
            self.vertexIndex = self.index

            points = self.getCapturedGeometry()
            #stop = self.stopCapturing()
            if points != None:
                self.geometryCaptured(points)


        elif event.button() == Qt.RightButton:

            points = self.getCapturedGeometry()
            stop = self.stopCapturing()
            if points != None:
                self.geometryCaptured(points)




    def snappointMovePoint(self, point):
        utils = self.canvas.snappingUtils()
        match = utils.snapToMap(point)
        if match.isValid():
            mapPt = match.point()
            self.tempRubberBand.movePoint(mapPt)
        else:
            mapPt, layerPt = self.transformCoordinates(point)
            # mapPt = self.snappoint(event.pos())
            #self.finished.emit(mapPt)
            self.tempRubberBand.movePoint(mapPt)



    def canvasMoveEvent(self, event):

        if self.tempRubberBand != None and self.capturing:
            #print "canvasMoveEvent"
            #snapper test
            #point = self.snappoint(event.pos())
            #self.finished.emit(point)
            #self.locationChanged.emit(point)
            self.snappointMovePoint(event.pos())
            #mapPt, layerPt = self.transformCoordinates(event.pos())
            #feature = self.findFeatureAt(event.pos())
            #mapPt = self.snappoint(event.pos())
            #self.finished.emit(mapPt)
            #self.tempRubberBand.movePoint(mapPt)

    def keyPressEvent(self, event):
        print " keyPressEvent "
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.removeLastVertex()
            event.ignore()

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            points = self.getCapturedGeometry()
            stop = self.stopCapturing()
            if points != None:
                self.geometryCaptured(points)

    def startCapturing(self):
        color = QColor("green")
        color.setAlphaF(0.08)
        self.rubberBand = QgsRubberBand(self.canvas, self.bandType())
        self.rubberBand.setWidth(2)
        self.rubberBand.setColor(color)
        self.rubberBand.show()
        self.tempRubberBand = QgsRubberBand(self.canvas, self.bandType())
        self.tempRubberBand.setWidth(1)
        color = QColor("white")
        color.setAlphaF(0.1)
        self.tempRubberBand.setColor(color)
        self.tempRubberBand.setLineStyle(Qt.DotLine)
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
        self.balayerCanvas()
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

    def geometryCaptured(self, layerCoords):
        if self.captureMode == CaptureTool.CAPTURE_LINE:

            geometry = QgsGeometry.fromPolyline(layerCoords)

        elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
            #                print [layerCoords]
            geometry = QgsGeometry.fromPolygon([layerCoords])
            if geometry is not None :
                area = geometry.area()
                #da = QgsDistanceArea()
                #res = da.measureArea(geometry)
                self.evArea.ui.Surface.setText(str(area))
                Area = self.ConvertirArea.convertArea(float(area), 'sqmeter', 'Ha')
                self.evArea.ui.HaEdit.setText(str(Area['Ha']))
                self.evArea.ui.CaEdit.setText(str(Area['Ca']))
                self.evArea.ui.AEdit.setText(str(Area['a']))



        #            feature = QgsFeature()
        #            feature.setGeometry(geometry)
        #            self.layer.addFeature(feature,True)
        #            self.layer.updateExtents()
        #            self.layer.commitChanges()
        self.current_geom = geometry
        #print "geometryCaptured"
        QgsMapLayerRegistry.instance().addMapLayers([self.layer])
        #            global ids
        #            ids = self.layer.allFeatureIds()
        #            print " ---------ids-------------"
        #            print(ids)
        #            print "------end ids------------"
        #            param = self.layer
        #            self.createScreenshot4(self.layer)
        #            self.ifc.mapCanvas().saveAsImage("D:\\test.png")

        #            QgsMapCanvas.saveAsImage("D:\\test.png",None,"PNG")



        #reply = QMessageBox.question(self.MainWindow, "Confirm", "Voulez-vous enregistrer la parcelle trace?",
        #                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        #if reply == QMessageBox.Yes:
        #    print "ok"
            #self.onGeometryAdded(geometry, layerCoords,self.sender)  # renvoyer le sender vers la fonction onGeometryAdded (Salim)

        #self.balayerCanvas()




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
        self.canvas.unsetMapTool(self)

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
            #                QgsMapCanvas.saveAsImage
            #                QgsMapCanvas().refreshAllLayers()
            #                self.ifc.mapCanvas().refreshAllLayers()



            #                self.ifc.mapCanvas().refreshAllLayers()

        self.ifc.mapCanvas().mapCanvasRefreshed.connect(exportMap)
        setNextFeatureExtent()  # Let's start

    def getNearestPoint(self,ArrayPoints):
        print "aaaaa"


    def addVertex(self, canvasPoint):

        mapPt, layerPt = self.transformCoordinates(canvasPoint)
        #layerPt = self.snappoint(canvasPoint)
        #self.finished.emit(layerPt)
        m = QgsVertexMarker(self.canvas)
        SnapPoint = self.snappoint(canvasPoint)
        feature = self.findFeatureAt(canvasPoint)
        #print "feature findFeatureAt Found !!!"
        #print feature
