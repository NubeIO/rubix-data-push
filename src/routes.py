from flask import Blueprint
from flask_restful import Api

from src.resources.device.device_plural import DevicePlural
from src.resources.device.device_singular import DeviceSingularByName, DeviceSingularByUUID
from src.resources.mapping.mapping import LPGBPMappingResourceList, LPGBPMappingResourceByLoRaPointUUID, \
    LPGBPMappingResourceByGenericPointUUID, LPGBPMappingResourceByBACnetPointUUID, LPGBPMappingResourceByUUID
from src.resources.network.network import SerialDriver
from src.resources.ping import Ping
from src.resources.point.point import PointsSingularByName, PointsSingularByUUID, PointsPlural
from src.resources.point.sync import LPToBPSync, LPToGPSync

bp_lora = Blueprint('lora', __name__, url_prefix='/api/lora')
api_lora = Api(bp_lora)
api_lora.add_resource(SerialDriver, '/networks')
api_lora.add_resource(DevicePlural, '/devices')
api_lora.add_resource(PointsPlural, '/points')
api_lora.add_resource(DeviceSingularByUUID, '/devices/uuid/<string:value>')
api_lora.add_resource(DeviceSingularByName, '/devices/name/<string:value>')
api_lora.add_resource(PointsSingularByUUID, '/points/uuid/<string:uuid>')
api_lora.add_resource(PointsSingularByName, '/points/name/<string:device_name>/<string:point_name>')

# lora to generic/bacnet points mappings
bp_mapping_lp_gbp = Blueprint('mappings_lp_gbp', __name__, url_prefix='/api/mappings/lp_gbp')
api_mapping_lp_gbp = Api(bp_mapping_lp_gbp)
api_mapping_lp_gbp.add_resource(LPGBPMappingResourceList, '')
api_mapping_lp_gbp.add_resource(LPGBPMappingResourceByUUID, '/uuid/<string:uuid>')
api_mapping_lp_gbp.add_resource(LPGBPMappingResourceByLoRaPointUUID, '/lora/<string:uuid>')
api_mapping_lp_gbp.add_resource(LPGBPMappingResourceByGenericPointUUID, '/generic/<string:uuid>')
api_mapping_lp_gbp.add_resource(LPGBPMappingResourceByBACnetPointUUID, '/bacnet/<string:uuid>')

bp_sync = Blueprint('sync', __name__, url_prefix='/api/sync')
api_sync = Api(bp_sync)
api_sync.add_resource(LPToGPSync, '/lp_to_gp')
api_sync.add_resource(LPToBPSync, '/lp_to_bp')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
Api(bp_system).add_resource(Ping, '/ping')
