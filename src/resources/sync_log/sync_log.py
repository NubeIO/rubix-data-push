from flask_restful import marshal_with, reqparse
from rubix_http.exceptions.exception import NotFoundException, PreConditionException
from rubix_http.resource import RubixResource

from src import PostgersSyncLogModel
from src.resources.model_fields import sync_log_fields, sync_log_details_fields
from src.services.sync.postgresql import PostgreSQL


class SyncLog(RubixResource):
    @classmethod
    @marshal_with(sync_log_details_fields)
    def get(cls):
        logs_details = []
        logs = PostgersSyncLogModel.find_all()
        for log in logs:
            try:
                max_sync_id = PostgreSQL().get_point_value_max_sync_id(log.global_uuid)
            except Exception:
                raise PreConditionException("Unable to connect PostgreSQL")
            logs_details.append({**log.to_dict(), 'max_sync_id': max_sync_id})
        return logs_details


class SyncLogByGlobalUUID(RubixResource):
    @classmethod
    @marshal_with(sync_log_details_fields)
    def get(cls, global_uuid):
        log: PostgersSyncLogModel = PostgersSyncLogModel.find_by_global_uuid(global_uuid)
        try:
            max_sync_id = PostgreSQL().get_point_value_max_sync_id(global_uuid)
        except Exception:
            raise PreConditionException("Unable to connect PostgreSQL")
        return {**log.to_dict(), 'max_sync_id': max_sync_id}

    @classmethod
    @marshal_with(sync_log_fields)
    def patch(cls, global_uuid: str):
        parser_patch = reqparse.RequestParser()
        parser_patch.add_argument('last_sync_id', type=int, required=True)
        data = parser_patch.parse_args()
        sync_log: PostgersSyncLogModel = PostgersSyncLogModel.find_by_global_uuid(global_uuid)
        if sync_log is None:
            raise NotFoundException(f"Sync log not found")
        sync_log.last_sync_id = data.get('last_sync_id', 0)
        sync_log.update_last_sync_id()
        return sync_log
