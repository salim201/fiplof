from PyQt4.QtCore import Qt
from PyQt4 import QtGui
from PyQt4.QtCore import QPoint
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsVertexMarker
from qgis.core import QGis, QgsPoint, QgsGeometry


class PointMapTool(QgsMapToolEmitPoint):
    def __init__(self, iface, points,  vertices):
        self.layer = None
        self.iface = iface
        self.canvas = iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.start_point, self.sp, self.end_point = None, None, None
        self.dragging = False
        self.rubberband = QgsRubberBand(self.canvas, QGis.Line)
        self.rubberband.setColor(QtGui.QColor('#FF4081'))
        self.rubberband.setWidth(1)
        self.points, self.vertices = points, vertices
        self.p0, self.p1, self.first_click = None, None, False
        self.m0, self.m1 = None, None

    def setLayer(self, layer):
        self.layer = layer

    def canvasPressEvent(self, e):
        c = self.toMapCoordinates(e.pos())
        corners = self.layer.cornerCoordinates()
        x, y = corners[0].x(), corners[0].y()
        xp, yp = c[0] - x, c[1] - y
        tp = (xp / self.layer.xScale, yp / self.layer.yScale)

        p = self.toMapCoordinates(e.pos())
        m = QgsVertexMarker(self.canvas)
        m.setCenter(p)
        m.setIconType(QgsVertexMarker.ICON_CROSS)
        m.setIconSize(7)
        m.setColor(QtGui.QColor('#FF5722'))
        m.setPenWidth(2)

        self.first_click = not self.first_click
        if self.first_click:
            self.p0 = self.toMapCoordinates(e.pos())
            self.m0 = m
            self.sp = tp
            self.p1 = None
            self.m1 = None
        else:
            self.p1 = self.toMapCoordinates(e.pos())
            self.m1 = m

    def canvasReleaseEvent(self, e):
        self.rubberband.reset(QGis.Line)
        if not self.first_click:
            self.points.append({'src': self.sp, 'dst': self.p1})
            self.vertices.append({'src': self.m0, 'dst': self.m1})
            # self.preview()

    def canvasMoveEvent(self, e):
        if not self.first_click:
            return
        self.rubberband.reset(QGis.Line)
        self.rubberband.addPoint(self.p0)
        self.rubberband.addPoint(self.toMapCoordinates(e.pos()), True)

    def delVertex(self, row):
        print(self.vertices)
        v = self.vertices.pop(row)
        self.canvas.scene().removeItem(v['src'])
        self.canvas.scene().removeItem(v['dst'])
        print(self.vertices)

    def preview(self):
        x, y = self.layer.center.x(), self.layer.center.y()
        dx, dy = self.p0[0] - self.p1[0], self.p0[1] - self.p1[1]
        x = x - dx
        y = y - dy
        self.layer.setCenter(QgsPoint(x, y))
        self.layer.repaint()
        self.layer.commitTransformParameters()
        self.translateVertices(dx, dy)

    def translateVertices(self, dx, dy):
        v = self.vertices[-1:][0]
        i = v['src']
        p = i.toMapCoordinates(QPoint(i.x(), i.y()))
        x0, y0 = p[0], p[1]
        i.setCenter(QgsPoint(x0 - dx, y0 - dy))
