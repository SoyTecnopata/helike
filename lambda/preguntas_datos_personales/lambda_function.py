# import json

# def lambda_handler(event, context):
#     print(event)
#     # TODO implement
#     response = {
#         "sessionState": {
#             "dialogAction": {
#                 "type": "Close"
#             },
#             "intent": {
#                 "confirmationState": "Confirmed",
#                 "name": "Inicio",
#                 "state": "Fulfilled",
#             },
    
#         },
#         "messages": [
#             {
#                 "contentType": "PlainText",
#                 "content": 'Weeeeeey ya',
#             }
#         ]
#     }
    
#     return response

"""
Lexbot Lambda handler.
"""
from urllib.request import Request, urlopen
import json
    
def lambda_handler(event, context):
    print('received request: ' + str(event))
    # date_input = event['currentIntent']['Fecha']
    slots = event['currentIntent']['slots']
    print(slots)
    
    fecha = event['currentIntent']['Fecha']
    print(fecha)
    
    print(str(date_input))
    
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": str(date_input)
            },
        }
    }
    print('result = ' + str(response))
    return response
