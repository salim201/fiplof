class RowStatus():
    INITIAL = 0
    INSERTED = 1
    UPDATED = 2
    DELETED = 3


class Row:
    status = None   # type: RowStatus
    array = []

    def __init__(self):
        self.array = []

    def append(self, value):
        self.status = RowStatus.INITIAL
        self.array.append(value)

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        if self.array[key] != value:
            self.status = RowStatus.UPDATED
        self.array[key] = value.toPyObject() if "toPyObject" in dir(value) else str(value)
