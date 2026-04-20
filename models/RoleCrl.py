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

    def insert_role(self,data):
        cursor = self.connection.cursor()
        try:
            sql='UPDATE demande_crl SET idpersonne=%s, titulaire=%s, affiche=true WHERE iddemande=%s AND id_role=%s AND titulaire=%s;' \
                'INSERT INTO demande_crl( iddemande, id_role,idpersonne,titulaire,affiche)' \
                'SELECT  %s,%s,%s,%s,true WHERE NOT EXISTS(SELECT * FROM demande_crl WHERE iddemande=%s AND id_role=%s AND titulaire=%s)'
            print sql
            res=cursor.execute(sql,(data[2],data[3],data[0],data[1],data[3],data[0],data[1],data[2],data[3],data[0],data[1],data[3]))
            self.connection.commit()
            return res
        except Exception as e:
            print e
            self.connection.rollback()

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