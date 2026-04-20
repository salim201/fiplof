from BaseModel import BaseModel


class GroupeAcces(BaseModel):
    def table_name(self):
        return "groupe_acces"

    def key_name(self):
        return "id"

    def key_value(self):
        return self.id

    def map(self, r):
        self.id, self.groupe_id, self.acces_id, self.autorise = r["id"], r["groupe_id"], r["acces_id"], r["autorise"]

    def fields(self):
        return "groupe_id", "acces_id", "autorise"

    def values(self):
        return self.groupe_id, self.acces_id, self.autorise

    def __init__(self, connection):
        BaseModel.__init__(self, connection)
        self.id, self.groupe_id, self.acces_id, self.autorise = 0, 0, 0, False

    def find_existant(self):
        q = self.query("SELECT * FROM " + self.table_name() + " WHERE groupe_id = %s AND acces_id = %s", (self.groupe_id, self.acces_id))
        if len(q) > 0:
            self.map(q[0])

    def find_by_gid(self, gid):
        # type: (int) -> list[GroupeAcces]
        results = []
        q = self.query("SELECT * FROM " + self.table_name() + " WHERE groupe_id = %s",
                       (gid, ))
        for r in q:
            a = GroupeAcces(self.connection)
            a.map(r)
            results.append(a)
        return results
