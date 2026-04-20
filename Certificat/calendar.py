#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

This example shows a QtGui.QCalendarWidget widget.

author: Jan Bodnar
website: zetcode.com
last edited: September 2011
"""

import sys
from PyQt4 import QtGui, QtCore


class CalendarEx(QtGui.QWidget):
    def __init__(self):
        super(CalendarEx, self).__init__()

        self.initUI()

    def initUI(self):
        calendar = QtGui.QCalendarWidget(self)
        calendar.setWindowModality(3)
        calendar.setMinimumDate(QtCore.QDate(1900, 1, 1))
        calendar.setMaximumDate(QtCore.QDate(3000, 1, 1))
        calendar.setGridVisible(True)
        calendar.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        calendar.setStyleSheet('background: white; color: black')
        calendar.setGridVisible(True)
        pos = QtGui.QCursor.pos()
        calendar.setGeometry(pos.x(), pos.y(), 300, 200)
        calendar.show()
