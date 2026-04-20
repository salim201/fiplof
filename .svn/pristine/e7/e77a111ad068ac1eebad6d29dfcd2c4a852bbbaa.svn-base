from usecases.migration.IFilesystem import IFilesystem
import os
import re


class DateBasedFilesystem(IFilesystem):
    def __init__(self):
        self.path = os.path

    def listdir(self, dirname):
        files = os.listdir(dirname)
        return filter(self.filterDateBasedFile, files)

    def filterDateBasedFile(self, filename):
        match = re.match('\d{4}-\d{2}-\d{2}-(.*)\.sql', filename)
        return match is not None
