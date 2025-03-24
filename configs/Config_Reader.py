import json


class ConfigReader:
    CONFIG_PATH = "configs/config.json"

    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        with open(self.config_path, "r") as f:
            return json.load(f)

    def get_key(self, key, default=None):
        """Получить значение по ключу с явным указанием значения по умолчанию."""
        return self.config_data.get(key, default)
