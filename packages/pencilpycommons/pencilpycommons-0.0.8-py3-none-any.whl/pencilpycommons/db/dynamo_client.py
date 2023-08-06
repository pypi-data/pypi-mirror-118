from boto3.dynamodb.conditions import Key, Attr

from pencilpycommons.db.abstract import AbstractDocumentDBClient


class DynamoDBClient(AbstractDocumentDBClient):

    def __init__(self, dynamo_resource):
        self.__resource = dynamo_resource

    def query_using_index(self, table_name: str, index_name: str, value):
        table = self.__resource.Table(table_name)
        response = table.query(IndexName=index_name, KeyConditionExpression=Key(index_name).eq(value))

        if not response or "Items" not in response:
            return list()

        return response["Items"]

    def query_with_attribute(self, table_name: str, attr_name: str, value):
        table = self.__resource.Table(table_name)
        response = table.scan(FilterExpression=Attr(attr_name).eq(value))

        if not response or "Items" not in response:
            return list()

        return response["Items"]

    def query_using_attribute_and_operator(self, table_name: str, attr_name: str, operator: str, value):
        table = self.__resource.Table(table_name)
        response = None

        if operator == '>':
            response = table.scan(FilterExpression=Attr(attr_name).gt(value))
        elif operator == '<':
            response = table.scan(FilterExpression=Attr(attr_name).lt(value))
        elif operator == '>=':
            response = table.scan(FilterExpression=Attr(attr_name).gte(value))
        elif operator == '<=':
            response = table.scan(FilterExpression=Attr(attr_name).lte(value))

        if not response or "Items" not in response:
            return list()

        return response["Items"]
