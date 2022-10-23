#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib3

import unittest


HTTP = urllib3.PoolManager()

#ENDPOINT = "http://127.0.0.1:8000/"
ENDPOINT = "https://863rvsbrg1.execute-api.us-east-1.amazonaws.com/api/"


class TestVersion(unittest.TestCase):

    def test_get_link(self):
        """ """
        response = HTTP.request(
                "GET",
                ENDPOINT,
            ).data.decode("utf-8")

        # model versions
        ok_value = 'Hello from the hackaton contract test'

        self.assertEqual(response == ok_value, True)
    def test_write_contract(self):
        """ """

        x = {
            "customer_id": '+525551871818'
        }

        response = json.loads(
            HTTP.request(
                "POST",
                ENDPOINT + "write_contract",
                body=json.dumps(x).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            ).data.decode("utf-8")
        )

        # service model versions
        customer_id = response["write_customer_data_contract"]

        # model versions
        ok_value = '+525551871818'

        self.assertEqual(customer_id == ok_value, True)
