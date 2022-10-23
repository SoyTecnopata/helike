#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime

# AWS Keys for BUCKETS
DEV_BUCKET = 'hackaton-bbva-testing-lambda-ses'

CUSTOMERS_PATH = 'customers'
VERIFICATION_PATH = 'verification_codes'

S3_CUSTOMER_VERIFICATION_FILEPATH = '{}'.format(CUSTOMERS_PATH)
