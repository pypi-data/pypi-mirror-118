class DBConfig:

    def __init__(self, host: str, port: int, username: str, password: str, db_name: str):
        """
        :param host:
        :param port:
        :param db:
        :param password:
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_name = db_name
