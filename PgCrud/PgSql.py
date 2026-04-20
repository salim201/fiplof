from PyQt4 import QtGui, QtCore
from PgCrud import PgColumn
import psycopg2
import psycopg2.extras


class Table:
    def __init__(self, connection, table_name):
        self.connection = connection
        self.columns = []   # type: list[PgColumn.Column]
        self.joins = []
        self.table_name = table_name

    def join(self, table_name, condition, join_type="INNER"):
        self.joins.append(join_type + " JOIN " + table_name + " ON " + condition)

    def addColumn(self, name, label, is_key=False, column_type=PgColumn.ColumnType.TEXT, alias=None, readonly=None):
        """
        Add a new table column

        :param name: name of the column in database
        :param label: Header of the table widget
        :param is_key: Set to True if column is a key
        :param column_type: Column type
        :rtype PgColumn.Column
        """
        readonlyColumn = is_key
        if readonly is not None:
            readonlyColumn = readonly
        c = PgColumn.Column(name, label, readonlyColumn, is_key, alias)
        c.setType(column_type)
        self.columns.append(c)
        return c

    def fillComboWithSql(self, widget, sql, column, idcolumn):
        # type: (QtGui.QComboBox, str, str, str) -> None
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            if(i[column] is None) and (i[idcolumn] is None):
                continue
            else:
                widget.addItem(i[column], i[idcolumn])
        cursor.close()

    def fillTable(self, tablewidget, conditions=None, orderby=None):
        # type: (QtGui.QTableWidget, list[Condition], bool) -> None
        tablewidget.setColumnCount(len(self.columns))
        i = 0
        for h in self.columns:
            header = QtGui.QTableWidgetItem()
            header.setText(h.label)
            tablewidget.setHorizontalHeaderItem(i, header)
            i += 1

        horizontal_header = tablewidget.horizontalHeader()
        for i in range(tablewidget.horizontalHeader().count()):
            horizontal_header.setResizeMode(i, QtGui.QHeaderView.ResizeToContents)
        tablewidget.horizontalHeader().setResizeMode(tablewidget.horizontalHeader().count() - 1, QtGui.QHeaderView.Stretch)

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cols = reduce(lambda x, y: (x if type(x) is str else x.selectClause()) + ", " + y.selectClause(), self.columns)
        print(cols)
        sql = "SELECT DISTINCT %s FROM %s" % (cols, self.table_name)

        for j in self.joins:
            sql += " " + j

        values = []
        if conditions is not None and len(conditions) > 0:
            where = " WHERE " + " AND ".join(map(lambda x: x.name + " = %s" if not x.like else x.name + " LIKE %s", conditions))
            values = map(lambda x: str(x.value) if not x.like else '%' + str(x.value) + '%', conditions)
            sql += where
        if orderby is not None:
            sql += " ORDER BY " + orderby
        rows = []
        try:
            cursor.execute(sql, values)
            rows = cursor.fetchall()
            tablewidget.setRowCount(len(rows))
        except Exception as e:
            print(e)
            self.connection.rollback()

        i = 0
        for row in rows:
            j = 0
            for col in self.columns:
                item = QtGui.QTableWidgetItem(str(row[col.aliasOrName()]))
                if col.readonly:
                    item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                tablewidget.setItem(i, j, item)
                j += 1
            i += 1
        cursor.close()

    def fillTableWithSql(self, tablewidget, sql, wheres, values, columns):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if len(wheres) > 0:
            sql += " WHERE " + " AND ".join(wheres)
        rows = []
        try:
            cursor.execute(sql, values)
            rows = cursor.fetchall()
        except Exception as e:
            print(e)
            self.connection.rollback()

        tablewidget.setRowCount(len(rows))
        tablewidget.setColumnCount(len(columns))
        i = 0
        for h in columns:
            header = QtGui.QTableWidgetItem()
            header.setText(h)
            tablewidget.setHorizontalHeaderItem(i, header)
            i += 1
        i = 0
        for row in rows:
            j = 0
            for col in row:
                item = QtGui.QTableWidgetItem(str(col))
                tablewidget.setItem(i, j, item)
                j += 1
            i += 1
        cursor.close()
        return rows

    def getSelectedId(self, tablewidget, col=0):
        # type: (QtGui.QTableWidget, list[Condition]) -> str
        indexes = tablewidget.selectedIndexes()  # type: list[QtCore.QModelIndex]
        if len(indexes) == 0:
            return None
        r = indexes[0].row()
        return str(tablewidget.item(r, col).text())


class Condition:
    def __init__(self, name, value, like=False):
        self.name, self.value, self.like = name, value, like
