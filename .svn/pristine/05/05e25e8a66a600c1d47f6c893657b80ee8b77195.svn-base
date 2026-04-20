from PyQt4.QtGui import QTableWidgetItem
from PyQt4 import QtCore

class ReadonlyTable:
    def __init__(self, tableWidget, getCellValue):
        self.tableWidget = tableWidget
        self.getCellValue = getCellValue

    def fillWithData(self, data,cf=False):
        self.tableWidget.setRowCount(0)
        i = 0
        while i < len(data):
            self.createTableRow(i, data,cf)
            i = i + 1

    def createTableRow(self, rowIndex, data,cf=False):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        columnIndex = 0
        if cf is True:
            if data[rowIndex][9]==1:
                while columnIndex < self.tableWidget.columnCount():
                    content = self.getCellValue(data, rowIndex, columnIndex)
                    self.createReadonlyTableCell(rowPosition, columnIndex, content,cf)
                    columnIndex = columnIndex + 1
            else:
                while columnIndex < self.tableWidget.columnCount():
                    content = self.getCellValue(data, rowIndex, columnIndex)
                    self.createReadonlyTableCell(rowPosition, columnIndex, content)
                    columnIndex = columnIndex + 1
        else:
            while columnIndex < self.tableWidget.columnCount():
                content = self.getCellValue(data, rowIndex, columnIndex)
                self.createReadonlyTableCell(rowPosition, columnIndex, content)
                columnIndex = columnIndex + 1

    def createReadonlyTableCell(self, rowIndex, columnIndex, cellContent,cf=False):
        cell = QTableWidgetItem(cellContent)
        cell.setFlags(cell.flags() ^ QtCore.Qt.ItemIsEditable)
        self.tableWidget.setItem(rowIndex, columnIndex, cell)
        if cf is True:
            self.tableWidget.item(rowIndex, columnIndex).setBackground(QtCore.Qt.darkCyan)
