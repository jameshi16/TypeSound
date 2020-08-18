# IConfigurationScheme.py - Abstraction layer on top of configuration loader
from .IConfiguration import IConfiguration


class IConfigurationScheme:
    def __init__(self, config_loader: IConfiguration, *args, **kwargs):
        self._config_loader = config_loader
        super(IConfigurationScheme, self).__init__(*args, **kwargs)

    def save_to_file(self, path: str):
        return self._config_loader.save_config_to_file(path)

    def save_to_string(self) -> str:
        return self._config_loader.save_config_to_string()
