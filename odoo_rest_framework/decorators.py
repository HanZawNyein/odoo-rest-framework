from odoo import http
import functools
import json
from . import jwt_http, validator


def dict_body_data(**kwargs):
    try:
        raw_body_data = http.request.httprequest.data.decode('utf-8')
        if raw_body_data:
            kwargs.update(json.loads(raw_body_data.replace("'", '"')))
    except Exception as e:
        kwargs['message'] = str(e)
    finally:
        return kwargs


def login_required(route=None, **kwargs):
    def decorator(view_func):
        @functools.wraps(view_func)
        @http.route(route, **kwargs)
        def wrapper(self, **kw):
            http_method, body, headers, token = jwt_http.parse_request()
            result = validator.verify_token(token)
            if not result['status']:
                return jwt_http.errcode(code=result['code'], message=result['message'])
            kw.update(dict_body_data(**kw))
            if kw.get('message'):
                return jwt_http.errcode(code=500, message=kw['message'])
            return view_func(self, **kw)

        return wrapper

    return decorator
