import logging
import jwt
import re
import datetime
import traceback
import os
from odoo import http, service, registry, SUPERUSER_ID
from odoo.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

regex = r"^[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


class Validator:
    def is_valid_email(self, email):
        return re.search(regex, email)

    def key(self):
        # return os.environ.get('ODOO_JWT_KEY')
        ICPSudo = request.env['ir.config_parameter'].sudo()
        return ICPSudo.get_param('jwt_secret_key')

    def create_token(self, user):
        try:
            ICPSudo = request.env['ir.config_parameter'].sudo()
            exp_day = ICPSudo.get_param("access_token_expires_in")
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=float(exp_day))
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': user['id'],
                'lgn': user['login'],
            }

            token = jwt.encode(
                payload,
                self.key(),
                algorithm=ICPSudo.get_param('jwt_algorithm')
            )

            self.save_token(token, user['id'], exp)

            # return token.decode('utf-8')
            return token
        except Exception as ex:
            _logger.error(ex)
            raise

    def save_token(self, token, uid, exp):
        request.env['jwt_provider.access_token'].sudo().create({
            'user_id': uid,
            'expires': exp.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'token': token,
        })

    def verify(self, token):
        record = request.env['jwt_provider.access_token'].sudo().search([
            ('token', '=', token)
        ])

        if len(record) != 1:
            _logger.info('not found %s' % token)
            return False

        if record.is_expired:
            return False

        return record.user_id

    def verify_token(self, token):
        try:
            result = {
                'status': False,
                'message': None,
            }
            payload = jwt.decode(token, self.key(), algorithms='HS256')
            
            if not self.verify(token):
                result['message'] = 'Token invalid or expired'
                result['code'] = 498
                _logger.info('11111')
                return result
            uid = request.session.authenticate(
                request.session.db, login=payload['lgn'], password=token)
            if not uid:
                result['message'] = 'Token invalid or expired'
                result['code'] = 498
                _logger.info('2222')
                return result

            result['status'] = True
            return result
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
            result['code'] = 498
            result['message'] = 'Token invalid or expired'
            _logger.error(traceback.format_exc())
            return result


validator = Validator()