from flask import Blueprint
from flask_restful import Api
from src.resources.ping import Ping
from src.resources.sync_log.sync_log import SyncLog, SyncLogByGlobalUUID

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
Api(bp_system).add_resource(Ping, '/ping')

bp_sync_logs = Blueprint('sync_logs', __name__, url_prefix='/api/sync_logs')
api_sync_logs = Api(bp_sync_logs)
api_sync_logs.add_resource(SyncLog, '')
api_sync_logs.add_resource(SyncLogByGlobalUUID, '/global_uuid/<string:global_uuid>')
