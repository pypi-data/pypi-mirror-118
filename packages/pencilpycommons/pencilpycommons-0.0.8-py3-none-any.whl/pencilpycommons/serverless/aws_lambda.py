import json
import logging
import traceback

from pencilpycommons.serverless.abstract import AbstractServerlessManager
from pencilpycommons.serverless.exceptions import ServerlessFunctionInvocationException, \
    ServerlessFunctionResponseException

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("aws")


class AWSLambdaManager(AbstractServerlessManager):

    def __init__(self, lambda_client):
        self.__lambda_client = lambda_client

    def invoke_function(self, function_path: str, payload: dict) -> dict:
        try:
            response = self.__lambda_client.invoke(
                FunctionName=function_path,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload)
            )
        except Exception as e:
            _logger.warning(e, exc_info=True)

            raise ServerlessFunctionInvocationException(
                "error invoking function {}: {}".format(function_path, traceback.format_exc()))

        try:
            payload = response['Payload'].read().decode("utf-8")
        except Exception as e:
            _logger.warning(e, exc_info=True)

            raise ServerlessFunctionResponseException(
                "error parsing response from function {}: {}".format(function_path, traceback.format_exc()))

        return json.loads(payload)
