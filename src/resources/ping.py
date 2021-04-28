import time
from datetime import datetime
from flask import current_app
from rubix_http.resource import RubixResource
from src.pyinstaller import resource_path
from src.utils.project import get_version

startTime = time.time()
up_time_date = str(datetime.now())

try:
    with open(resource_path('VERSION')) as version_file:
        version = version_file.read().strip()
except FileNotFoundError:
    version = 'Fake'


def get_up_time():
    """
    Returns the number of seconds since the program started.
    """
    return time.time() - startTime


class Ping(RubixResource):
    @classmethod
    def get(cls):
        up_time = get_up_time()
        up_min = up_time / 60
        up_min = round(up_min, 2)
        up_min = str(up_min)
        up_hour = up_time / 3600
        up_hour = round(up_hour, 2)
        up_hour = str(up_hour)
        # from src import AppSetting
        # setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        return {
            'version': get_version(),
            'up_time_date': up_time_date,
            'up_min': up_min,
            'up_hour': up_hour,
            # 'serial': {
            #     'enabled': setting.mqtt.enabled,
            #     'status': "ADD SOMINT HERE"
            # },
            # 'mqtt': {
            #     'enabled': setting.mqtt.enabled,
            #     'status': MqttClient().status()
            # }
        }
