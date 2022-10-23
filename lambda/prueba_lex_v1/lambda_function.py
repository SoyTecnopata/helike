
"""
Lexbot Lambda handler.
"""
from urllib.request import Request, urlopen
import json


    
def lambda_handler(event, context):
    print('received request: ' + str(event))


    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "Ayy Wey"
            },
            
            
        }
    }
    print('result = ' + str(response))
    return response
