import json


class Config:

    @classmethod
    def load(cls):
        with open('../out/config/config.json', 'r') as f:
            config = json.load(f)
        return config.get('mqtt')


class AppSetting(Config):
    PORT = 19191

    def __init__(self):
        self.config = Config.load()
        self.__port = self.config.get('enabled') or AppSetting.PORT

    @property
    def port(self):
        return self.__port


me = AppSetting()
print(me.port)
