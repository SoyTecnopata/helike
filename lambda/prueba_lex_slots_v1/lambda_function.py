

import json

def lambda_handler(event, context):
    print('received request: ' + str(event))
    name = event['currentIntent']['slots']['Name']
    print(name)
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "Hola " + name
            },
        }
    }
    print('result = ' + str(response))
    return response
