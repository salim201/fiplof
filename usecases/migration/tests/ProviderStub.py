from ..IMigrationFilesProvider import IMigrationFilesProvider


class ProviderStub(IMigrationFilesProvider):
    def __init__(self, files):  # type:(list[str]) -> None
        self.files = files

    def getNonExecutedFiles(self):
        return self.files
