import pygsheets
import pandas as pd
import awswrangler as wr

import datetime
import json
import sys
import os
import boto3

s3client = boto3.client('s3')
filename = os.path.join('/tmp', 'creds.json')
s3Test = s3client.download_file('glue-assets-bucket', 'credentials/creds.json', filename)


# Get the credentials. (The mail within this file should have viewer access to the file you want to reach)"""
gc = pygsheets.authorize(service_file=os.path.join('/tmp', 'creds.json'))

control_sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1w0sTtmPwJeLG0n4N3ZoIToVQA7tjfJiN3q9MKyzq_HY/edit?usp=sharing')
values_to_extract = control_sheet.worksheet('title', 'Test').get_all_records()
df =pd.DataFrame(values_to_extract)
df = df.loc[df['estatus'] == "Contactar"]
print(df)
try:
    wr.s3.to_parquet(
        df,
        path="s3://google-sheets-input/input/clients_to_contact.parquet",
        index=False)
except:
  print("No new rows to be written")


print("Done")
