class IPath:
    def isdir(self, dirname):  # type:(str)->bool
        raise NotImplementedError


class IFilesystem:
    path = None  # type: IPath

    def listdir(self, dirname):  # type:(str)->list[str]
        raise NotImplementedError
