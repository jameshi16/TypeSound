import unittest
from .ConfigurationSchemeV1 import ConfigurationSchemeV1
from .IConfiguration import IConfiguration


class FakeConfiguration(IConfiguration):
    """Need to use a FakeConfiguration because
    we are directly modifying _loaded_obj"""
    def __init__(self, *args, **kwargs):
        super(FakeConfiguration, self).__init__(*args, **kwargs)
        self._loaded = True
        self._loaded_obj = {}


class TestConfigurationSchemeV1(unittest.TestCase):
    def setUp(self):
        self.config_loader = FakeConfiguration()
        self.instance = ConfigurationSchemeV1(self.config_loader)

    def test_Defaults(self):
        self.config_loader._loaded_obj = {}
        self.assertEqual(self.instance.cap_kps, 9.0)
        self.assertEqual(self.instance.path_to_dir, '/tmp')
        self.assertEqual(self.instance.increase_rate, 0.01)
        self.assertEqual(self.instance.decay_rate, 0.1)

    def test_Set(self):
        self.config_loader._loaded_obj = {}
        self.instance.cap_kps = 1.0
        self.instance.path_to_dir = 'no matter'
        self.instance.increase_rate = 2.0
        self.instance.decay_rate = 3.0

        self.assertEqual(self.instance.cap_kps, 1.0)
        self.assertEqual(self.instance.path_to_dir, 'no matter')
        self.assertEqual(self.instance.increase_rate, 2.0)
        self.assertEqual(self.instance.decay_rate, 3.0)

    def test_Preset(self):
        self.config_loader._loaded_obj = {
            'version': 1,
            'cap_kps': 3.0,
            'path_to_dir': 'matter not',
            'increase_rate': 2.0,
            'decay_rate': 1.0
        }

        self.assertEqual(self.instance.cap_kps, 3.0)
        self.assertEqual(self.instance.path_to_dir, 'matter not')
        self.assertEqual(self.instance.increase_rate, 2.0)
        self.assertEqual(self.instance.decay_rate, 1.0)
