from . import PgColumn


class FieldGroup:
    def __init__(self, label):
        self.label = label
        self.fields = []        # type: list[PgColumn.Column]

    def addField(self, name, label):
        # type: (str, str) -> PgColumn.Column
        f = PgColumn.Column(name, label, False, False)
        self.fields.append(f)
        return f
