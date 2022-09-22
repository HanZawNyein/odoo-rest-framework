### Odoo REST Framework

    Version : 1.1.1

### Package :

    pip install odoo_rest_framework

###### package link :

    https://pypi.org/project/odoo-rest-framework/

###### github link :

    https://github.com/HanZawNyein/odoo-rest-framework.git

###### Author :

    Han Zaw Nyein

###### Author_email:

    hanzawnyineonline@gmail.com

### Description :

    Store user access token for one-time-login

### Code Example
import json
from odoo import http
from odoo.http import request
from .odoo_rest_framework import (
    jwt_http,
    validator,
    util,
    create_serializer,
    read_serializer,
    fields_extractor,
    update_serializer,
    send_notifications,
)


class Testing(http.Controller):
    @http.route('/api/testing/list')
    def testing_list(self, *args, **kwargs):
        http_method, body, headers, token = jwt_http.parse_request()
        result = validator.verify_token(token)
        if not result['status']:
            return jwt_http.errcode(code=result['code'], message=result['message'])
        model_obj = request.env['market.review']
        all_fields = fields_extractor(model_object=model_obj)
        market_review_ids = model_obj.sudo().search_read([], fields=all_fields)
        value_object = read_serializer(value_object=market_review_ids)
        return jwt_http.response(success=True, data=value_object)

    @http.route('/api/testing/create', type='http', auth='public', csrf=False, cors='*', methods=['POST'])
    def testing_create(self, *args: dict, **kwargs: dict):
        http_method, body, headers, token = jwt_http.parse_request()
        result = validator.verify_token(token)
        if not result['status']:
            return jwt_http.errcode(code=result['code'], message=result['message'])

        raw_body_data = request.httprequest.data
        my_json = raw_body_data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        data['prospect_condition_lines'] = create_serializer(data['prospect_condition_lines'])
        model_obj = request.env['market.review']
        market_review_id = model_obj.create(data)
        return jwt_http.response(data={'id': market_review_id.id})

    @http.route('/api/testing/update', type='http', auth='public', csrf=False, cors='*')
    def testing_update(self, *args, **kwargs):
        http_method, body, headers, token = jwt_http.parse_request()
        result = validator.verify_token(token)
        if not result['status']:
            return jwt_http.errcode(code=result['code'], message=result['message'])

        raw_body_data = request.httprequest.data
        my_json = raw_body_data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        model_obj = request.env['market.review'].browse(data.get('id'))  # .search([('id', '=', data.get('id'))])
        try:
            if model_obj.create_date:
                data['prospect_condition_lines'] = update_serializer(data['prospect_condition_lines'])
                data.pop('id')
                model_obj.create(data)
        except Exception as e:
            return jwt_http.response(success=False, message=str(e))

### Response Example

{
    "success": true,
    "message": null,
    "data": [
        {
            "id": 54,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                52
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        },
        {
            "id": 55,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                53
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        },
        {
            "id": 56,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                54
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        },
        {
            "id": 57,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                55
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        },
        {
            "id": 58,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                56
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        },
        {
            "id": 59,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                57
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        },
        {
            "id": 60,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                58
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        },
        {
            "id": 61,
            "name": "Market Review for February 2022",
            "month": "2",
            "year": "2022",
            "division_id": {
                "id": 1,
                "name": "Yangon"
            },
            "date": "2022-09-02",
            "total_broker": 100,
            "feedback": "dsfsdf",
            "feedback_type": "normal",
            "action_plan_feedback": "dsf",
            "action_plan_market": "fsdf",
            "market_condition_lines": null,
            "mio_condition_lines": null,
            "focus_bu_id": {
                "id": 10,
                "name": "Gyobinkauk"
            },
            "focus_segment_id": {
                "id": 1,
                "name": "Motor"
            },
            "prospect_condition_lines": [
                59
            ],
            "competitor_information_lines": null,
            "state": "draft",
            "reject_reason": null,
            "create_date": "2022-09-23",
            "write_date": "2022-09-23"
        }
    ]
}