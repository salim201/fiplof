class IOgrResource:
    def ExecuteSQL(self, sql, flag1, flag2):  # type:(str,any,any) -> list[dict]
        raise NotImplementedError

    def Destroy(self):  # type:()->None
        raise NotImplementedError


class IOgrDriver:
    def Open(self, filename, flag1):  # type:(str,bool,bool) -> IOgrResource
        raise NotImplementedError
