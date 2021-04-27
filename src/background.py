import logging
from threading import Thread

from flask import current_app


logger = logging.getLogger(__name__)


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


# TODO: Should refactor to stop when receive exit code
class Background:
    @staticmethod
    def run():
        # from src.lora import SerialConnectionListener
        # from src.mqtt import MqttClient
        # setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        # logger.info("Running Background Task...")
        # if setting.mqtt.enabled:
        #     MqttClient().start(setting.mqtt)



        Background.sync_on_start()



    @staticmethod
    def sync_on_start():
        print("sync_on_start")
        # from .models.model_point_store import PointStoreModel
        # """Sync mapped points values from LoRa > Generic | BACnet points values"""
        # PointStoreModel.sync_points_values_lp_to_gbp_process()
