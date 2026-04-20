#! /usr/bin/python
# -*- coding: utf-8 -*-
# Python v3

from PyQt4 import QtGui, QtDesigner
import os
# ===== à adapter selon le widget! ==========================================
# nom (str) du fichier du widget sans extension
FICHIERWIDGET = "ui.territoirewidget"
# nom (str) de la classe du widget importé
NOMCLASSEWIDGET = "TerritoireWidget"
# nom (str) de l'instance crée dans Designer
NOMWIDGET = "territoire"
# groupe (str) de widgets pour Designer
GROUPEWIDGET = "Plof"
# texte (str) pour le toolTip dans Designer
TEXTETOOLTIP = "Combobox des territoires Plof"
# texte (str) pour le whatsThis dans Designer
TEXTEWHATSTHIS = "Combobox des territoires Plof"
# icone (rien ou QPixmap) pour présenter le widget dans Designer
ICONFILE = "icons/map.png"
# ===========================================================================

# importation de la classe du widget
modulewidget = __import__(FICHIERWIDGET, fromlist=[NOMCLASSEWIDGET])
CLASSEWIDGET = getattr(modulewidget, NOMCLASSEWIDGET)


#############################################################################
class TerritoirePlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    """classe pour renseigner Designer sur le widget
       nom de classe à renommer selon le widget
    """

    # ========================================================================
    def __init__(self, parent=None):
        super(TerritoirePlugin, self).__init__(parent)
        self.initialized = False

    # ========================================================================
    def initialize(self, core):
        if self.initialized:
            return
        self.initialized = True
        # ========================================================================

    def isInitialized(self):
        return self.initialized

    # ========================================================================
    def createWidget(self, parent):
        """retourne une instance de la classe qui définit le nouveau widget
        """
        return CLASSEWIDGET(parent)

    # ========================================================================
    def name(self):
        """définit le nom du widget dans QtDesigner
        """
        return NOMCLASSEWIDGET
        # ========================================================================

    def group(self):
        """définit le nom du groupe de widgets dans QtDesigner
        """
        return GROUPEWIDGET

    # ========================================================================
    def icon(self):
        """retourne l'icone qui represente le widget dans Designer
           => un QtGui.QIcon() ou un QtGui.QIcon(imagepixmap)
        """
        iconpath = (os.path.dirname(os.path.realpath(__file__))) + "/" + ICONFILE
        return QtGui.QIcon(QtGui.QPixmap(iconpath))

    # ========================================================================
    def toolTip(self):
        """retourne une courte description du widget comme tooltip
        """
        return TEXTETOOLTIP
        # ========================================================================

    def whatsThis(self):
        """retourne une courte description du widget pour le "What's this?"
        """
        return TEXTEWHATSTHIS
        # ========================================================================

    def isContainer(self):
        """dit si le nouveau widget est un conteneur ou pas
        """
        return False
        # ========================================================================

    def domXml(self):
        """donne des propriétés du widget pour utilisation dans Designer
        """
        return ('<widget class="{}" name="{}">\n' \
                ' <property name="toolTip" >\n' \
                '  <string>{}</string>\n' \
                ' </property>\n' \
                ' <property name="whatsThis" >\n' \
                '  <string>{}</string>\n' \
                ' </property>\n' \
                '</widget>\n' \
                ).format(NOMCLASSEWIDGET, NOMWIDGET, TEXTETOOLTIP, TEXTEWHATSTHIS)
        # ========================================================================

    def includeFile(self):
        """retourne le nom du fichier (str sans extension) du widget
        """
        return "Widgets." + FICHIERWIDGET