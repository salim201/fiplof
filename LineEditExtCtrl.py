#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, SLOT
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



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

class LineEditExtCtrl(QtGui.QLineEdit):
    def __init__(self, parent):
        super(LineEditExtCtrl, self).__init__(parent)
        # type = 0 => Alphabetique, type = 1 => numerique, type =2 => Alphanumerique, type = 3 => date
        #self.setValidator(validator)
        #self.setWindowModality(2)

    def initActions(self):
        self.textEdited.connect(self.controlInput)

    def controlInput(self, s):
        state = self.validator.validate(_fromUtf8(s))
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b' # green
        elif state == QtGui.QValidator.Intermediate:
            color = '#fff79a' # yellow
        else:
            color = '#f6989d' # red
        self.setStyleSheet('QLineEdit { background-color: %s }' % color)
        #print _fromUtf8(ret)

    def setTypeChamp(self, typechamp, required = None):
        if typechamp == 'alpha':
            regexp = QtCore.QRegExp('\D*')
        elif typechamp == 'alphanumerique':
            regexp = QtCore.QRegExp('\w*')
        elif typechamp == 'date':
            regexp = QtCore.QRegExp('\d{1,2}/\d{1,2}/\d{4}')
        elif typechamp == 'numerique':
            regexp = QtCore.QRegExp('\d*')

        validator = QtGui.QRegExpValidator(regexp)
        self.setValidator(validator)
        self.required = required


