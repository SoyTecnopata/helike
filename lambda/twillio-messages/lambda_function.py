import boto3
import urllib3
import json
import time
import random

table_name='pulsar_retargeting'
HTTP = urllib3.PoolManager()

preguntas={  "apellido_1":"primer apellido",
  "apellido_2":"segundo apellido",
  "ciudad":"Ciudad de registro",
  "c_dia":"dia de registro de tu cedula en numero",
  "c_mes":"mes de registro de tu cedula en numero",
  "c_year":"año de registro de tu cedula en numero",
  "n_dia":"dia de nacimiento en numero",
  "n_mes":"mes de nacimiento en numero",
  "n_year":"año de nacimiento en numero",
}


def update_dynamo(table_name='',celular='',value_to_update='', value=''):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    update_expression = "SET {0} = :value".format(value_to_update)
    update_response = table.update_item(
        Key={
            'celular': celular
        },
        ConditionExpression='attribute_exists(celular)',
        UpdateExpression=update_expression,

        ExpressionAttributeValues={
            ":value": value}
    )
    return update_response

def read_dynamo(table_name='',celular='',values_to_read=['']):
    celular=str(celular)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    dynamo_response = table.get_item(Key={'celular': celular},AttributesToGet=values_to_read)
    return dynamo_response['Item']



def lambda_handler(event, context):
    print(event)
    
    all_valitations=['estatus','continuar','validate_datos','validate_email','no_continuar',
    'verification_code_number','respuesta_rand','validate_cedula', 'validate_face','sent_contract','verification_code_validated']
    
    respuesta=event['Body']
    clean_from = event['From'].replace('%2B', '+').replace('%3A', ':')
    celular=clean_from.split(':')[-1]
    
    print('**********************************************',celular)
    
    valid_vals=read_dynamo(table_name,celular,all_valitations)
    
    contract_val=['continuar','validate_cedula', 'estatus','validate_datos','validate_email','validate_face']
    face_val=['continuar','validate_cedula', 'estatus','validate_datos','validate_email']
    ced_val=['estatus','continuar','validate_datos','validate_email']
    mail_val=['estatus','continuar','validate_datos']
    datos_val=['estatus','continuar']
    continuar=['estatus']
    
    valid_vals=read_dynamo(table_name,celular,all_valitations)
    print(valid_vals)
    
    bot_gen_response= "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
               "<Response><Message><Body> {mensaje} </Body></Message></Response>"
    if len(valid_vals)==len(all_valitations):
        print('finalizado')
        mensaje='tu tarjeta está en camino'
        bot_response=bot_gen_response.format(mensaje=mensaje)
        return bot_response

    elif valid_vals.get('continuar') is None:
        print('preguntar si continua')
        print('mandar mensaje de promo')
        
        time.sleep(5)
        
        mensaje='Que tal dejaste tu tramite inconcluso deseas continuar'
        bot_response=bot_gen_response.format(mensaje=mensaje)
        
        update_dynamo(table_name, celular, 'continuar', True)
        return bot_response
        
        
    elif valid_vals.get('respuesta_rand') is None:
        if str(respuesta) == 'Si':
            choice=random.choice(list(preguntas.keys()))
            pregunta_rand= 'escribe tu '+preguntas[choice]
            respuesta_rand=read_dynamo(table_name,celular,[choice])[choice]
            update_dynamo(table_name,celular,'respuesta_rand',respuesta_rand)
            mensaje='Gracias, ahora validare tu datos '+pregunta_rand
            bot_response=bot_gen_response.format(mensaje=mensaje)
            return bot_response
        else:
            mensaje='Cuentanos el motivo?'
            bot_response=bot_gen_response.format(mensaje=mensaje)
            update_dynamo(table_name,celular,'no_continuar',True)
            update_dynamo(table_name,celular,'respuesta_rand','no hay')
            return bot_response
            
    elif valid_vals.get('validate_datos') is None:
        print('respuesta datos personales')
        respuesta_valor=read_dynamo(table_name,celular,['respuesta_rand'])['respuesta_rand']
        if str(respuesta) == str(respuesta_valor):
            email=read_dynamo(table_name,celular,['email'])['email']
            ENDPOINT = "https://lmxcjhpqn3.execute-api.us-east-1.amazonaws.com/api/"
            x = {"email": email,"celular": celular}
            HTTP = urllib3.PoolManager()
            response = json.loads(
                HTTP.request(
                    "POST",
                    ENDPOINT + "send_verification_id",
                    body=json.dumps(x).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    ).data.decode("utf-8"))
        
            mensaje='Genial, te enviamos un correo al email registrado, puedes escribir los 6 digitos?'
        
            bot_response=bot_gen_response.format(mensaje=mensaje)
            
            update_dynamo(table_name, celular, 'validate_datos', True)
            return bot_response
        else:
            mensaje='respuesta incorrecta'
            bot_response=bot_gen_response.format(mensaje=mensaje)
            return bot_response


    elif valid_vals.get('verification_code_validated') is None:
        print('validar codigo')
        email=read_dynamo(table_name,celular,['email'])['email']
        

        HTTP = urllib3.PoolManager()
        ENDPOINT = "https://lmxcjhpqn3.execute-api.us-east-1.amazonaws.com/api/"
        x = {"email": email,"celular": celular, "verification_code":respuesta}
        HTTP = urllib3.PoolManager()
        response = json.loads(
            HTTP.request(
                "POST",
                ENDPOINT + "confirm_verification_id",
                body=json.dumps(x).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                ).data.decode("utf-8"))
        
        print(response)
        if response['confirmation_code_was_correct:']=='true':
            mensaje='Genial, tu correo está validado! Ahora envia una foto de tu cedula'
            
        else:
            mensaje='Codigo erroneo, vuelve a intentar'
            
        bot_response=bot_gen_response.format(mensaje=mensaje)

        return bot_response
        
        
    elif valid_vals.get('validate_cedula') is None:
        print('validar cedula')
        twilio_image=event['MediaUrl0']
        image=twilio_image.replace('%2B', '+').replace('%3A', ':').replace('%2F', '/')
        mensaje='cedula recibida, ahora tomate una selfi'
        bot_response=bot_gen_response.format(mensaje=mensaje)

        update_dynamo(table_name, celular, 'validate_cedula', True)
        return bot_response
    
    elif valid_vals.get('validate_face') is None:
        print('comparar caras')
        twilio_image=event['MediaUrl0']
        image=twilio_image.replace('%2B', '+').replace('%3A', ':').replace('%2F', '/')
        mensaje='Esa es la cara de alguien que acaba de obtener su tarjeta Aqua.\n Aqui esta tu contrato: '
        ENDPOINT = "https://863rvsbrg1.execute-api.us-east-1.amazonaws.com/api/"
        x = { "customer_id": celular}
        HTTP = urllib3.PoolManager()
        response = json.loads(HTTP.request(
                "POST",
                ENDPOINT + "write_contract",
                body=json.dumps(x).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                ).data.decode("utf-8"))
        
        contrato_url=response['url_link']
        
        mensaje= mensaje+contrato_url
        bot_response=bot_gen_response.format(mensaje=mensaje)
        update_dynamo(table_name, celular, 'validate_face', True)
        return bot_response
        
        
    elif valid_vals.get('sent_contract') is None:
        print('enviar contrato')
        mensaje='Envio de contrato'
        bot_response=bot_gen_response.format(mensaje=mensaje)
        print(bot_response)
        update_dynamo(table_name, celular, 'sent_contract', True)
        return bot_response
    elif valid_vals.get('estatus') is not None:
        update_dynamo(table_name, celular, 'estatus', 'Contactar')
        if valid_vals['estatus'] == 'Contactar':
            update_dynamo(table_name, celular, 'continuar', True)
            return bot_response

    
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
           "<Response><Message><Body>Hello world! -Lambda</Body><Media>https://demo.twilio.com/owl.png</Media></Message></Response>"

