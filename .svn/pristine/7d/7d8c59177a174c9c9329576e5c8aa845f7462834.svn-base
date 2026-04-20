from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import psycopg2
import psycopg2.extras
from . import PgColumn
from . import PgRow
from . import Delegates
from . import PgFieldGroup


class Dialog(QtGui.QDialog):
    def __init__(self, tableName):
        """
        Constructor

        :param tableName: name of table in database
        """
        super(Dialog, self).__init__()
        self.tableName = tableName  # type: str
        self.columns = []           # type: list[PgColumn.Column]
        self.tableModel = None      # type: PgTableModel
        self.tableView = None       # type: QtGui.QTableView
        self.fieldsGroups = []      # type: list[PgFieldGroup.FieldGroup]

    def setConnection(self, dbhost, dbuser, dbpass, dbname, dbport="5432"):
        """
        Set connection parameters

        :param dbhost: Hostname
        :param dbuser: Username
        :param dbpass: Password
        :param dbname: Database name
        :param dbport: Port (default 5432)
        """
        self.dbhost, self.dbport, self.dbuser, self.dbpass, self.dbname = dbhost, dbport, dbuser, dbpass, dbname

    def addColumn(self, name, label, is_key=False, column_type=PgColumn.ColumnType.TEXT):
        """
        Add a new table column

        :param name: name of the column in database
        :param label: Header of the table widget
        :param is_key: Set to True if column is a key
        :param column_type: Column type
        :rtype PgColumn.Column
        """
        c = PgColumn.Column(name, label, is_key, is_key)
        c.setType(column_type)
        self.columns.append(c)
        return c

    def addFieldsGroup(self, label):
        # type: (str) -> PgFieldGroup.FieldGroup
        g = PgFieldGroup.FieldGroup(label)
        self.fieldsGroups.append(g)
        return g

    def setupUi(self):
        layout = QVBoxLayout()
        self.createTable()
        buttons = self.createButtons()
        groups = self.createFieldGroups()
        layout.addLayout(buttons)
        for i in groups:
            layout.addWidget(i)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        pass

    def createTable(self):
        self.tableView = QTableView()
        self.tableModel = PgTableModel(self.dbhost, self.dbport, self.dbuser, self.dbpass, self.dbname, self.tableName, self.columns)
        self.tableView.setModel(self.tableModel)
        for idx, value in enumerate(self.columns):
            if value.type == PgColumn.ColumnType.DATE:
                self.tableView.setItemDelegateForColumn(idx, Delegates.DatePickerDelegate(value, self))
            if value.type == PgColumn.ColumnType.INTEGER:
                self.tableView.setItemDelegateForColumn(idx, Delegates.IntegerDelegate(value, self))
        self.tableView.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        return

    def createButtons(self):
        buttons = QHBoxLayout()
        buttonAdd = QPushButton("Nouveau")
        buttonDel = QPushButton("Suypprimer")
        buttonSave = QPushButton("Enregistrer")
        buttonCancel = QPushButton("Annuler")
        buttons.addWidget(buttonAdd)
        buttons.addWidget(buttonDel)
        buttons.addSpacerItem(QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
        buttons.addWidget(buttonSave)
        buttons.addWidget(buttonCancel)

        buttonAdd.clicked.connect(self.add)
        buttonDel.clicked.connect(self.delete)
        buttonSave.clicked.connect(self.save)
        buttonCancel.clicked.connect(self.close)
        return buttons

    def createFieldGroups(self):
        # type: () -> [QtGui.QGroupBox]
        fieldGroups = []
        for g in self.fieldsGroups:
            fieldGroup = QtGui.QGroupBox(g.label)
            fieldGroups.append(fieldGroup)
            flayout = QtGui.QFormLayout()

            for k in g.fields:
                if k.type == PgColumn.ColumnType.DATE:
                    w = QtGui.QDateEdit()
                    w.setCalendarPopup(True)
                else:
                    w = QtGui.QLineEdit()
                flayout.addRow(QtGui.QLabel(k.label), w)
                fieldGroup.setLayout(flayout)
        return fieldGroups

    def show(self):
        self.setupUi()
        super(Dialog, self).show()

    def save(self):
        """
        Perform save to database

        :return:
        """
        modified = self.tableModel.getModifiedData()
        for i in modified:
            self.saveUpdate(i)

        deleted = self.tableModel.getDeletedData()
        # TODO: Confirmation on deletion
        for i in deleted:
            self.saveDelete(i)
        self.close()

    def add(self):
        """
        Add a new row

        :return:
        """
        count = self.tableModel.rowCount()
        self.tableModel.insertRow(0)

    def delete(self):
        indexes = self.tableView.selectedIndexes()
        self.tableView.setUpdatesEnabled(False)
        for index in indexes:
            self.tableModel.deleteRow(index)
        self.tableView.setUpdatesEnabled(True)

    def saveUpdate(self, modified):
        """
        Save modified row

        :param modified: Modified row
        :type modified: PgRow.Row
        :return:
        """
        connection = psycopg2.connect(database=self.dbname, user=self.dbuser, password=self.dbpass, host=self.dbhost)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        column_names = []
        column_values = []
        for idx, val in enumerate(self.columns):
            column_names.append(val.name + " = " + "%s") if not val.is_key else None
            column_values.append(str(modified[idx])) if not val.is_key else None
        whereClause = " AND ".join(self.whereClause())
        setClause = ", ".join(column_names)
        sql = "UPDATE " + self.tableName \
              + " SET " + setClause \
              + " WHERE " + whereClause
        column_values += self.whereValues(modified)
        cursor.execute(sql, column_values)
        connection.commit()
        cursor.close()
        connection.close()

    def saveDelete(self, deleted):
        """
        Commit deleted rows

        :param deleted: Modified row
        :type deleted: PgRow.Row
        :return:
        """
        connection = psycopg2.connect(database=self.dbname, user=self.dbuser, password=self.dbpass, host=self.dbhost)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        whereClause = " AND ".join(self.whereClause())
        whereValues = self.whereValues(deleted)

        sql = "DELETE FROM " + self.tableName + " WHERE " + whereClause
        cursor.execute(sql, whereValues)
        connection.commit()
        cursor.close()
        connection.close()
    
    def whereClause(self):
        """
        Get where clause for a modified row

        :return [str]
        """
        keys = filter(lambda x: x.is_key, self.columns)
        wheres = []
        for idx, val in enumerate(keys):
            wheres.append(val.name + " = %s")
        return wheres

    def whereValues(self, modified):
        """
        Get values for where clause

        :param modified: modified row
        :type modified: PgRow.Row
        :return: [str]
        """
        keys = filter(lambda x: x.is_key, self.columns)
        wheres = []
        for idx, val in enumerate(keys):
            wheres.append(modified[idx])
        return wheres


class PgTableModel(QAbstractTableModel):
    columns = []    # type: list[PgColumn.Column]
    arraydata = []  # type: list[PgRow.Row]

    def __init__(self, dbhost, dbport, dbuser, dbpass, dbname, tablename, columns, *args):
        self.dbhost, self.dbport, self.dbuser, self.dbpass, self.dbname = dbhost, dbport, dbuser, dbpass, dbname
        self.tablename, self.columns = tablename, columns
        QAbstractTableModel.__init__(self, None, *args)
        self.arraydata = []
        self.init_data()

    def init_data(self):
        keys = filter(lambda x: x.is_key, self.columns)
        order = " ORDER BY " + ", ".join(map(lambda x: x.name, keys))

        connection = psycopg2.connect(database=self.dbname, user=self.dbuser, password=self.dbpass, host=self.dbhost)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM " + self.tablename + (order if len(keys) > 0 else ""))
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            j = 0
            datarow = PgRow.Row()
            for col in self.columns:
                datarow.append(str(row[col.name]))
                j += 1
            self.arraydata.append(datarow)
            i += 1
        cursor.close()
        connection.close()

    def insertRow(self, p_int, parent=None, *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.arraydata), len(self.arraydata) + 1)
        datarow = PgRow.Row()
        for col in self.columns:
            datarow.append("")
            datarow.status = PgRow.RowStatus.INSERTED
        self.arraydata.append(datarow)
        self.endInsertRows()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.arraydata)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.columns)

    def data(self, index, role=None):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.arraydata[index.row()][index.column()]
        if role == Qt.BackgroundColorRole:
            if self.arraydata[index.row()].status == PgRow.RowStatus.UPDATED:
                return QColor(Qt.yellow)
            if self.arraydata[index.row()].status == PgRow.RowStatus.DELETED:
                return QColor(Qt.red)
            if self.arraydata[index.row()].status == PgRow.RowStatus.INSERTED:
                return QColor(Qt.green)
        return None

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[col].label
        return None

    def flags(self, index):
        if self.columns[index.column()].readonly:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self.arraydata[index.row()].status == PgRow.RowStatus.DELETED:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def setData(self, index, value, role=None):
        if index.isValid():
            self.arraydata[index.row()][index.column()] = value
            return True
        return False

    def deleteRow(self, index):
        if index.isValid():
            self.arraydata[index.row()].status = PgRow.RowStatus.DELETED

    def getModifiedData(self):
        # type: () -> [PgRow.Row]
        """
        Get list of modified data

        :return: array of modified rows
        """
        return filter(lambda x: x.status == PgRow.RowStatus.UPDATED, self.arraydata)

    def getDeletedData(self):
        # type: () -> [PgRow.Row]
        """
        Get list of deleted data

        :return: array of deleted rows
        """
        return filter(lambda x: x.status == PgRow.RowStatus.DELETED, self.arraydata)
