### Odoo REST Framework

    Version : 1.1.3

### Package :

    pip install odoo-rest-framework

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

# Controller Code Example

    from odoo import http
    from .odoo_rest_framework import (
        login_required,
        jwt_http,
        fields_extractor,
        read_serializer
    )
    from odoo.http import request


    class Testing(http.Controller):
        @login_required(route='/api/testing/', csrf=False, methods=['GET'])
        def testing(self, limit=5, offset=1, *args, **kwargs):
            model_res_partner = request.env['res.partner']
            # all_fields = fields_extractor(model_res_partner)
            all_partner = model_res_partner.search_read([], fields=['id','name'], limit=limit, offset=offset)
            all_partner = read_serializer(all_partner)
            return jwt_http.response(data=all_partner, message='Holidays')


# Response Example
    {
        "success": true,
        "message": "Holidays",
        "data": [
            {
                "id": 37,
                "name": "Brandon Freeman"
            },
            {
                "id": 44,
                "name": "Colleen Diaz"
            }
        ]
    }