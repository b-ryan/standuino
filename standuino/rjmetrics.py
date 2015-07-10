import requests
import json
import os


def send_state(state):
    apikey = os.environ["RJMETRICS_APIKEY"]
    host = os.environ["RJMETRICS_HOST"]

    url = "{}/v2/client/8/table/test_standing/data".format(host)

    payload = state.json()
    payload["keys"] = ["id"]

    params = {
        "apikey": apikey,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    requests.post(url, data=json.dumps(payload), params=params,
                  headers=headers)
