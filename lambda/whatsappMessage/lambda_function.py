from twilio.rest import Client
import boto3

def lambda_handler(event=None, context=None):

    twilio_sid = ''
    auth_token = ''

    from_number = 'whatsapp:' '+14155238886'
    
    nombre=event['Records'][0]['Sns']['MessageAttributes']['nombre']['Value']
    celular=event['Records'][0]['Sns']['MessageAttributes']['celular']['Value']
    cedula_identificacion=event['Records'][0]['Sns']['MessageAttributes']['cedula_identificacion']['Value']

    whatsapp_client = Client(twilio_sid, auth_token)
    
    send_message_result = whatsapp_client.messages.create(
            body = 'Que tal {}, dejaste tu trámite inconcluso, ¿deseas continuar? 1.Si, 2.No'.format(nombre),
            from_= from_number,
            to='whatsapp:' + celular,

        )
    
    print(send_message_result)
    print(send_message_result.sid)
    
    updateDynamo(send_message_result.sid, celular)
    
def updateDynamo(sid, celular):
    
    dynamodb = boto3.client('dynamodb')
    
    response=dynamodb.update_item(TableName='pulsar_retargeting', 
                                    Key={
                                        'celular': {
                                            'S': celular 
                                        }
                                    },
                                    UpdateExpression='SET sid= :var1',
                                    ExpressionAttributeValues= {
                                            ':var1': {
                                                "S": sid 
                                                }
                                            },
                                    ReturnValues='UPDATED_NEW')
    
    print(response)
