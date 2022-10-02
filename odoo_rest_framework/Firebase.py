import json

from requests.structures import CaseInsensitiveDict
from requests import post


def send_notifications(title:str, body:str, token:str, server_key:str)->object:
    url = "https://fcm.googleapis.com/fcm/send"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = server_key
    headers["Content-Type"] = "application/json"
    data = {
        'to': token,
        'notification': {
            'title': title,
            'body': body
        }
    }
    resp = post(url, headers=headers, data=json.dumps(data))
    return resp