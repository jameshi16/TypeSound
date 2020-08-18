import unittest
import numpy as np
import sox
from unittest.mock import patch
from .MiniaudioPlayer import MiniaudioPlayer

# build the test tone here, becasue we're patching sox.Transformer later
test_tone = np.sin(2 * np.pi * 440.0 * np.arange(44100 * 1.0) / 44100)
tfm = sox.Transformer()
y_out = tfm.build_array(input_array=test_tone, sample_rate_in=44100)


@patch('sox.Transformer')
def makePlayer(patched_transformer):
    patched_transformer.return_value.build_array.return_value = y_out
    return MiniaudioPlayer('does not matter')


class TestMiniaudioPlayer(unittest.TestCase):
    def setUp(self):
        global y_out
        self.miniaudioplayer = makePlayer()
        self.generator = None

    def start_playback(self, stream):
        self.generator = stream

    @patch('miniaudio.PlaybackDevice')
    def test_Play(self, miniaudio_playback):
        self.miniaudioplayer.speed_factor = 1.0
        self.miniaudioplayer._width = 1
        miniaudio_playback.return_value.start.side_effect = self.start_playback
        self.miniaudioplayer.play()
        self.assertIsNotNone(self.generator)

        with self.assertRaises(RuntimeError):
            self.miniaudioplayer.play()

        data = self.generator.send(len(y_out))
        self.assertTrue((y_out.astype(np.int16) == data).all())

        self.miniaudioplayer.pause()
        self.assertFalse(self.miniaudioplayer._played)
        self.assertTrue(self.miniaudioplayer._paused)

        self.miniaudioplayer.play()
        self.assertTrue(self.miniaudioplayer._played)
        self.assertFalse(self.miniaudioplayer._paused)

        self.miniaudioplayer.pause()
        self.assertFalse(self.miniaudioplayer._played)
        self.assertTrue(self.miniaudioplayer._paused)

        self.miniaudioplayer.unpause()
        self.assertTrue(self.miniaudioplayer._played)
        self.assertFalse(self.miniaudioplayer._paused)

        self.miniaudioplayer.stop()

    @patch('miniaudio.PlaybackDevice')
    def test_FactoredPlay(self, miniaudio_playback):
        self.miniaudioplayer.speed_factor = 2.0
        miniaudio_playback.return_value.start.side_effect = self.start_playback
        self.miniaudioplayer.play()
        self.assertIsNotNone(self.generator)

        data = self.generator.send(len(y_out))
        self.assertEqual(len(data) / 2, len(y_out))

    @patch('miniaudio.PlaybackDevice')
    def test_Finished(self, miniaudio_playback):
        self.miniaudioplayer.speed_factor = 2.0
        miniaudio_playback.return_value.start.side_effect = self.start_playback
        self.miniaudioplayer.play()
        self.assertIsNotNone(self.generator)

        self.generator.send(len(y_out))
        with self.assertRaises(StopIteration):
            self.generator.send(1)
        self.assertTrue(self.miniaudioplayer.finished())
