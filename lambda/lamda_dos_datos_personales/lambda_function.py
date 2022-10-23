import json

def lambda_handler(event, context):
    print(event)
    # TODO implement
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "confirmationState": "Confirmed",
                "name": "parte_2",
                "state": "Fulfilled",
            },
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": 'oooooooooooootra respuesta',
            }
        ]
    }
    
    return response
