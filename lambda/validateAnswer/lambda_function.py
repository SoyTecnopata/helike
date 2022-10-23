import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def dispatch(event):
    print (event)
    respuesta = event ['currentIntent']['slots']['Respuesta']
    
    if respuesta=="Si" or respuesta == "1":
        print(respuesta)
        response = {
                "dialogAction": {
                    'type': 'ConfirmIntent',
                    'fulfilmentState' : 'Fulfilled',
                    'message': {
                        'contentType': 'PlainText',
                        'content': 'Gracias'
                        }
                 }
        }
    elif respuesta=="No" or respuesta == "2":
        response = {
                "dialogAction": {
                    'type': 'ConfirmIntent',
                    'intentName': 'reason',
                    'fulfilmentState' : 'Fullfiled',
                    'message': {
                        'contentType': 'PlainText',
                        'content': 'Ingresa el motivo'
                        }
                 }
        }
        
    print('result = ' + str(response))
    
    return response

def lambda_handler(event, context):

    logger.debug('event={}'.format(event))
    response = dispatch(event)
    logger.debug(response)
    return response
    

