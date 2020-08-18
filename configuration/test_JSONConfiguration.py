import unittest
from unittest.mock import patch
from .JSONConfiguration import JSONConfiguration
from .IConfiguration import ConfigurationNoVersion, ConfigurationNotLoaded


class TestJSONConfiguration(unittest.TestCase):
    def setUp(self):
        self.instance = JSONConfiguration()

    def test_GetVersion(self):
        self.instance._loaded = True
        self.instance._loaded_obj = {
            'version': 1
        }

        self.assertEqual(self.instance.get_version(), 1)

        self.instance._loaded = False
        self.instance._loaded_obj = {}
        with self.assertRaises(ConfigurationNotLoaded):
            self.instance.get_version()

    @patch('json.load')
    @patch('builtins.open')
    def test_LoadConfigFromFile(self, open_mock, json_load_mock):
        json_load_mock.return_value = {
            'version': 1
        }

        self.instance.load_config_from_file('does not matter')
        json_load_mock.assert_called()
        open_mock.assert_called()
        self.assertEqual(
            self.instance._loaded_obj,
            json_load_mock.return_value
        )
        self.assertEqual(self.instance._loaded, True)

        json_load_mock.return_value = {}
        with self.assertRaises(ConfigurationNoVersion):
            self.instance.load_config_from_file('does not matter')

    def test_LoadConfigFromString(self):
        config = '{"version": 1}'
        self.instance.load_config_from_string(config)
        self.assertEqual(self.instance._loaded_obj, {'version': 1})

        with self.assertRaises(ConfigurationNoVersion):
            self.instance.load_config_from_string('{}')

    @patch('json.dump')
    @patch('builtins.open')
    def test_SaveConfigToFile(self, open_mock, json_dump_mock):
        self.instance._loaded_obj = {'version': 1}
        self.instance.save_config_to_file('does not matter')

        open_mock.assert_called()
        json_dump_mock.assert_called_with(
            self.instance._loaded_obj,
            unittest.mock.ANY
        )

    def test_SaveConfigToString(self):
        self.instance._loaded_obj = {'version': 1}
        rtn = self.instance.save_config_to_string()

        self.assertEqual(rtn, '{\"version\": 1}')
