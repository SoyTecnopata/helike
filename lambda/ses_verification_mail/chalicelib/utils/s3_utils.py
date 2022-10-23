#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError
import os

# Get S3 client
# Boto will automaticaly close and open connection accordingly to
# the activity of the resquests.
SECRET_KEY = os.getenv('HACKATHON_SECRET_KEY')
ACCESS_KEY = os.getenv('HACKATHON_ACCESS_KEY')

S3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)


def save(data, process_name, bucket_name, key):
    """Save file in S3 bucket

        This method uses a specific boto3 client configured
        to access KPay S3 buckets with specific keys

    Args:
        data (any): the data that will be stored in s3 bucket
        process_name (String): name of the script from where the file comes
        bucket_name (String): bucket name where the data will be stored
        key (String): Directory of the bucket, ex. "dir/subdir/file.json"

    Raises:
        Exception: raised when an error occurs while saving to S3
    """
    print("Saving results from executing script: {}".format(process_name))

    try:
        S3.put_object(
            Body=data,
            Bucket=bucket_name,
            Key=key)
    except ClientError as e:
        raise Exception(e.response['Error']['Message'])


def get_key(key, bucket_name):
    """Fetch the content of the key.

    Parameters
    -----------
    key: str
        S3 key.
    bucket_name: str
        S3 bucket name.

    Returns
    --------
    obj_data: str
        The content of the key as a string.
    """

    obj = S3.get_object(Bucket=bucket_name, Key=key)

    obj_data = obj["Body"].read().decode("utf8")

    return obj_data


def bucket_folder_list_files(path, bucket_name):
    """List the content of a folder in S3.

    Given the path of a folder in the given bucket, list all
    the keys found.

    Parameters
    -----------
    path: str
    bucket_name:str

    Returns
    --------
    files_in_folder: list
    """

    # Query S3
    s3_result = S3.list_objects_v2(Bucket=bucket_name, Prefix=path)

    # Valid response includes the key 'Contents'
    if "Contents" not in s3_result:
        return []

    # Get first page of keys
    files_in_folder = [key["Key"] for key in s3_result["Contents"]]

    # If more pages available continue until the end of the list
    while s3_result["IsTruncated"]:
        continuation_key = s3_result["NextContinuationToken"]

        # Get next page of keys
        s3_result = S3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=path,
            ContinuationToken=continuation_key,
        )

        # Append keys
        files_in_folder += [key["Key"] for key in s3_result["Contents"]]

    if path in files_in_folder:
        del files_in_folder[files_in_folder.index(path)]

    return files_in_folder
