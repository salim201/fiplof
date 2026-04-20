from ..IMigrationRepository import IMigrationRepository


class RepositoryStub(IMigrationRepository):
    def __init__(self):
        self.executedFiles = []
        self.lastExecutedFile = ''
        self.errorousFiles = []

    def setErrorousFiles(self, files):
        self.errorousFiles = files

    def execute(self, file):
        if self.errorousFiles.count(file) > 0:
            return False
        self.executedFiles.append(file)
        return True

    def getExecutedFiles(self):
        return self.executedFiles

    def saveLastExecutedFile(self, file):  # type: (str) -> None
        self.lastExecutedFile = file

    def getLastExecutedFile(self):
        return self.lastExecutedFile
