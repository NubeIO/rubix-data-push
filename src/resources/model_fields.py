from flask_restful import fields

sync_log_fields = {
    'global_uuid': fields.String,
    'last_sync_id': fields.Integer
}

sync_log_details_fields = {
    **sync_log_fields,
    'max_sync_id': fields.Integer
}
