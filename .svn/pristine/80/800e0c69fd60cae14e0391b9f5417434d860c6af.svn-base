from genericpath import isdir
from .IFilesystem import IFilesystem
from .IMigrationFilesProvider import IMigrationFilesProvider
from .IFilesystem import IFilesystem
from .IMigrationRepository import IMigrationRepository


class MigrationFilesProvider(IMigrationFilesProvider):
    def __init__(self, migrationFolder, repository, filesystem):  # type:(str, IMigrationRepository, IFilesystem)->None
        self.migrationFolder = migrationFolder
        self.repository = repository
        self.filesystem = filesystem

    def getNonExecutedFiles(self):
        if not self.filesystem.path.isdir(self.migrationFolder):
            return []
        lastExecutedFile = self.repository.getLastExecutedFile()
        allFiles = sorted(self.filesystem.listdir(self.migrationFolder))
        allFilesWithPath = self.__mapFilesWithDirectory(allFiles)
        if allFilesWithPath.count(lastExecutedFile) == 0:
            return allFilesWithPath
        index = allFilesWithPath.index(lastExecutedFile) + 1
        return allFilesWithPath[index:]

    def __mapFilesWithDirectory(self, files):
        return map(lambda file: '%s/%s' % (self.migrationFolder, file), files)
