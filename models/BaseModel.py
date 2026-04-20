import psycopg2
import psycopg2.extras


class BaseModel:
    def __init__(self, connection):
        self.connection = connection

    def table_name(self):
        raise NotImplementedError()

    def key_name(self):
        raise NotImplementedError()

    def key_value(self):
        raise NotImplementedError()

    def map(self, r):
        raise NotImplementedError()

    def fields(self):
        # type: () -> list
        raise NotImplementedError()

    def values(self):
        raise NotImplementedError()

    def find_all(self):
        results = []
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM %s" % self.table_name())
            rows = cursor.fetchall()
            for r in rows:
                d = self.__class__(self.connection)
                d.map(r)
                results.append(d)
        except Exception as e:
            print(e)
        cursor.close()
        return results

    def find_by_id(self, theid):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            sql = "SELECT * FROM %s" % (self.table_name())
            cursor.execute(sql + " WHERE " + self.key_name() + "=%s", (theid,))
            res = cursor.fetchone()
            t = self.__class__(self.connection)
            t.map(res)
            return t
        except Exception as e:
            print(e)
        cursor.close()
        return None

    def find_by_lib(self, theid):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            sql = "SELECT * FROM %s" % (self.table_name())
            cursor.execute(sql + " WHERE " + self.key_name() + "=%s", (theid,))
            res = cursor.fetchone()
            t = self.__class__(self.connection)
            t.map(res)
            return t
        except Exception as e:
            print(e)
        cursor.close()
        return None

    def insert(self):
        # type: () -> int
        id_of_new_row = 0
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            fields = self.fields()
            place_holders = ",".join(map(lambda x: "%s", fields))
            cursor.execute(
                "INSERT INTO " + self.table_name() + "(" + ",".join(fields) + ") VALUES(" + place_holders + ") "
                "RETURNING " + self.key_name(),
                self.values()
            )
            id_of_new_row = cursor.fetchone()[0]
            self.connection.commit()
            print("INSERT INTO " + self.table_name() + "(" + ",".join(fields) + ") VALUES(" + place_holders + ") ")
        except Exception as e:
            print(e)
            cursor.close()
            self.connection.rollback()
        return id_of_new_row

    def update(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        uid = 0
        try:
            fields = self.fields()
            place_holders = ",".join(map(lambda x: x + "=%s", fields))
            values = self.values() + (self.key_value(), )
            cursor.execute(
                "UPDATE " + self.table_name()
                + " SET " + place_holders
                + " WHERE " + self.key_name() + "=%s", values
            )
            self.connection.commit()
            uid = self.key_value()
        except Exception as e:
            print(e)
            cursor.close()
            self.connection.rollback()
        return uid

    def delete_by_id(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("DELETE FROM " + self.table_name() + " WHERE " + self.key_name() + " = %s",
                           (self.key_value(),))
            cursor.close()
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()

    def save(self):
        # type: () -> int
        if self.key_value():
            return self.update()
        else:
            return self.insert()

    def query(self, sql, params):
        results = []
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            for r in rows:
                results.append(r)
        except Exception as e:
            print(e)
            self.connection.rollback()
        cursor.close()
        return results
