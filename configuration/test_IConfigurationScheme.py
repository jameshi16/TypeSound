import unittest
from unittest.mock import MagicMock
from .IConfigurationScheme import IConfigurationScheme


class TestIConfigurationScheme(unittest.TestCase):
    def setUp(self):
        self.config_loader = MagicMock()
        self.instance = IConfigurationScheme(self.config_loader)

    def test_SaveToFile(self):
        self.instance.save_to_file('hello')
        self.config_loader.save_config_to_file.assert_called_with('hello')

    def test_SaveToString(self):
        self.instance.save_to_string()
        self.config_loader.save_config_to_string.assert_called()
