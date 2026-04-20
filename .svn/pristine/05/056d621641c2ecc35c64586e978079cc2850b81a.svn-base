from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *


class IdentifyGeometry(QgsMapToolIdentify):
    def __init__(self, canvas,parent):
        self.parent = parent
        self.fiscalite = self.parent.fiscalite
        self.titre = self.parent.titre
        self.cadastre = self.parent.cadastre
        self.demande_fn = self.parent.demande_fn
        self.tss = self.parent.tss
        self.z_certifiable = self.parent.z_certifiable
        self.VecteurBase = self.parent.VecteurBase
        self.allAlayer = []
        self.Paps = self.parent.Paps
        self.canvas = canvas
        self.dragging = False
        self.ui_ = parent.ui
        self.feature  = None
        self.layer = None
        QgsMapToolIdentify.__init__(self, canvas)

    def canvasReleaseEvent(self, event):
        layer = self.parent.cLayer
        #layer = self.canvas.currentLayer()
        print "layer in"
        print layer
        print "layer out"
        if layer is None:
            return
        self.layer = layer
        print("VECTEUR BASE")
        print(self.VecteurBase)
        p = self.Paps
        i = 0
        if (len(p) == 0):
            pass
        else:
            for Ps in p:
                self.allAlayer.append(Ps)
                i = i+1

        try:
            for index in range(self.ui_.listWidget.count()):
                if self.ui_.listWidget.item(index).checkState() > 0:
                    if str(self.ui_.listWidget.item(index).text()) == "Fiscalite":
                        self.allAlayer.append(self.fiscalite)
                    if str(self.ui_.listWidget.item(index).text()) == "Titre":
                        self.allAlayer.append(self.titre)
                    if str(self.ui_.listWidget.item(index).text()) == "Demande FN":
                        self.allAlayer.append(self.demande_fn)
                    if str(self.ui_.listWidget.item(index).text()) == "Cadastre":
                        self.allAlayer.append(self.cadastre)
                    if str(self.ui_.listWidget.item(index).text()) == "TSS":
                        self.allAlayer.append(self.tss)
                    #if str(self.ui_.listWidget.item(index).text()) == "Zone Certifiable":
                        #self.allAlayer.append(self.z_certifiable)


        except Exception as err:
            print(err)

        self.allAlayer.append(layer)

        print("ALLL LAYER")
        alLLayer = self.allAlayer
        print(self.allAlayer)
        print("vector LAYER")
        print(self.VectorLayer)
        try:
            results = self.identify(event.x(), event.y(), self.TopDownStopAtFirst, self.allAlayer, self.VectorLayer)
            print "RESULT IN IDENT"
            print results

            if len(results) > 0:
                print " YES emit(SIGNAL(geomIdentified) "
                
                self.emit(SIGNAL("geomIdentified"), results[0].mLayer, results[0].mFeature)
                point = self.toMapCoordinates(event.pos())
#                layer = self.canvas.currentLayer()
                layer = results[0].mLayer
                self.feature  = results[0].mFeature
#                print  self.feature.id()
                if event.modifiers() & Qt.ShiftModifier:
                    print "modifiers"
                    layer.select(self.feature.id())
                else:
                    layer.setSelectedFeatures([self.feature.id()])
                    QgsProject.instance().setSnapSettingsForLayer(layer.id(), True, 2, 1, 1000, True)
                    print "setSelected"
                if layer == None:
                    print "None"
                    return
                if layer.type() != QgsMapLayer.VectorLayer:
                    print "QgsMapLayer.VectorLayer"
                    return
                    point = self.canvas.mapRenderer().mapToLayerCoordinates(layer, point)
                    pixTolerance = 6
                    mapTolerance = pixTolerance * self.canvas.mapUnitsPerPixel()
                    rect = QgsRectangle(point.x() - mapTolerance, point.y() - mapTolerance, point.x() + mapTolerance,
                            point.y() + mapTolerance)
                    provider = layer.dataProvider()
            else:
                print " NOT emit(SIGNAL(geomIdentified) "
                #identify fiscalite

            self.allAlayer = []

        except Exception as e:
            print(e)