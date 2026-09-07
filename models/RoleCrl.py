from BaseModel import BaseModel


class RoleCrl(BaseModel):
    def table_name(self):
        return "role_crl"

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

    def insert_role(self, data):
        cursor = self.connection.cursor()
        try:
            sql = ('UPDATE demande_crl SET idpersonne=%s, titulaire=%s, president=%s, affiche=true '
                   'WHERE iddemande=%s AND id_role=%s AND titulaire=%s;'
                   'INSERT INTO demande_crl(iddemande, id_role, idpersonne, titulaire, president, affiche) '
                   'SELECT %s,%s,%s,%s,%s,true '
                   'WHERE NOT EXISTS(SELECT * FROM demande_crl WHERE iddemande=%s AND id_role=%s AND titulaire=%s)')
            print sql
            res = cursor.execute(sql, (
                data[2], data[3], data[4],
                data[0], data[1], data[3],
                data[0], data[1], data[2], data[3], data[4],
                data[0], data[1], data[3]
            ))
            self.connection.commit()
            return res
        except Exception as e:
            print(e)
            self.connection.rollback()

    def find_or_create_by_lib(self, lib):
        role = self.find_by_lib(lib)
        if role:
            return role
        cursor = self.connection.cursor()
        try:
            sql = "INSERT INTO role_crl (libelle_role) VALUES (%s) RETURNING id_role"
            cursor.execute(sql, (lib,))
            id_role = cursor.fetchone()[0]
            self.connection.commit()
            return (id_role, lib)
        except Exception as e:
            print(e)
            self.connection.rollback()
            return None

    def find_by_lib(self, lib):
        cursor = self.connection.cursor()
        try:
            sql = "SELECT * FROM %s" % (self.table_name())
            sql=sql + " WHERE libelle_role='"+lib+"'"
            print sql
            cursor.execute(sql)
            res = cursor.fetchone()
            return res
        except Exception as e:
            print(e)
            self.connection.rollback()