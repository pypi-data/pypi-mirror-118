class ServerlessFunctionInvocationException(Exception):

    def __init__(self, message):
        super().__init__(message)


class ServerlessFunctionResponseException(Exception):

    def __init__(self, message):
        super().__init__(message)
