from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from . import PgColumn


class DatePickerDelegate(QtGui.QItemDelegate):
    def __init__(self, column, parent=None, *args):
        # type: (PgColumn.Column, object, object) -> object
        QtGui.QItemDelegate.__init__(self, parent, *args)
        self.widget = None
        self.column = column

    def createEditor(self, parent, QStyleOptionViewItem, QModelIndex):
        self.widget = QtGui.QDateEdit(parent)
        self.widget.setCalendarPopup(True)
        return self.widget

    def setModelData(self, parent, model, index):
        # type: (QtGui.QWidget, QtCore.QAbstractItemModel, QtCore.QModelIndex) -> object
        value = self.widget.date().toString("yyyy-MM-dd")
        model.setData(index, value, QtCore.Qt.EditRole)


class IntegerDelegate(QtGui.QItemDelegate):
    def __init__(self, column, parent=None, *args):
        # type: (PgColumn.Column, object, object) -> object
        QtGui.QItemDelegate.__init__(self, parent, *args)
        self.widget = None
        self.column = column

    def createEditor(self, parent, QStyleOptionViewItem, QModelIndex):
        self.widget = QtGui.QSpinBox(parent)
        if PgColumn.ColumnOption.MAXIMUM in self.column.options:
            self.widget.setMaximum(self.column.options[PgColumn.ColumnOption.MAXIMUM])
        return self.widget
