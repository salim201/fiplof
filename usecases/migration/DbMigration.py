from .IMigrationFilesProvider import IMigrationFilesProvider
from .IMigrationRepository import IMigrationRepository


class DbMigration:
    def __init__(self, provider, repository):  # type: (IMigrationFilesProvider, IMigrationRepository) -> None
        self.provider = provider
        self.repository = repository

    def migrate(self):
        files = sorted(self.provider.getNonExecutedFiles())
        lastExecutedFile = self.executeFiles(files)
        if lastExecutedFile is not None:
            self.repository.saveLastExecutedFile(lastExecutedFile)

    def executeFiles(self, files):  # type:(list[str]) -> str
        lastExecutedFile = None
        for file in files:
            if not self.repository.execute(file):
                break
            lastExecutedFile = file
        return lastExecutedFile
