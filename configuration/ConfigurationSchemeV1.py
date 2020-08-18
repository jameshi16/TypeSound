from .IConfigurationScheme import IConfigurationScheme
from .IConfiguration import IConfiguration


class ConfigurationSchemeV1(IConfigurationScheme):
    def __init__(self, config_loader: IConfiguration, *args, **kwargs):
        super(ConfigurationSchemeV1, self).__init__(
            config_loader, *args, **kwargs)

    @property
    def cap_kps(self):
        if 'cap_kps' not in self._config_loader.loaded_data:
            return 9.0
        return self._config_loader.loaded_data['cap_kps']

    @cap_kps.setter
    def cap_kps(self, value):
        self._config_loader.loaded_data['cap_kps'] = value

    @property
    def path_to_dir(self):
        if 'path_to_dir' not in self._config_loader.loaded_data:
            return '/tmp'
        return self._config_loader.loaded_data['path_to_dir']

    @path_to_dir.setter
    def path_to_dir(self, value):
        self._config_loader.loaded_data['path_to_dir'] = value

    @property
    def increase_rate(self):
        if 'increase_rate' not in self._config_loader.loaded_data:
            return 0.01
        return self._config_loader.loaded_data['increase_rate']

    @increase_rate.setter
    def increase_rate(self, value):
        self._config_loader.loaded_data['increase_rate'] = value

    @property
    def decay_rate(self):
        if 'decay_rate' not in self._config_loader.loaded_data:
            return 0.1
        return self._config_loader.loaded_data['decay_rate']

    @decay_rate.setter
    def decay_rate(self, value):
        self._config_loader.loaded_data['decay_rate'] = value
