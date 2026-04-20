from BaseModel import BaseModel


class Groupe(BaseModel):
    def table_name(self):
        return "groupe"

    def key_name(self):
        return "id"

    def key_value(self):
        return self.id

    def fields(self):
        f = ("nom", "description")
        return f

    def values(self):
        v = (self.nom, self.description)
        return v

    def __init__(self, connection):
        BaseModel.__init__(self, connection)
        self.id, self.nom, self.description = 0, "", ""

    def map(self, res):
        self.id, self.nom, self.description = res["id"], res["nom"], res["description"]
