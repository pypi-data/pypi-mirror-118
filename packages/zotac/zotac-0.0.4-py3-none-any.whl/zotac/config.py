import pathlib
import os
import json

CONFIG_PATH = os.path.join(pathlib.Path(__file__).parent.resolve(), "config.json")


def get_config(func):
    def wrapper(*args, **kwargs):
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        func(*args, **kwargs, config=config)
    
    return wrapper


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
