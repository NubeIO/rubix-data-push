from flask_restful import fields

sync_log_fields = {
    'global_uuid': fields.String,
    'last_sync_id_to_envizi': fields.Integer,
    'last_sync_datetime_to_envizi': fields.String
}

sync_log_details_fields = {
    **sync_log_fields,
    'latest_sync_id_in_postgres': fields.Integer,
    'latest_sync_datetime_in_postgres': fields.String,
    'max_sync_id_in_postgres': fields.Integer,
    'has_envizi_record': fields.Boolean,
    'has_postgres_record': fields.Boolean,
}
