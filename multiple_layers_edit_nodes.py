# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MultipleLayersEditNodes
                                 A QGIS plugin
 select between Layers and active de node toll 
                              -------------------
        begin                : 2017-06-01
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Carlos Eduardo Cagna\ IBGE
        email                : carlos.cagna@ibge.gov.br
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *
from MultipleLayersEditNodesButton import MultipleLayersEditNodesButton
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from multiple_layers_edit_nodes_dialog import MultipleLayersEditNodesDialog
import os.path


class MultipleLayersEditNodes:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MultipleLayersEditNodes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Multiple Layers Edit Nodes')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MultipleLayersEditNodes')
        self.toolbar.setObjectName(u'MultipleLayersEditNodes')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MultipleLayersEditNodes', message)


    def createToolButton(self, parent, text):
        button = QToolButton(parent)
        button.setObjectName(text)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        parent.addWidget(button)
        return button        

    def createAction(self, icon_path, text, callback):
        action = QAction(
            QIcon(icon_path),
            text,
            self.iface.mainWindow())
        # connect the action to the run method
        action.setCheckable(True)
        action.toggled.connect(callback)
        return action        
        
    # noinspection PyMethodMayBeStatic

    def createClearAction(self, icon_path, text):
        action = QAction(
            QIcon(icon_path),
            text,
            self.iface.mainWindow())
        # connect the action to the run method
        action.setCheckable(False)
        action.triggered.connect(self.clear)
        return action        

        
    def initGui(self):
        # Create action that will start plugin configuration
        self.actionCriar = self.createAction(":/plugins/MultipleLayersEditNodes/icon.png",
                                            u"Multiple Layers Edit Nodes",
                                            self.run)




                
        self.tool = MultipleLayersEditNodesButton(self.iface, self.iface.mapCanvas(), self.actionCriar)
        print self.actionCriar

        
        #QToolButtons
        self.selectionButton = self.createToolButton(self.toolbar, u'MultipleLayersEditNodesButton')
        self.selectionButton.addAction(self.actionCriar)     

        self.selectionButton.setDefaultAction(self.actionCriar)    


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Multiple Layers Edit Nodes'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        

    def run(self, b):

        self.selectionButton.setDefaultAction(self.selectionButton.sender())
        if b:
            self.iface.mapCanvas().setMapTool(self.tool)
        else:
            self.iface.mapCanvas().unsetMapTool(self.tool)