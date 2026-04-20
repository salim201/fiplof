from ConfigParser import SafeConfigParser
import os


class ParamsConfig:
    def __init__(self):
        self.parser = SafeConfigParser()
        self.parser.read(self.resolve("params.ini"))
        self.auto_save_path = self.parser.get('params', 'auto_save_path')
        self.has_z_certifiable = self.parser.get('params', 'has_z_certifiable')
        self.online_interco = self.parser.get('params', 'online_interco')


    def resolve(self, name, basepath=None):
        if not basepath:
            basepath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(basepath, name)
