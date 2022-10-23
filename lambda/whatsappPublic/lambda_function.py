import logging
import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s: %(levelname)s: %(message)s')

sns_client = boto3.client('sns', region_name=AWS_REGION)

def lambda_handler(event, context):
    
    if (event['Records'][0]['eventName']=='INSERT'):
        
        nombre = event['Records'][0]['dynamodb']['NewImage']['nombre']['S']
        celular = event['Records'][0]['dynamodb']['NewImage']['celular']['S']
        cedula_identificacion = event['Records'][0]['dynamodb']['NewImage']['cedula_identificacion']['S']
        
        topic_arn = 'arn:aws:sns:us-east-1:751161914064:customersTopic'
        message = 'New Customer'
    
        logger.info(f'Publishing message to topic - {topic_arn}...')
        message_id = publish_message(topic_arn, message, nombre, celular, cedula_identificacion)
        logger.info(
            f'Message published to topic - {topic_arn} with message Id - {message_id}.'
        )

def publish_message(topic_arn, message, nombre, celular, cedula_identificacion):
    """
    Publishes a message to a topic.
    """
    try:

        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            MessageAttributes={
                        'cedula_identificacion': {
                            'DataType': 'String',
                            'StringValue': cedula_identificacion
                        },
                        'nombre': {
                            'DataType': 'String',
                            'StringValue': nombre
                        },
                        'celular': {
                            'DataType': 'String',
                            'StringValue': celular
                        },
                    },
        )['MessageId']

    except ClientError:
        logger.exception(f'Could not publish message to the topic.')
        raise
    else:
        return response

    

