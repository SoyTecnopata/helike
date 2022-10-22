import json
import os
import boto3
from collections import defaultdict


# Get environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_KEY = os.getenv('ACCESS_KEY')
table_name='pulsar_retargeting'
event={
   "Records":[
      {
         "eventVersion":"2.1",
         "eventSource":"aws:s3",
         "awsRegion":"us-east-1",
         "eventTime":"2022-10-22T17:03:51.024Z",
         "eventName":"ObjectCreated:Put",
         "userIdentity":{
            "principalId":"A16VN5XLMYTM84"
         },
         "requestParameters":{
            "sourceIPAddress":"173.244.55.44"
         },
         "responseElements":{
            "x-amz-request-id":"4XTP03RQAGSEZ3HN",
            "x-amz-id-2":"DEA4UKYNIqpAT1H4K+jjFDhhxkVq5TxzQTsbUmyaMSvGysnyeghepc4HlaR/omfRscV+qgl0+QnsOvPZB/l78ZgdbrAitKSC"
         },
         "s3":{
            "s3SchemaVersion":"1.0",
            "configurationId":"a2f51d91-6467-490e-a076-a2752e529f33",
            "bucket":{
               "name":"pulsar-data-collector",
               "ownerIdentity":{
                  "principalId":"A16VN5XLMYTM84"
               },
               "arn":"arn:aws:s3:::pulsar-data-collector"
            },
            "object":{
               "key":"53038780/imagenes_recibidas/DU_y4GcX0AAKvGc.jpg",
               "size":587621,
               "eTag":"ec08eb6cdf405536eaecad54db7af189",
               "sequencer":"0063542276EFF35FFE"
            }
         }
      }
   ]
}

def is_a_cedula(bucket='',image=''):
    rekognition_client = boto3.client("rekognition",
                                      aws_access_key_id=ACCESS_KEY,
                                      aws_secret_access_key=SECRET_KEY,
                                      region_name="us-east-1"
                                      )
    nedeed_labels = ['Text', 'Person', 'Id Cards']
    labels_response = rekognition_client.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": image}})
    labels_found=[]
    for label in labels_response['Labels']:
        if label['Confidence']>=80:
            labels_found.append(label['Name'])

    return all(item in labels_found for item in nedeed_labels)

def update_dynamo(table_name='',cedula_identificacion='',value_to_update='', value=''):
    dynamodb = boto3.resource('dynamodb',
                                      aws_access_key_id=ACCESS_KEY,
                                      aws_secret_access_key=SECRET_KEY,
                                      region_name="us-east-1"
                                      )
    table = dynamodb.Table(table_name)

    update_expression = "SET {0} = :value".format(value_to_update)
    update_response = table.update_item(
        Key={
            'cedula_identificacion': cedula_identificacion
        },
        ConditionExpression='attribute_exists(cedula_identificacion)',
        UpdateExpression=update_expression,

        ExpressionAttributeValues={
            ":value": value}
    )

def read_dynamo(table_name='',cedula_identificacion=0,values_to_read=['']):
    cedula_identificacion=str(cedula_identificacion)
    dynamodb = boto3.resource('dynamodb',
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name="us-east-1"
                              )
    table = dynamodb.Table(table_name)
    dynamo_response = table.get_item(Key={'cedula_identificacion': cedula_identificacion},
                              AttributesToGet=values_to_read)
    return dynamo_response['Item']

def validate_cedula(bucket,image, cedula_identificacion):
    textract_client = boto3.client('textract',
                                      aws_access_key_id=ACCESS_KEY,
                                      aws_secret_access_key=SECRET_KEY,
                                      region_name="us-east-1"
                                      )
    id_response = textract_client.analyze_id( DocumentPages=[{"S3Object": {"Bucket": bucket, "Name": image}}])
    output_dict = defaultdict(dict)

    for field in id_response['IdentityDocuments'][0]['IdentityDocumentFields']:
        output_dict[field['Type']['Text']][field['ValueDetection']['Text']] = field['ValueDetection']['Confidence']

    if 'DOCUMENT_NUMBER' in output_dict.keys():
        cedula_ocr=list(output_dict['DOCUMENT_NUMBER'].keys())[0]
        confidence_ocr=list(output_dict['DOCUMENT_NUMBER'].values())[0]
        if confidence_ocr > 80:
            return int(cedula_identificacion) == int(cedula_ocr)
    return False



def lambda_handler(event, context=None):

    bucket = event['Records'][0]['s3']['bucket']['name']
    image = event['Records'][0]['s3']['object']['key']
    image_keys=image.split('/')
    cedula_identificacion=image_keys[0]
    filename=image_keys[-1]
    file_extention=filename.split('.')[-1]
    s3 = boto3.client('s3',aws_access_key_id=ACCESS_KEY,
                                      aws_secret_access_key=SECRET_KEY,
                                      region_name="us-east-1")

    if is_a_cedula(bucket,image):
        print('this is a valid cedula')
        valid_cedula_path='cedula_validada'
        valid_cedula_name=cedula_identificacion+'_cedula.'+file_extention
        valid_cedula_key= cedula_identificacion+'/'+valid_cedula_path+'/'+valid_cedula_name
        if validate_cedula(bucket,image,cedula_identificacion):
            update_dynamo(table_name, cedula_identificacion, 'validate_cedula', True)
            s3.copy({"Bucket": bucket, "Key": image}, bucket, valid_cedula_key)



if __name__ == '__main__':
    lambda_handler(event)
