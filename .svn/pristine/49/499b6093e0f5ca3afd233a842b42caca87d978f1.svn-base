from ..IFilesystem import IFilesystem, IPath


class PathStub(IPath):
    def __init__(self, fileStructure):  # type:(dict[str, list[str]]) -> None
        self.fileStructure = fileStructure

    def isdir(self, dirname):
        return self.fileStructure.get(dirname) is not None


class FilesystemStub(IFilesystem):
    def __init__(self, fileStructure):  # type:(dict[str, list[str]]) -> None
        self.fileStructure = fileStructure
        self.path = PathStub(fileStructure)

    def listdir(self, dirname):
        return self.fileStructure[dirname]
