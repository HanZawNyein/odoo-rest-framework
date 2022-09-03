from odoo import fields

UNNECESSARY_FIELDS = [
    'activity_ids', 'activity_state', 'activity_user_id', 'activity_type_id', 'activity_type_icon',
    'activity_date_deadline', 'my_activity_date_deadline', 'activity_summary', 'activity_exception_decoration',
    'activity_exception_icon', 'message_is_follower', 'message_follower_ids', 'message_partner_ids', 'message_ids',
    'has_message', 'message_unread', 'message_unread_counter', 'activity_type_id','active'
    'activity_date_deadline', 'activity_summary', 'activity_exception_icon', 'message_follower_ids',
    'activity_type_id', 'activity_date_deadline', 'activity_summary', 'message_attachment_count', '__last_update',
    'message_has_sms_error', 'display_name', 'message_main_attachment_id', 'create_uid', 'message_needaction',
    'message_has_error_counter', 'message_has_error', 'write_uid', 'website_message_ids', 'message_needaction_counter'
]

ODOO_DEFAULT_FIELDS = [
    fields.Char, fields.Text, fields.Selection,
    fields.Boolean,
    fields.Integer, fields.Float,
]
