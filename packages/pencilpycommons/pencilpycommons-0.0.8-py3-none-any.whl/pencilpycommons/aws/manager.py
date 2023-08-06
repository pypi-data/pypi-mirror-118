import logging

import boto3

from pencilpycommons.aws.resource import ResourceType

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("aws")


class AWSManager(object):
    __shared_state = dict()
    __aws_inited = False

    def __init__(self, access_key: str, secret_key: str, region: str, in_lambda=False):
        self.__dict__ = self.__shared_state

        if self.__aws_inited is False:
            self.__aws_inited = True
            _logger.info('Loading AWS session')
            self.__session = self.__get_session()
            _logger.info('Loading AWS session done')

        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__region = region
        self.__in_lambda = in_lambda

    def __get_session(self):
        if self.__in_lambda:
            _logger.info('IN_LAMBDA')
            session = boto3.Session()
            return session

        return boto3.Session(region_name=self.__region,
                             aws_access_key_id=self.__access_key,
                             aws_secret_access_key=self.__secret_key)

    def clear_session(self):
        _logger.info('Clearing AWS session')
        self.__aws_inited = False
        self.__session = None

    def get_session(self):
        if self.__session is None:
            self.__session = self.__get_session()

        return self.__session

    def get_client(self, resource_type: ResourceType):
        if resource_type is None:
            return None

        return self.get_session().client(resource_type.value)

    def get_resource(self, resource_type: ResourceType):
        if resource_type is None:
            return None

        return self.get_session().resource(resource_type.value)
