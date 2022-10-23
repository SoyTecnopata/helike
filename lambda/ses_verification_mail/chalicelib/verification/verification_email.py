#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from chalicelib.utils import s3_utils, utils
from chalicelib.data import config
import time
import json
import boto3

client = boto3.client("ses")


def send_verif_code(email, customer_id):
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
        "/"+customer_id+"/verification_codes/verification_code.json"

    actual_time = time.time()

    verification_cust = {}

    verification_cust['customer_id'] = customer_id
    verification_cust['created_at'] = actual_time
    verification_cust['verification_code'] = verification_code

    print("verification code saved in :"+verification_s3_file)

    json_verification_cust = json.dumps(verification_cust)

    s3_utils.save(json_verification_cust,
                  "Writing customer_id verification code",
                  config.DEV_BUCKET,
                  verification_s3_file
                  )
    return {"mail sent succesfully to: ": email}


def confirmation_verif_code(customer_id, verification_code, time_limit=5.0):
    """Review if verification code is 
    correct with a time limit of n minutes"""

    verification_code = verification_code

    verification_s3_file = config.S3_CUSTOMER_VERIFICATION_FILEPATH +\
        "/"+customer_id+"/verification_codes/verification_code.json"

    bucket = config.DEV_BUCKET

    # let's read the file
    verification_file = s3_utils.get_key(key=verification_s3_file,
                                         bucket_name=bucket)

    verification_dict = json.loads(verification_file)

    actual_time = time.time()

    true_confirmation_code = verification_dict["verification_code"]
    confirmation_code_time = verification_dict["created_at"]

    print("previous_time  "+str(confirmation_code_time))
    print("current_time "+str(actual_time))

    elapsed_time = round((actual_time - confirmation_code_time) / 60, 2)

    if (
        (verification_code == true_confirmation_code)
            & (float(elapsed_time) < float(time_limit))
    ):
        res = "true"
    else:
        res = "false"

    return {"customer_id": customer_id,
            "true confirmation code :": true_confirmation_code,
            "sent confirmation code :": verification_code,
            "confirmation_code_was_correct:": res,
            "elapsed_time:": elapsed_time,
            }
