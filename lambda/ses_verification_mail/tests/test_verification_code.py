#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib3

import unittest


HTTP = urllib3.PoolManager()

#ENDPOINT = "http://127.0.0.1:8000/"
ENDPOINT = "https://lmxcjhpqn3.execute-api.us-east-1.amazonaws.com/api/"


class TestVersion(unittest.TestCase):
    def test_sending_verification_code(self):
        """ """

        x = {
            "email": "hackathonhelike@gmail.com",
            "customer_id": "a0000"
        }

        x = {
            "email": "samorogu@gmail.com",
            "customer_id": "a0001"
        }

        x = {
            "email": "jimenasantiago.b@gmail.com"
        }

        x = {
            "email": "emmanuelfhorn@gmail.com",
            "customer_id": "a0002"
        }

        x = {
            "email": "r.j.m.suastegui@gmail.com",
            "customer_id": "a0003"
        }

        response = json.loads(
            HTTP.request(
                "POST",
                ENDPOINT + "send_verification_id",
                body=json.dumps(x).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            ).data.decode("utf-8")
        )

        # service model versions
        email_response = response["mail sent succesfully to: "]

        # model versions
        ok_value = "hackathonhelike@gmail.com"

        self.assertEqual(email_response == ok_value, True)


def test_confirm_verification_code(self):
    """ """

    x = {
        "email": "samorogu@gmail.com",
        "customer_id": "a0001",
        "verification_code": 104097
    }

    x = {
            "email": "r.j.m.suastegui@gmail.com",
            "customer_id": "a0003",
            "verification_code": 875835
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
