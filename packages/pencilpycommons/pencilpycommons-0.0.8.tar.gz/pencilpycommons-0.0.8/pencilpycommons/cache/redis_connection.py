import logging

import redis

from pencilpycommons.cache.config import RedisConfig

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("redis")


def get_redis_connection(config: RedisConfig):
    """
    :param config:
    :return:
    """
    if config is None:
        return None

    try:
        _logger.info(f'Connecting to Redis at {config.host}')

        if not config.password:
            pool = redis.ConnectionPool(host=config.host, port=config.port, db=config.db)
        else:
            pool = redis.ConnectionPool(host=config.host, port=config.port, db=config.db, password=config.password)

        redis_connection = redis.Redis(connection_pool=pool)

        _logger.info(f'Connected to Redis')
        redis_connection.ping()
        _logger.info(f'Redis connection test successful!!!')

    except Exception as e:
        _logger.error("error connecting to redis: {}".format(str(e)), stack_info=True)
        redis_connection = None

    return redis_connection
