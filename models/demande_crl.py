from BaseModel import BaseModel


class demande_crl(BaseModel):
    def table_name(self):
        return "demande_crl"

    def key_name(self):
        return "id_role"

    def key_value(self):
        return self.role_id

    def fields(self):
        f = ("libelle_role")
        return f

    def values(self):
        v = (self.id_role, self.libelle_role)
        return v

    def __init__(self, connection):
        BaseModel.__init__(self, connection)
        self.id_role, self.libelle_role=0, ""

    def map(self, res):
        self.role_id, self.libelle_role =\
            res['id_role'], res['libelle_role']


