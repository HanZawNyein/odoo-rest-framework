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

    def get_leave_list(self, leave_type, report_id, related_hr_id):
        http_method, body, headers, token = JwtHttp.parse_request()
        result = validator.verify_token(token)
        if not result['status']:
            return JwtHttp.errcode(code=result['code'], message=result['message'])

        # DOMAIN
        domain = []
        date = datetime.now().strftime('%Y-%m-%d')
        fiscal_id = request.env['hr.fiscal.year'].sudo().search(
            [('date_from', '<=', date), ('date_to', '>=', date), ('active', '=', True)])
        if not fiscal_id:
            date_from = date
            date_to = date
        else:
            date_from = fiscal_id[0].date_from
            date_to = fiscal_id[0].date_to

        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])

        if leave_type == 'All' and report_id == 0 and related_hr_id == 0:
            domain = [('request_date_to', '>=', date_from), ('request_date_to', '<=', date_to)]

        elif leave_type != 'All' and report_id == 0 and related_hr_id == 0:
            domain = [('request_date_to', '>=', date_from), ('request_date_to', '<=', date_to),
                      ('holiday_status_id.name', '=', leave_type)]

        elif leave_type == 'All' and report_id != 0 and related_hr_id == 0:
            domain = [('request_date_to', '>=', date_from), ('request_date_to', '<=', date_to),
                      ('report_id', '=', report_id)]

        else:
            domain = [('request_date_to', '>=', date_from), ('request_date_to', '<=', date_to),
                      ('related_hr_id', '=', related_hr_id)]

        fields = [
            'department_id', 'holiday_type', 'holiday_status_id', 'employee_id', 'related_hr_id', 'report_id',
            'charge_id',
            'name', 'request_date_from', 'request_date_to', 'duration_display', 'state', 'payslip_status', 'attach'
        ]
        data = request.env['hr.leave'].sudo().search_read(domain, fields=fields)
        for i in data:
            i['request_date_from'] = str(i.get('request_date_from'))
            i['request_date_to'] = str(i.get('request_date_to'))
        return JwtHttp.response(data=data, message="Leave Details")

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
