from enum import Enum


class ResourceType(Enum):
    S3 = "s3"
    Lambda = "lambda"
    DynamoDB = "dynamodb"
