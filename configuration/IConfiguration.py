# IConfiguration.py - Base class for all configuration derivatives

class ConfigurationNotLoaded(Exception):
    """Configuration hasn't loaded, but an attribute is being read"""
    pass


class ConfigurationNoVersion(Exception):
    """Configuration doesn't have a version in its schema"""
    pass


class ConfigurationVersionMismatch(Exception):
    """Wrong class is being used for configuration version"""
    pass


class IConfiguration:
    def __init__(self, *args, **kwargs):
        self._loaded = False
        self._loaded_obj = {}
        super(IConfiguration, self).__init__(*args, **kwargs)

    def _loaded_or_raise(self):
        if not self._loaded:
            raise ConfigurationNotLoaded

    def get_version(self) -> int:
        raise NotImplementedError

    def load_config_from_file(self, path: str):
        raise NotImplementedError

    def load_config_from_string(self, string: str):
        raise NotImplementedError

    def save_config_to_file(self, path: str):
        raise NotImplementedError

    def save_config_to_string(self) -> str:
        raise NotImplementedError

    @property
    def loaded_data(self):
        self._loaded_or_raise()
        return self._loaded_obj
