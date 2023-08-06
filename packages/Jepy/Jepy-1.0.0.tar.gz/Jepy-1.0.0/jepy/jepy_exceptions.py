class ArgumentError(ValueError):
    def __init__(self,*args,**kwargs):
        ValueError.__init__(self,*args,**kwargs)

class ServerError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
