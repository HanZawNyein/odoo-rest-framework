### Odoo REST Framework

    Version : 1.0.6

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

    from odoo_rest_framework import (
        jwt_http,
        validator,
        util,
        status,
        fields_extractor,
        format_dict_one2many,
        format_dict_many2one,
        serializer,
        send_notifications
    )
    

    market_review = request.env['market.review'].search(search_query)
    data = serializer(market_review)
    return jwt_http.response(success=True, message='Success', data=data)

### Response Example

    {
    "success": true,
    "message": "Success",
    "data": [
        {
            "id":1,
            "create_date": "2022-08-22 04:32:06",
            "write_date": "2022-08-23 07:56:15",
            "year": "2022",
            "total_broker": 100,
            "product_id": {"id": 22, "name": "product"},
            "prospect_condition_lines": [
                {
                    "id": 1,
                    "status": "inquiry",
                    "model_id": {"id": 1, "name": "Test Model"},
                    "create_date": "2022-08-10 07:10:50",
                    "write_date": "2022-08-12 07:11:00",
                    "product_id": {"id": 1, "name": "product"},
                    "branch_id": {"id": 1, "name": "Test Brand"},
                    "holding_id": {"id": 6, "name": "Bago"},
                    "qty": 8,
                    "way_plan_id": {"id": 1, "name": "Monthly Way Plan for February(Bago)"},
                    "market_review_id": null
                },
                {
                    "id": 2,
                    "status": "inquiry",
                    "model_id": {"id": 1, "name": "Test Model"},
                    "create_date": "2022-08-22 04:32:06",
                    "write_date": "2022-08-23 07:56:15",
                    "product_id": {"id": 1, "name": "product"},
                    "branch_id": {"id": 1, "name": "Test Brand"},
                    "holding_id": {"id": 6, "name": "Bago"},
                    "qty": 0,
                    "way_plan_id": null,
                    "market_review_id": null
                }
            ],
            "date": "2022-09-02",
            "feedback_type": "normal",
            "feedback": "this is Feedback"
            }
        ]
    }
