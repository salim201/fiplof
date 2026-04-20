class ColumnType:
    TEXT = 0
    INTEGER = 1
    DATE = 2


class ColumnOption:
    MINIMUM = 0
    MAXIMUM = 1


class Column:
    def __init__(self, name, label, readonly, is_key, alias):
        """
        Create a new column

        :param name: column name in database
        :param label: label in table widget header
        :param readonly: Set to True if column is readonly
        """
        self.name, self.label, self.readonly, self.is_key, self.alias = name, label, readonly, is_key, alias
        self.type = ""
        self.options = {}

    def setType(self, colum_type):
        # type: (ColumnType) -> None
        """
        Set column type

        :param colum_type:
        :type colum_type: int
        :return: None
        """
        self.type = colum_type

    def setOption(self, option, value):
        """
        Set column option

        :param option: option
        :type option: int
        :param value: option value
        :return: None

        Example:
            c.setOption(PgColumn.ColumnOption.MAXIMUM, 100)
        """
        self.options[option] = value

    def selectClause(self):
        if self.alias:
            return "%s as %s" % (self.name, self.alias)
        return self.name

    def aliasOrName(self):
        if self.alias:
            return self.alias
        return self.name
