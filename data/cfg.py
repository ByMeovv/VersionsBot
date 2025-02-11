import yaml
from typing import Any
import os


class Config:
    """
    Loads configuration values from a YAML file.

    The configuration values are loaded from the 'data.yaml' file and accessed through Config class methods.
    """

    _instance = None

    def __new__(cls, config_path: str = "config.yaml"):
        """
        Returns a singleton instance of the Config class.

        This method is used to ensure that only one instance of the Config class
        is created, and that all other requests for an instance of the class
        return the same instance. The instance is created the first time the
        method is called, and the same instance is returned on subsequent calls.

        The method takes an optional parameter, config_path, which is used to
        specify the path to the configuration file. If not provided, the method
        will use the default value of "data.yaml".

        :param config_path: The path to the configuration file.
        :type config_path: str
        :return: A singleton instance of the Config class.
        :rtype: Config
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Get absolute path to the data file relative to this module
            base_dir = os.path.dirname(os.path.abspath(__file__))
            cls._instance.config_path = os.path.join(base_dir, config_path)
            cls._instance._config = cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> dict:
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_value(key: str) -> Any:
        return Config()._config.get(key)