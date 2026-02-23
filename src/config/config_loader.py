import yaml
import os

CONFIG_PATH = os.getenv("TEST_CONFIG", "config/config.yaml")


def load_config():

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


config = load_config()