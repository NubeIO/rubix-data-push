import logging
from threading import Thread
from flask import current_app

from .setting import AppSetting

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
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        from src.services.sync.postgresql import PostgreSQL
        FlaskThread(target=PostgreSQL().setup, daemon=True,
                    kwargs={'config': setting.postgres}).start()
