import datetime

import odoo

UNNECESSARY_FIELDS = [
    'activity_ids', 'activity_state', 'activity_user_id', 'activity_type_id', 'activity_type_icon',
    'activity_date_deadline', 'my_activity_date_deadline', 'activity_summary', 'activity_exception_decoration',
    'activity_exception_icon', 'message_is_follower', 'message_follower_ids', 'message_partner_ids', 'message_ids',
    'has_message', 'message_unread', 'message_unread_counter', 'active''activity_date_deadline',
    'activity_summary', 'activity_exception_icon', 'message_follower_ids', 'activity_date_deadline',
    'activity_summary', 'message_attachment_count', '__last_update', 'message_has_sms_error', 'display_name',
    'message_main_attachment_id', 'create_uid', 'message_needaction', 'message_has_error_counter', 'message_has_error',
    'write_uid', 'website_message_ids', 'message_needaction_counter'
]


def fields_extractor(model_object: list, remove_fields=None):
    if remove_fields is None:
        remove_fields = UNNECESSARY_FIELDS
    result = []
    for a in list(model_object._fields.keys()):
        if not a in remove_fields:
            result.append(a)
    return result


create_serializer = lambda value_object: base_serializer(first_value=0, second_value=0, data=value_object)


def update_serializer(value_object):
    result = []
    for v in value_object:
        if v.get('id'):
            __id = v.get('id')
            v.pop('id')
            result.append((1, __id, v))
        else:
            result.append((0, 0, v))
    return result


def base_serializer(first_value, second_value, data: list):
    result = []
    for d in data:
        result.append((first_value, second_value, d))
    return result


def read_serializer(value_object):
    result = []
    for value in value_object:
        one_record = {}
        for v in list(value.keys()):
            if isinstance(value[v], datetime.date):
                one_record[v] = datetime_toString(value[v]) or None
            elif isinstance(value[v], datetime.datetime):
                one_record[v] = odoo.fields.Datetime.to_string(value[v]) or None
            elif isinstance(value[v], tuple):
                one_record[v] = {'id': value[v][0], 'name': value[v][1]} or None
            else:
                one_record[v] = value[v] or None
        result.append(one_record)
    return result


def datetime_toString(date_object):
        return odoo.fields.Date.to_string(date_object).astimezone(pytz.timezone(request.env.user.tz or pytz.utc))
