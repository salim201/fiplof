import psycopg2
import psycopg2.extras
import globalvars


class Inventaire:
    def __init__(self):
        self.date_inventaire, self.nomdemandeur, self.numdemande,self.datedecision= "", "", "", ""
        self.codeparcelle=""
        self.fkt= ""
        self.hameau=""
        self.isDecision=False
        self.datedemande=""

    @staticmethod
    def find_where(connection, metadata, wheres=[], page=1,limitSelect=100):
        print "ato am find_where"
        print "metadata  mandalo et eto"
        print metadata
        print "vita metadata"
        offset = (page - 1) * limitSelect
        inventaires = []
        where = ""
        print metadata
        if len(wheres) > 0:
            print "eto"
            where = "WHERE inventaire IS true AND " + " AND ".join(wheres)
        else :
            where = "WHERE inventaire IS true"
        if metadata["isDecision"]==True :
            sql = """SELECT date_inventaire,codeparcelle,pd.nomdemandeur,pd.numdemande,datedecision,h.nomhameau as nomhameau,fkt FROM parcelle_d pd
                        INNER JOIN hameau h on h.idhameau=pd.idhameau INNER JOIN demande d on d.gid=pd.gid """;
        else:
            #sql = """ SELECT date_inventaire,codeparcelle,pd.nomdemandeur,pd.numdemande,h.nomhameau as nomhameau,fkt
            #                   FROM parcelle_d pd  INNER JOIN hameau h on h.idhameau=pd.idhameau""";
            sql= """ SELECT date_inventaire,codeparcelle,CONCAT( p.nompersonne,' ', p.prenompersonne ) as nomdemandeur,pd.numdemande,d.datedemande,d.datedecision,h.nomhameau as nomhameau,ad.idpersonne,fkt FROM parcelle_d pd
                        INNER JOIN hameau h on h.idhameau=pd.idhameau
						LEFT JOIN demande d on pd.gid=d.gid
						INNER JOIN avoir_demande ad on pd.gid=ad.idparcelle		
						JOIN personne p on ad.idpersonne=p.idpersonne
						"""
            where+= "AND ad.representant=True"
        sql = sql + """ %s """% where
        #sql = """ SELECT date_inventaire,codeparcelle,pd.nomdemandeur,pd.numdemande,h.nomhameau as nomhameau,fkt FROM parcelle_d pd  INNER JOIN hameau h on h.idhameau=pd.idhameau %s""" % where
        sql_count = "WITH Q AS (%s) SELECT COUNT(*) AS num FROM Q" % sql
        #sql += " LIMIT " + str(limitSelect)
        sql += " LIMIT " + str(limitSelect) + " OFFSET " + str(offset)

        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            i=0
            for r in rows:
                print i
                d = Inventaire()
                d.map(r)
                if metadata["isDecision"]==True:
                    d.datedecision=r["datedecision"]
                else: d.datedecision=""
                inventaires.append(d)
                i=i+1
        except Exception as e:
            connection.rollback()
            print(e)
        try:
            cursor.execute(sql_count)
            row = cursor.fetchone()
            metadata["numpages"] = (int(row["num"]) / limitSelect) + 1
        except Exception as e:
            connection.rollback()
            print(e)
        cursor.close()
        return inventaires

    """
    
    def update_codep(self,):"""


    def map(self, res):
        self.date_inventaire,self.codeparcelle, self.nomdemandeur, self.numdemande,self.fkt = \
            res["date_inventaire"],res["codeparcelle"], res["nomdemandeur"], res["numdemande"], res["fkt"]
        self.hameau=res["nomhameau"]
        self.datedemande=res["datedemande"]