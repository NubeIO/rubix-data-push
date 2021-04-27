from flask import Blueprint
from flask_restful import Api
from src.resources.ping import Ping


bp_system = Blueprint('system', __name__, url_prefix='/api/system')
Api(bp_system).add_resource(Ping, '/ping')
