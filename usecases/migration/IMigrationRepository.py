class IMigrationRepository:
    def execute(self, file):  # type:(str) -> bool
        raise NotImplementedError

    def saveLastExecutedFile(self, file):  # type:(str) -> None
        raise NotImplementedError

    def getLastExecutedFile(self):  # type:()->str
        raise NotImplementedError
