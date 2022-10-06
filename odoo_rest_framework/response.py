import json
from odoo.http import request

HEADERS = [
    ('Content-Type', 'application/json'),
    ('Cache-Control', 'no-store'),
    ('Access-Control-Allow-Origin', '*'),
    ('Access-Control-Allow-Methods', 'GET, POST')
]

DATA = {'success': True, 'message': '' or None, 'data': list or None}


def response_json(success: bool = True, data: None or list = None, *, message=None):
    return request.make_response(json.dumps({"success": success, "data": data, "message": message}), HEADERS)
