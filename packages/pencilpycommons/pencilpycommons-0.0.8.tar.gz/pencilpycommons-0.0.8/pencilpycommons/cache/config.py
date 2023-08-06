_DEFAULT_REDIS_PORT = 6379
_DEFAULT_REDIS_DB = 0


class RedisConfig:
    def __init__(self, host: str, port=_DEFAULT_REDIS_PORT, db=_DEFAULT_REDIS_DB, password=None):
        """
        :param host:
        :param port:
        :param db:
        :param password:
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
