from BaseModel import BaseModel


class Utilisateur(BaseModel):
    def table_name(self):
        return "utilisateur"

    def key_name(self):
        return "idutilisateur"

    def key_value(self):
        return self.idutilisateur

    def map(self, r):
        self.idutilisateur, self.nomutilisateur, self.prenomutilisateur, self.loginutilisateur,\
            self.passwordutilisateur, self.typeutilisateur, self.telephone, self.adresse, self.fonction, \
            self.loginufiplof, self.passwdfiplof, self.groupe_id = \
            r["idutilisateur"], r["nomutilisateur"], r["prenomutilisateur"], r["loginutilisateur"], \
            r["passwordutilisateur"], r["typeutilisateur"], r["telephone"], r["adresse"], r["fonction"], \
            r["loginufiplof"], r["passwdfiplof"], r["groupe_id"]

    def fields(self):
        f = ("idutilisateur", "nomutilisateur", "prenomutilisateur", "loginutilisateur",
             "passwordutilisateur", "typeutilisateur", "telephone", "adresse", "fonction",
             "loginufiplof", "passwdfiplof", "groupe_id")
        return f

    def values(self):
        v = (self.idutilisateur, self.nomutilisateur, self.prenomutilisateur, self.loginutilisateur,
             self.passwordutilisateur, self.typeutilisateur, self.telephone, self.adresse, self.fonction,
             self.loginufiplof, self.passwdfiplof, self.groupe_id)
        return v

    def __init__(self, connection):
        BaseModel.__init__(self, connection)
        self.idutilisateur, self.nomutilisateur, self.prenomutilisateur, self.loginutilisateur, \
            self.passwordutilisateur, self.typeutilisateur, self.telephone, self.adresse, self.fonction, \
            self.loginufiplof, self.passwdfiplof, self.groupe_id = \
            0, "", "", "",\
            "", "", "", "", "",\
            "", "", ""

    def is_deletable(self):
        if self.groupe_id != 1:
            return True
        res = self.query("SELECT count(*) AS nb FROM " + self.table_name()
                         + " WHERE groupe_id=%s AND " + self.key_name() + " != %s", (1, self.key_value()))
        return res[0]["nb"] > 0
