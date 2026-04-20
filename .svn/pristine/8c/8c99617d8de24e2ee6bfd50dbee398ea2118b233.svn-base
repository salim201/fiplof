from BaseModel import BaseModel


class Fokontany(BaseModel):
    def table_name(self):
        return "fokontany"

    def key_name(self):
        return "idfokontany"

    def key_value(self):
        return self.fokontanyid

    def fields(self):
        f = ("idcommune", "codefokontany", "nomfokontany", "shapelength", "shapearea", "csv_id")
        return f

    def values(self):
        v = (self.idfokontany, self.idcommune, self.codefokontany, self.nomfokontany, self.shapelength, self.shapearea, self.csv_id)
        return v

    def __init__(self, connection):
        BaseModel.__init__(self, connection)
        self.idfokontany, self.idcommune, self.codefokontany, self.nomfokontany, self.shapelength, self.shapearea, self.csv_id =\
            0, 0, "", "", None, None, None

    def map(self, res):
        self.idfokontany, self.idcommune, self.codefokontany, self.nomfokontany, self.shapelength, self.shapearea, self.csv_id =\
            res['idfokontany'], res['idcommune'], res['codefokontany'], res['nomfokontany'], res['shapelength'], res['shapearea'], res['csv_id']

