import logging
from typing import List

import redis

from pencilpycommons.cache.abstract import AbstractCacheClient
from pencilpycommons.cache.config import RedisConfig

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("redis")


class RedisClient(AbstractCacheClient):

    def __init__(self, config: RedisConfig):
        if config is None:
            raise Exception("error creating redis client: invalid/null redis config")

        _logger.info(f'Connecting to Redis at {config.host}')

        if not config.password:
            pool = redis.ConnectionPool(host=config.host, port=config.port, db=config.db)
        else:
            pool = redis.ConnectionPool(host=config.host, port=config.port, db=config.db, password=config.password)

        self.__connection = redis.Redis(connection_pool=pool)

        _logger.info(f'Connecting to Redis...')
        self.__connection.ping()
        _logger.info(f'Redis connection test successful!!!')

    def get(self, key: str):
        return self.__connection.get(key)

    def set(self, key: str, value, ttl=None):
        return self.__connection.set(key, value, ttl)

    def exists(self, key: str) -> bool:
        num = self.__connection.exists(key)
        if num and num > 1:
            return True

        return False

    def delete(self, key: str):
        return self.__connection.delete(key)

    def keys(self, pattern: str) -> List[str]:
        return self.__connection.keys(pattern)

    def set_if_not_exists(self, key: str, value):
        return self.__connection.setnx(key, value)

    def set_ttl(self, key: str, ttl):
        return self.__connection.expire(key, ttl)

    def increment_value_by(self, key: str, amount: int) -> int:
        return self.__connection.incr(key, amount)

    def decrement_value_by(self, key: str, amount: int) -> int:
        return self.__connection.decr(key, amount)

    def push_to_list_head(self, key: str, *values):
        return self.__connection.lpush(key, values)

    def push_to_list_end(self, key: str, *values):
        return self.__connection.rpush(key, values)

    def pop_from_list_end(self, key: str):
        return self.__connection.rpop(key)

    def pop_from_list_head(self, key: str):
        return self.__connection.lpop(key)
