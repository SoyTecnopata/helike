#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib3

import unittest


HTTP = urllib3.PoolManager()

#ENDPOINT = "http://127.0.0.1:8000/"
ENDPOINT = "https://lmxcjhpqn3.execute-api.us-east-1.amazonaws.com/api/"


class TestVersion(unittest.TestCase):

    def test_get_link(self):
        """ """
        response = HTTP.request(
                "GET",
                ENDPOINT,
            ).data.decode("utf-8")

        # model versions
        ok_value = 'Hello from the hackaton ses test'

        self.assertEqual(response == ok_value, True)

    def test_sending_verification_code(self):
        """ """

        x = {
            "email": "samorogu@gmail.com",
            "celular": "+525551871818"
        }

        response = json.loads(
            HTTP.request(
                "POST",
                ENDPOINT + "send_verification_id",
                body=json.dumps(x).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            ).data.decode("utf-8")
        )
        if 'succesfully' in response.keys():
            res = 1

        response["mail sent succesfully to: "]

        # service model versions
        email_response = response["mail sent succesfully to: "]

        # model versions
        ok_value = "samorogu@gmail.com"

        self.assertEqual(email_response == ok_value, True)


def test_confirm_verification_code(self):
    """ """

    x = {
        "email": "samorogu@gmail.com",
        "celular": "+525551871818",
        "verification_code": 440431
    }

    response = json.loads(
        HTTP.request(
            "POST",
            ENDPOINT + "confirm_verification_id",
            body=json.dumps(x).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        ).data.decode("utf-8")
    )

    # service model versions
    email_response = response["customer_id"]

    # model versions
    ok_value = "a0001"

    self.assertEqual(email_response == ok_value, True)


if __name__ == "__main__":
    unittest.main()
