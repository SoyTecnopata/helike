# Get S3 client
# Boto will automaticaly close and open connection accordingly to
# the activity of the resquests.
import os
import boto3
from botocore.exceptions import ClientError

SECRET_KEY = os.getenv('HACKATHON_SECRET_KEY')
ACCESS_KEY = os.getenv('HACKATHON_ACCESS_KEY')


def read_dynamo(table_name='', numero_cliente=0, values_to_read=['']):
    """read information from dynamo
    For more information, visit:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#table
    """
    
    numero_cliente = str(numero_cliente)
    dynamodb = boto3.resource('dynamodb'#,
                              #aws_access_key_id=ACCESS_KEY,
                              #aws_secret_access_key=SECRET_KEY,
                              #region_name="us-east-1"
                              )
    table = dynamodb.Table(table_name)
    dynamo_response = table.get_item(Key={'celular': numero_cliente},
                                     AttributesToGet=values_to_read)
    return dynamo_response['Item']


def update_dynamo(table_name='', numero_cliente='', value_to_update='', value=''):
    dynamodb = boto3.resource('dynamodb'#,
                              #aws_access_key_id=ACCESS_KEY,
                              #aws_secret_access_key=SECRET_KEY,
                              #region_name="us-east-1"
                              )
    table = dynamodb.Table(table_name)

    update_expression = "set {0} = :value".format(value_to_update)
    table.update_item(
        Key={
            'celular': str(numero_cliente)
        },
        ConditionExpression='attribute_exists(celular)',
        UpdateExpression=update_expression,

        ExpressionAttributeValues={
            ":value": value}
    )
