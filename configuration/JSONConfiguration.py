from .IConfiguration import IConfiguration
from .IConfiguration import ConfigurationNoVersion
import json


class JSONConfiguration(IConfiguration):
    """Generic JSON configuration loader"""
    def __init__(self, *args, **kwargs):
        super(JSONConfiguration, self).__init__(*args, **kwargs)

    def get_version(self):
        self._loaded_or_raise()
        return self._loaded_obj['version']

    def load_config_from_file(self, path: str):
        with open(path, mode='r') as config_file:
            loaded_obj = json.load(config_file)
            if 'version' not in loaded_obj:
                raise ConfigurationNoVersion

            self._loaded_obj = loaded_obj
            self._loaded = True

    def load_config_from_string(self, string: str):
        loaded_obj = json.loads(string)
        if 'version' not in loaded_obj:
            raise ConfigurationNoVersion

        self._loaded_obj = loaded_obj
        self._loaded = True

    def save_config_to_file(self, path: str):
        with open(path, mode='w') as config_file:
            json.dump(self._loaded_obj, config_file)

    def save_config_to_string(self):
        return json.dumps(self._loaded_obj)
