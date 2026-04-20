import ConfigParser
import os

class AppConfig:
    def __init__(self):
        self.read()

    def read(self):
        parser = ConfigParser.SafeConfigParser()
        parser.read(self.resolve("app.ini"))
        self.db_host = parser.get('database', 'host') if parser.has_section("database") else ""
        self.db_port = parser.get('database', 'port') if parser.has_section("database") else ""
        self.db_user = parser.get('database', 'user') if parser.has_section("database") else ""
        self.db_pass = parser.get('database', 'pass') if parser.has_section("database") else ""
        self.db_name = parser.get('database', 'name') if parser.has_section("database") else ""
        self.fondimage = parser.get("path", "fondimage") if parser.has_section("path") else ""

    def write(self):
        config = ConfigParser.RawConfigParser()
        config.add_section("database")
        config.add_section("path")
        config.set('database', 'host', self.db_host)
        config.set('database', 'port', self.db_port)
        config.set('database', 'user', self.db_user)
        config.set('database', 'pass', self.db_pass)
        config.set('database', 'name', self.db_name)
        config.set('path', 'fondimage', self.fondimage)
        with open(self.resolve("app.ini"), "wb") as configfile:
            config.write(configfile)

    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)