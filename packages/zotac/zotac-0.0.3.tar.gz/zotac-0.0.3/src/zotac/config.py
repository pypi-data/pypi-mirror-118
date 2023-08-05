import pathlib
import os
import json

CONFIG_PATH = os.path.join(pathlib.Path(__file__).parent.resolve(), "config.json")


def get_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
