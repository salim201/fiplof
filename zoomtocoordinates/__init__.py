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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "ZoomToCoordinates"


def description():
    return "Zoom,Pan and Highlight Entered Coordinates"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Vinayan Parameswaran"

def email():
    return "vinayan123@gmail.com"

def classFactory(iface):
    # load ZoomToCoordinates class from file ZoomToCoordinates
    from zoomtocoordinates import ZoomToCoordinates
    return ZoomToCoordinates(iface)
