from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal


class DraggableListView(QtGui.QListWidget):
    itemMoved = pyqtSignal(int, int)

    def __init__(self, parent):
        super(DraggableListView, self).__init__(parent)

    def dropEvent(self, event):
        old_index = self.currentRow()
        super(DraggableListView, self).dropEvent(event)
        cur_index = self.currentRow()
        self.itemMoved.emit(old_index, cur_index)

    def dragEnterEvent(self, event):
        if self.currentRow() < 6:
            event.ignore()
            return
        event.accept()

    def dragMoveEvent(self, event):
        item = self.itemAt(event.answerRect().x(), event.answerRect().y())
        if self.row(item) < 6:
            event.ignore()
            return
        event.accept()
        super(DraggableListView, self).dragMoveEvent(event)

