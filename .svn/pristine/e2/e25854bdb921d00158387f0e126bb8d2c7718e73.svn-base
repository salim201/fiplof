# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZoomToCoordinates
                                 A QGIS plugin
 Zoom,Pan and Highlight Entered Coordinates
                              -------------------
        begin                : 2013-04-10
        copyright            : (C) 2013 by Vinayan Parameswaran
        email                : vinayan123@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from zoomtocoordinatesdialog import ZoomToCoordinatesDialog


class ZoomToCoordinates:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/zoomtocoordinates"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale")

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/zoomtocoordinates_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ZoomToCoordinatesDialog()
        self.dlg.setWindowModality(QtCore.Qt.NonModal)
        self.dlg.setParent(self.iface.mainWindow(),QtCore.Qt.Dialog)
        #self.dlg = QtGui.QMainWindow(self.iface.mainWindow(), QtCore.Qt.Dialog)
        
        #add Spinbox to toolbar 
        lblScale = QLabel("Scale View By")
        self.dlg.ui.toolBar.addSeparator() 
        self.dlg.ui.toolBar.addWidget(lblScale)    
        spBox = QSpinBox()
        self.dlg.ui.toolBar.addWidget(spBox)

        self.spinBox = spBox
        
        #validations
        validator = QtGui.QDoubleValidator()
        lEditX = self.dlg.ui.mTxtX
        lEditY = self.dlg.ui.mTxtY       
        lEditX.setValidator(validator)
        lEditY.setValidator(validator)
        
        #create rubberband for point..for qgis 1.9 and higher
        self.rubberBand = None
        
        #create vertex marker for point..older versons..
        self.vMarker = None
        
        #add rubberbands for cross
        self.crossRb = QgsRubberBand(iface.mapCanvas(),QGis.Line)
        self.crossRb.setColor(Qt.black)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/zoomtocoordinates/icon.png"),
            u"ZoomToCoordinates", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        
        QObject.connect(self.dlg.ui.mActionZoomTo, SIGNAL("activated()"), self.zoom)
        QObject.connect(self.dlg.ui.mActionPan, SIGNAL("activated()"), self.pan)
        QObject.connect(self.dlg.ui.mActionFlash, SIGNAL("activated()"), self.flash)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&ZoomToCoordinates", self.action)
        
        #configure rubberbands..
        
        if QGis.QGIS_VERSION_INT >= 10900:
			self.rubberBand = QgsRubberBand(self.canvas,QGis.Point)
			self.rubberBand.setColor(Qt.red)
			#self.rubberBand.setIcon(QgsRubberBand.IconType.ICON_CIRCLE)
			self.rubberBand.setIconSize(7)
        else:
			self.vMarker = QgsVertexMarker(self.canvas)
			self.vMarker.setIconSize(10)
		

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&ZoomToCoordinates", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = 1
        #result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
            
    def zoom(self):
		print "zoom button clicked!"
		x = self.dlg.ui.mTxtX.text()
		y = self.dlg.ui.mTxtY.text()
		
		if not x:
			return
		
		if not y:
			return
			
		print x + "," + y
		scale = self.spinBox.value()
		print "scale is - " + str(scale)
		rect = QgsRectangle(float(x)-scale,float(y)-scale,float(x)+scale,float(y)+scale)
		self.canvas.setExtent(rect)
		pt = QgsPoint(float(x),float(y))
		self.highlight(pt)
		self.canvas.refresh()
		
    def pan(self):
		print "pan button clicked!"
		x = self.dlg.ui.mTxtX.text()
		y = self.dlg.ui.mTxtY.text()
		
		if not x:
			return
		
		if not y:
			return
		
		print x + "," + y
		
		canvas = self.canvas
		currExt = canvas.extent()
		
		canvasCenter = currExt.center()
		dx = float(x) - canvasCenter.x()
		dy = float(y) - canvasCenter.y()
		
		xMin = currExt.xMinimum() + dx
		xMax = currExt.xMaximum() + dx
		yMin = currExt.yMinimum() + dy
		yMax = currExt.yMaximum() + dy
		
		newRect = QgsRectangle(xMin,yMin,xMax,yMax)
		canvas.setExtent(newRect)
		pt = QgsPoint(float(x),float(y))
		self.highlight(pt)
		canvas.refresh()
		
    def flash(self):
		print "flash button clicked!"
		
		x = self.dlg.ui.mTxtX.text()
		y = self.dlg.ui.mTxtY.text()
		
		if not x:
			return
		
		if not y:
			return
		pt = QgsPoint(float(x),float(y))
		self.highlight(pt)
			
    def highlight(self,point):
		print "highlighting.."
		canvas = self.canvas
		
		currExt = canvas.extent()
		
		leftPt = QgsPoint(currExt.xMinimum(),point.y())
		rightPt = QgsPoint(currExt.xMaximum(),point.y())
		
		topPt = QgsPoint(point.x(),currExt.yMaximum())
		bottomPt = QgsPoint(point.x(),currExt.yMinimum())
		
		horizLine = QgsGeometry.fromPolyline( [ leftPt , rightPt ] )
		vertLine = QgsGeometry.fromPolyline( [ topPt , bottomPt ] )
		
		self.crossRb.reset(QGis.Line)
		self.crossRb.addGeometry(horizLine,None)
		self.crossRb.addGeometry(vertLine,None)
		
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
		QTimer.singleShot(500,self.resetRubberbands)
    
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
		
