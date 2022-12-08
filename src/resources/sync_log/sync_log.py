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
        pushed_global_uuids = []
        logs = PostgersSyncLogModel.find_all()
        default_case = dict(global_uuid=None, latest_sync_id=None, latest_sync_datetime=None, max_sync_id=None)
        try:
            rows = PostgreSQL().get_postgres_sync_rows_details()
        except Exception:
            raise PreConditionException("Unable to connect PostgreSQL")
        for log in logs:
            row = next((v for i, v in enumerate(rows) if v['global_uuid'] == log.global_uuid), default_case)
            log_dict = log.to_dict()
            last_sync_datetime_to_envizi = get_not_none_datetime_value(log_dict)
            log = {**log_dict,
                   'last_sync_datetime_to_envizi': last_sync_datetime_to_envizi,
                   'latest_sync_id_in_postgres': row['latest_sync_id'],
                   'latest_sync_datetime_in_postgres': row['latest_sync_datetime'],
                   'max_sync_id_in_postgres': row['max_sync_id'],
                   'has_envizi_record': True,
                   'has_postgres_record': row['global_uuid'] is not None,
                   }
            logs_details.append(log)
            pushed_global_uuids.append(log_dict['global_uuid'])
        for row in rows:
            # include those lists which is on Postgres but yet to be pushed to Envizi
            if row['global_uuid'] not in pushed_global_uuids:
                logs_details.append({
                    'global_uuid': row['global_uuid'],
                    'last_sync_id_to_envizi': None,
                    'last_sync_datetime_to_envizi': None,
                    'latest_sync_id_in_postgres': row['latest_sync_id'],
                    'latest_sync_datetime_in_postgres': row['latest_sync_datetime'],
                    'max_sync_id_in_postgres': row['max_sync_id'],
                    'has_envizi_record': False,
                    'has_postgres_record': True,
                })
        return logs_details


class SyncLogByGlobalUUID(RubixResource):
    @classmethod
    @marshal_with(sync_log_details_fields)
    def get(cls, global_uuid):
        log: PostgersSyncLogModel = PostgersSyncLogModel.find_by_global_uuid(global_uuid)
        try:
            row = PostgreSQL().get_postgres_sync_row_details(global_uuid)
        except Exception:
            raise PreConditionException("Unable to connect PostgreSQL")
        if log:
            log_dict = log.to_dict()
            last_sync_datetime_to_envizi = get_not_none_datetime_value(log_dict)

            return {**log_dict,
                    'last_sync_datetime_to_envizi': last_sync_datetime_to_envizi,
                    'latest_sync_id_in_postgres': row[1],
                    'latest_sync_datetime_in_postgres': row[2],
                    'max_sync_id_in_postgres': row[3],
                    'has_envizi_record': True,
                    'has_postgres_record': row[0] is not None,
                    }
        elif row[0]:
            return {
                'global_uuid': row[0],
                'last_sync_id_to_envizi': None,
                'last_sync_datetime_to_envizi': None,
                'latest_sync_id_in_postgres': row[1],
                'latest_sync_datetime_in_postgres': row[2],
                'max_sync_id_in_postgres': row[3],
                'has_envizi_record': False,
                'has_postgres_record': True,
            }
        raise NotFoundException(f"not found {global_uuid}")

    @classmethod
    @marshal_with(sync_log_fields)
    def patch(cls, global_uuid: str):
        parser_patch = reqparse.RequestParser()
        parser_patch.add_argument('last_sync_id_to_envizi', type=int, required=True)
        data = parser_patch.parse_args()
        sync_log: PostgersSyncLogModel = PostgersSyncLogModel.find_by_global_uuid(global_uuid)
        if sync_log is None:
            raise NotFoundException(f"Sync log not found")
        sync_log.last_sync_id_to_envizi = data.get('last_sync_id_to_envizi', 0)
        sync_log.update_last_sync_id_to_envizi()
        return sync_log

    @classmethod
    @marshal_with(sync_log_fields)
    def delete(cls, global_uuid: str):
        sync_log: PostgersSyncLogModel = PostgersSyncLogModel.find_by_global_uuid(global_uuid)
        if sync_log is not None:
            sync_log.delete_from_db()
        PostgreSQL().delete_postgres_data(global_uuid)
        return '', 204


def get_not_none_datetime_value(log_dict):
    last_sync_datetime_to_envizi = log_dict.get('last_sync_datetime_to_envizi')
    last_sync_datetime_to_envizi = None if last_sync_datetime_to_envizi == "None" else last_sync_datetime_to_envizi
    return last_sync_datetime_to_envizi
