from .BaseModel import BaseModel


class Journal(BaseModel):
    def __init__(self, connection):
        BaseModel.__init__(self, connection)
        self.id, self.idutilisateur, self.idobjetcible, self.typeobjectcible = 0, 0, 0, ""
        self.description, self.dateaction, self.heureaction = "", "", ""

    def table_name(self):
        return "journal"

    def key_name(self):
        return "id"

    def key_value(self):
        return self.id

    def map(self, r):
        self.id, self.idutilisateur, self.idobjetcible = r["id"], r["idutilisateur"], r["idobjetcible"]
        self.typeobjectcible = r["typeobjectcible"]
        self.description, self.dateaction, self.heureaction = r["description"], r["dateaction"], r["heureaction"]

    def fields(self):
        return "idutilisateur", "idobjetcible", "typeobjectcible", "description", "dateaction", "heureaction"

    def values(self):
        return self.idutilisateur, self.idobjetcible, self.typeobjectcible, self.description, \
            self.dateaction, self.heureaction
