from BaseModel import BaseModel


class Acces(BaseModel):
    def __init__(self, connection):
        BaseModel.__init__(self, connection)
        self.id, self.nom, self.libelle = 0, "", ""

    def table_name(self):
        return "acces"

    def key_name(self):
        return "id"

    def key_value(self):
        return self.id

    def map(self, r):
        self.id, self.nom, self.libelle = r["id"], r["nom"], r["libelle"]

    def fields(self):
        return "id", "nom", "libelle"

    def values(self):
        return self.id, self.nom, self.libelle

    def category_name(self):
        return ' '.join(map(lambda a: a.capitalize(), self.nom.split('/')[0].split('_')))
