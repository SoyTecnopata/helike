import json
import os
import boto3

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

def lambda_handler(event, context):
response = dispatch(event)   
return response 

def dispatch(intent_request):    
intent_name = intent_request['sessionState']['intent']['name']    
response = None        

session_attributes = get_session_attributes(intent_request)    print(intent_request['sessionState'])                

# Distribuir según sea el intent requerido 
if intent_name == 'ClasesRecomendadas':        
return ClasesRecomendadas(intent_request)    

 raise Exception('Intent with name ' + intent_name + ' not supported') 
 
 
def GuardarRespuesta(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)

    #Reemplazar el valor de la región por la usada
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://dynamodb.REGION.amazonaws.com")

  
    #Busqueda de la tabla 
    table = dynamodb.Table('retargeting_helike')

   

    #Extracción de identificación del estudiante

    idestudiante = get_slot(intent_request, 'Continuar')

   

    #Composición del mensaje para el usuario final
    text = "Data Guardada"


    message =  {

            'contentType': 'PlainText',

            'content': text

        }

    fulfillment_state = "Fulfilled"   

    return close(intent_request, session_attributes, fulfillment_state, message)
