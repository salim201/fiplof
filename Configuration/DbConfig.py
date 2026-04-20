from ConfigParser import SafeConfigParser
import os


class DbConfig:
    def __init__(self):
        self.parser = SafeConfigParser()
        self.parser.read(self.resolve("app.ini"))
        self.db_host = self.parser.get('database', 'host')
        self.db_port = self.parser.get('database', 'port')
        self.db_user = self.parser.get('database', 'user')
        self.db_pass = self.parser.get('database', 'pass')
        self.db_name = self.parser.get('database', 'name')

    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)
