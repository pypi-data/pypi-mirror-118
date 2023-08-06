import datetime
import json

import requests


def handle_response(response):
    """
    Handles Responses From the JengaHQ API and Raises Exceptions appropriately
    as errors occur and returns a `dict` object from the `json` response
    """
    try:
        resp = response.json()
        if resp.get("error"):
            raise requests.exceptions.RequestException(
                resp["code"] + " : " + resp["message"]
            )
        else:
            return response.json()
    except json.decoder.JSONDecodeError as e:
        raise ("An error occurred decoding the JSON response" + str(e))


def generate_reference() -> str:
    """
    Generate a transaction reference
    Should always be a 12 digit String
    """

    a = datetime.datetime.now()
    ref = "".join(str(a).replace(" ", "").replace("-", "").split(":")[0:2])
    return ref
