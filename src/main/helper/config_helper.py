import os
import json
import logging


class ConfigHelper:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_key(key):
        config_path = os.path.join(
            os.path.dirname(__file__), "../../tests/config/config.json"
        )
        print(f"Looking for config file at: {os.path.abspath(config_path)}")
        api_key = None
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    api_key = config.get(key)
            except json.JSONDecodeError:
                ConfigHelper.logger.error(f"Error parsing {config_path}")
        if not api_key:
            api_key = os.getenv(key)

        assert api_key, f"Key {key} not found in config.json or environment variables"
        return api_key
