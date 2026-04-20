#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, SLOT

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

class LineEditExt(QtGui.QLineEdit):
    def __init__(self, parent):
        super(LineEditExt, self).__init__(parent)
        self.setWindowModality(2)


    def initAction(self):
        from intervalleRun import intervalleRun
        intervalle = intervalleRun()
        intervalle.show()
        intervalle.exec_()

    def mousePressEvent(self, e):
        self.initAction()


