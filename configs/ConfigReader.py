import json

CONFIG_PATH = "../configs/config.json"

def config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
