from odoo import http
import odoo
from odoo.http import request, Response
from .Validator import validator
import simplejson as json
from tzwhere import tzwhere
from datetime import datetime, date
import pytz

return_fields = ['id', 'login', 'name', 'company_id', 'noti_token']


class JwtHttp:
    def __init__(self):
        self.tz_where = tzwhere.tzwhere()

    def get_state(self):
        return {
            'd': request.session.db
        }

    def parse_request(self):
        http_method = request.httprequest.method
        try:
            body = http.request.params
        except Exception:
            body = {}

        headers = dict(list(request.httprequest.headers.items()))
        if 'wsgi.input' in headers:
            del headers['wsgi.input']
        if 'wsgi.errors' in headers:
            del headers['wsgi.errors']
        if 'HTTP_AUTHORIZATION' in headers:
            headers['Authorization'] = headers['HTTP_AUTHORIZATION']

        # extract token
        token = ''
        if 'Authorization' in headers:
            try:
                # Bearer token_string
                token = headers['Authorization'].split(' ')[1]
            except Exception:
                pass

        return http_method, body, headers, token

    def date2str(self, d, f='%Y-%m-%d %H:%M:%S'):
        """
        Convert datetime to string
            :param self: 
            :param d: datetime object
            :param f='%Y-%m-%d%H:%M:%S': string format
        """
        try:
            s = d.strftime(f)
        except:
            s = None
        finally:
            return s

    def response(self, success=True, message=None, data=None, code=200):
        """
        Create a HTTP Response for controller 
            :param success=True indicate this response is successful or not
            :param message=None message string
            :param data=None data to return
            :param code=200 http status code
        """
        payload = json.dumps({
            'success': success,
            'message': message,
            'data': data,
        })

        return Response(payload, status=code, headers=[
            # ('Host', 'localhost:8074'),
            ('Access-Control-Allow-Headers',
             'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'OPTIONS, HEAD, GET, PUT, POST'),
            ('Access-Control-Allow-Headers', 'Authorization'),
            ('Access-Control-Allow-Credential', True),
            ('Content-Type', 'application/json'),
        ])

    def response_500(self, message='Internal Server Error', data=None):
        return self.response(success=False, message=message, data=data, code=500)

    def response_404(self, message='404 Not Found', data=None):
        return self.response(success=False, message=message, data=data, code=404)

    def response_403(self, message='403 Forbidden', data=None):
        return self.response(success=False, message=message, data=data, code=403)

    def errcode(self, code, message=None):
        return self.response(success=False, code=code, message=message)

    def do_login(self, login, password, noti_token):
        # get current db
        state = self.get_state()
        uid = request.session.authenticate(state['d'], login, password)
        user = request.env['res.users'].sudo().browse(uid)
        user.noti_token = noti_token
        if not uid:
            return self.errcode(code=400, message='incorrect login')
        # login success, generate token
        user = request.env.user.read(return_fields)[0]
        token = validator.create_token(user)
        return self.response(data={'user': user, 'token': token})


    def do_logout(self, token):
        request.session.logout()
        request.env['jwt_provider.access_token'].sudo().search([
            ('token', '=', token)
        ]).unlink()

    def cleanup(self):
        # Clean up things after success request
        # use logout here to make request as stateless as possible

        request.session.logout()

    def get_tz_where(self):
        return self.tz_where

    def current_datetime_in_float(self, lat, lon):
        timezone_str = self.tz_where.tzNameAt(float(lat), float(lon))
        # current_time_in_float 
        tz = pytz.timezone(timezone_str)
        dt_with_tz = datetime.datetime.now(tz)
        a = dt_with_tz.replace(tzinfo=None)
        current_time_in_float = (a - datetime.datetime.combine(a.date(), datetime.time())).total_seconds() / 3600
        return {'date': a.date(), 'time': current_time_in_float}


jwt_http = JwtHttp()
