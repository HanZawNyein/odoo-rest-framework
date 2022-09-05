import datetime

import odoo
from . import status

fields_extractor = lambda model_name, unwanted_fields: list(set(model_name._fields.keys()) - set(unwanted_fields))
format_dict_many2one = lambda value_object: {'id':value_object.id or None,'name':value_object.name or None}


def serializer(value_object: str) -> dict:
    all_fields = fields_extractor(model_name=value_object, unwanted_fields=status.UNNECESSARY_FIELDS)
    result = []
    for value in value_object:
        one_record_result = {}
        for f in all_fields:
            if isinstance(value._fields[f], odoo.fields.Date):
                one_record_result[f] = odoo.fields.Date.to_string(value[f]) or None
            elif isinstance(value._fields[f], odoo.fields.Datetime):
                one_record_result[f] = odoo.fields.Datetime.to_string(value[f]) or None
            elif isinstance(value._fields[f], odoo.fields.Many2one):
                one_record_result[f] = format_dict_many2one(value_object=value[f]) or None
            elif isinstance(value._fields[f], odoo.fields.One2many):
                one_record_result[f] = format_dict_one2many(value_object=value[f]) or None
            elif isinstance(value._fields[f], odoo.fields.Integer):
                one_record_result[f] = value[f] or 0
            elif isinstance(value._fields[f], odoo.fields.Float):
                one_record_result[f] = value[f] or 0.0
            elif isinstance(value._fields[f], odoo.fields.Boolean):
                one_record_result[f] = value[f] or False
            else:
                one_record_result[f] = value[f] or None
        result.append(one_record_result)
        # print(len(one_record_result))
    return result


def format_dict_one2many(value_object:object)->list:
        all_fields = fields_extractor(model_name=value_object, unwanted_fields=status.UNNECESSARY_FIELDS)
        result = []
        for value in value_object:
            one_record_result = {}
            for f in all_fields:
                if isinstance(value._fields[f], odoo.fields.Date):
                    one_record_result[f] = odoo.fields.Date.to_string(value[f]) or None
                elif isinstance(value._fields[f], odoo.fields.Datetime):
                    one_record_result[f] = odoo.fields.Datetime.to_string(value[f]) or None
                elif isinstance(value._fields[f], odoo.fields.Many2one):
                    one_record_result[f] = format_dict_many2one(value_object=value[f]) or None
                elif isinstance(value._fields[f], odoo.fields.Integer):
                    one_record_result[f] = value[f] or 0
                elif isinstance(value._fields[f], odoo.fields.Float):
                    one_record_result[f] = value[f] or 0.0
                elif isinstance(value._fields[f], odoo.fields.Boolean):
                    one_record_result[f] = value[f] or False
                else:
                    one_record_result[f] = value[f] or None
            result.append(one_record_result)
        return result
