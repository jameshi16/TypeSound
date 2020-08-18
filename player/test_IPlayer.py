import unittest
from .IPlayer import IPlayer


class TestIPlayer(unittest.TestCase):
    def setUp(self):
        self.iplayer = IPlayer("doesn't matter")

    def test_Play(self):
        with self.assertRaises(NotImplementedError):
            self.iplayer.play()

    def test_Pause(self):
        with self.assertRaises(NotImplementedError):
            self.iplayer.pause()

    def test_Unpause(self):
        with self.assertRaises(NotImplementedError):
            self.iplayer.unpause()

    def test_Stop(self):
        with self.assertRaises(NotImplementedError):
            self.iplayer.stop()

    def test_Finished(self):
        with self.assertRaises(NotImplementedError):
            self.iplayer.finished()

    def test_SpeedFactor(self):
        self.iplayer.speed_factor = 1.0
        self.assertEqual(self.iplayer.speed_factor, 1.0)
        self.iplayer.speed_factor = 0.0
