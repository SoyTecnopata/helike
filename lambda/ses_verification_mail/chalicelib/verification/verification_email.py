#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from chalicelib.utils import s3_utils, dynamo_utils, utils
from chalicelib.data import config
import time
import json
import boto3

import urllib3

HTTP = urllib3.PoolManager()

#ENDPOINT = "http://127.0.0.1:8000/"
ENDPOINT = "https://lmxcjhpqn3.execute-api.us-east-1.amazonaws.com/api/"

client = boto3.client("ses")

table_name = 'pulsar_retargeting'

def save_image_in_s3(link='https://api.twilio.com/2010-04-01/Accounts/ACee59125c4a3673329f0c63e3c7d547b2/Messages/MM8c68454724675d0b3e58d0e2cc1e5bc3/Media/ME549529890fd647b8c52e8ff6f351e48c'):
    
    import os
    
    SECRET_KEY = os.getenv('HACKATHON_SECRET_KEY')
    ACCESS_KEY = os.getenv('HACKATHON_ACCESS_KEY')

    S3 = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)

    customer_number = '+5551871818'

    index_s3_file = "customers"+\
        str(customer_number)+"/contracts/index.html"

    response = HTTP.request(
                "GET",
                link,
            ).data

    S3.put_object(
            Body=response,
            Bucket='hackaton-bbva-testing-lambda-ses',
            Key=index_s3_file,
            ContentType='text/html')

    return "success"

def send_verif_code(email, customer_phone):
    """Sent verification id to email
    and save it on s3 in the customer path in s3
    with the verification code """
    verification_code = utils.random_with_N_digits(6)
    subject = 'Verificación del correo electrónico para tu tarjeta'
    body = """
                 <br>
                 Gracias por iniciar el proceso de tu tarjeta. 
                 <br>
                 Queremos asegurarnos de que es realmente usted. 
                 <br>
                 Ingrese el siguiente código de verificación en Whatsapp. 
                 Código de verificación:
                 <br>
                 {}.
         """.format(verification_code)

    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
    client.send_email(Source="hackathonhelike@gmail.com",
                      Destination={"ToAddresses": [email]}, Message=message)
    print("The mail is sent successfully")

    verification_s3_file = config.S3_CUSTOMER_VERIFICATION_FILEPATH +\
        "/"+customer_phone+"/verification_codes/verification_code.json"

    actual_time = time.time()

    verification_cust = {}

    verification_cust['customer_phone'] = customer_phone
    verification_cust['created_at'] = actual_time
    verification_cust['verification_code'] = verification_code

    print("verification code saved in :"+verification_s3_file)

    json_verification_cust = json.dumps(verification_cust)

    #s3_utils.save(json_verification_cust,
    #              "Writing customer_id verification code",
    #              config.DEV_BUCKET,
    #              verification_s3_file
    #              )
    dynamo_utils.update_dynamo(
        table_name=table_name,
        numero_cliente=customer_phone,
        value_to_update='verification_code_sent',
        value=True
    )

    dynamo_utils.update_dynamo(
        table_name=table_name,
        numero_cliente=customer_phone,
        value_to_update='verification_code_number',
        value=verification_code
    )

    dynamo_utils.update_dynamo(
        table_name=table_name,
        numero_cliente=customer_phone,
        value_to_update='verification_code_created_at',
        value=str(actual_time)
    )

    return {"mail sent succesfully to: ": email}


def confirmation_verif_code(customer_phone, verification_code, time_limit=10.0):
    """Review if verification code is 
    correct with a time limit of n minutes"""

    verification_code = verification_code

    #verification_s3_file = config.S3_CUSTOMER_VERIFICATION_FILEPATH +\
    #    "/"+customer_phone+"/verification_codes/verification_code.json"

    bucket = config.DEV_BUCKET

    # let's read the file
    #verification_file = s3_utils.get_key(key=verification_s3_file,
    #                                     bucket_name=bucket)

    verification_dict = dynamo_utils.read_dynamo(
        table_name=table_name,
        numero_cliente=customer_phone,
        values_to_read=['verification_code_number','verification_code_created_at'])

    actual_time = time.time()

    true_confirmation_code = verification_dict["verification_code_number"]
    confirmation_code_time = float(verification_dict["verification_code_created_at"])

    print("previous_time  "+str(confirmation_code_time))
    print("current_time "+str(actual_time))

    elapsed_time = round((actual_time - confirmation_code_time) / 60, 2)

    if (
        (str(verification_code) == str(true_confirmation_code))
            & (float(elapsed_time) < float(time_limit))
    ):
        res = "true"

        dynamo_utils.update_dynamo(
        table_name=table_name,
        numero_cliente=customer_phone,
        value_to_update='verification_code_validated',
        value=True
    )
    else:
        res = "false"

        dynamo_utils.update_dynamo(
        table_name=table_name,
        numero_cliente=customer_phone,
        value_to_update='verification_code_validated',
        value=False
    )

    return {"customer_phone": customer_phone,
            "true confirmation code :": str(true_confirmation_code),
            "sent confirmation code :": str(verification_code),
            "confirmation_code_was_correct:": res,
            "elapsed_time:": elapsed_time,
            }
