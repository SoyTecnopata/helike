import json
import boto3

def lambda_handler(event, context):

    name = event ['interpretations'][0]['intent']['name']
    
    print (name)
    
    motivo_input = event ['sessionState']['intent']['slots']['Motivo']['value']['originalValue']
    encoded_string = motivo_input.encode("utf-8")

    bucket_name = "pulsar-reasons"
    file_name = "test.txt"

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=encoded_string)
    
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "confirmationState": "Confirmed",
                "name": "demo-welcome",
                "state": "Fulfilled",
            },
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": 'Gracias por tus comentarios',
            }
        ]
    }
    
    print('result = ' + str(response))
    
    return response
    

