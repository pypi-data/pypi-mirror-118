from playhouse.db_url import connect

from pencilpycommons.db.abstract import AbstractDBClient
from pencilpycommons.db.config import DBConfig


class MySQLClient(AbstractDBClient):

    def __init__(self, config: DBConfig):
        self.__config = config
        self.__connections = dict()

        if config.db_name not in self.__connections.keys():
            self.__connections[config.db_name] = self._new_connection(config.db_name)

        self.__config = config

    def get_connection(self, db_name: str, force_new=False):

        if force_new is None or force_new is False:
            if db_name not in self.__connections.keys():
                self.__connections[db_name] = self._new_connection(db_name)

            return self.__connections[db_name]

        # Use with caution. Connection obtained like this has to be closed explicitly
        return self._new_connection(db_name)

    def close_connection(self, db_name: str):

        if db_name in self.__connections.keys():
            self.__connections[db_name].close()
            self.__connections[db_name] = None

    def _new_connection(self, db_name: str):
        config = self.__config

        database_url = "mysql://{}:{}@{}:{}/{}". \
            format(config.username, config.password, config.host, config.port, db_name)

        connection_params = {'charset': 'utf8', 'use_unicode': True}

        return connect(database_url, **connection_params)
