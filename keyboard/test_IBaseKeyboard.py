import unittest
import time
from unittest.mock import MagicMock, patch
from .IBaseKeyboard import IBaseKeyboard


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class TestIBaseKeyboard(unittest.TestCase):
    def setUp(self):
        self.ibasekeyboard = IBaseKeyboard()

    def test_IncreaseRate(self):
        self.ibasekeyboard.increase_rate = 1.0
        self.assertEqual(self.ibasekeyboard.increase_rate, 1.0)
        self.ibasekeyboard.increase_rate = 0.01

    def test_DecayRate(self):
        self.ibasekeyboard.decay_rate = 0.5
        self.assertEqual(self.ibasekeyboard.decay_rate, 0.5)
        self.ibasekeyboard.decay_rate = 0.1

    def test_KPS(self):
        self.ibasekeyboard._kps = 1.0
        self.assertEqual(self.ibasekeyboard.kps, 1.0)
        self.ibasekeyboard._kps = 0

    @patch('asyncio.sleep', new_callable=AsyncMock)
    def test_KPSAfterOneSecond(self, time_sleep_patched):
        # callback down doesn't execute if kps is less than 0
        self.ibasekeyboard._kps = 0.1

        self.ibasekeyboard.increase_rate = 1.0
        self.ibasekeyboard.decay_rate = 0.0
        self.ibasekeyboard._buffer_kps = 100
        self.ibasekeyboard._start_kps_change()
        time.sleep(0.1)
        self.ibasekeyboard._stop_kps_change()
        self.assertGreater(self.ibasekeyboard.kps, 0)

    def test_Start(self):
        with self.assertRaises(NotImplementedError):
            self.ibasekeyboard.start()

    def test_Stop(self):
        with self.assertRaises(NotImplementedError):
            self.ibasekeyboard.stop()

    def test_CapKps(self):
        self.ibasekeyboard._cap_kps = 10
        self.assertEqual(self.ibasekeyboard.cap_kps, 10)
        self.ibasekeyboard._cap_kps = 9
