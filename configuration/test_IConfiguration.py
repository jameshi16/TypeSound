import unittest
from .IConfiguration import IConfiguration, ConfigurationNotLoaded


class TestIConfiguration(unittest.TestCase):
    def setUp(self):
        self.instance = IConfiguration()

    def test_LoadedOrRaise(self):
        self.instance._loaded = False
        with self.assertRaises(ConfigurationNotLoaded):
            self.instance._loaded_or_raise()

        self.instance._loaded = True
        self.instance._loaded_or_raise()
        self.instance._loaded = False

    def test_Unimplemented(self):
        with self.assertRaises(NotImplementedError):
            self.instance.get_version()
            self.instance.load_config_from_file('no matter')
            self.instance.load_config_from_string('no matter')
            self.instance.save_config_to_file('no matter')
            self.instance.save_config_to_string()

    def test_LoadedData(self):
        self.instance._loaded = False
        with self.assertRaises(ConfigurationNotLoaded):
            self.instance.loaded_data

        self.instance._loaded = True
        self.assertEqual(self.instance.loaded_data, {})
        self.instance._loaded = False
