# MiniaudioPlayer.py - Music player based on Miniaudio
from .IPlayer import IPlayer
import numpy as np
import sox
import miniaudio


class MiniaudioPlayer(IPlayer):
    """IPlayer implementation using miniaudio and sox"""
    def __init__(self, path_to_file: str):
        super(MiniaudioPlayer, self).__init__(path_to_file)
        self._index = 0
        self._width = 2
        self._channels = 2
        self._sample_rate = 44100
        self._device = None
        self._played = False
        self._paused = False
        self._finished = False

        tfm = sox.Transformer()
        self.y_out = tfm.build_array(
            input_filepath=path_to_file)

    def __sound_callback(self):
        required_frames = yield b""
        y_out = self.y_out
        while True:
            factor = self.speed_factor
            required_bytes = required_frames * self._width
            x0 = np.linspace(0.0,
                             float(required_frames) - 1.0,
                             int(required_bytes * factor))
            x1 = np.linspace(0.0,
                             float(required_frames) - 1.0,
                             required_bytes)

            sample_data = y_out[
                self._index:
                self._index + int(
                    required_frames * factor)].flatten().astype(np.float)
            if self._index > y_out.shape[0]:
                self._finished = True
                return
            if len(x0) > len(sample_data):
                x0 = x0[:len(sample_data)]
            self._index += int(required_frames * factor)
            adjusted_data = np.interp(x1, x0, sample_data).astype(np.int16)
            required_frames = yield adjusted_data
        self._finished = True

    def play(self):
        if self._played:
            raise RuntimeError("Cannot be played again")

        if not self._paused:
            self._device = miniaudio.PlaybackDevice(
                output_format=miniaudio.SampleFormat.SIGNED16,
                nchannels=self._channels,
                sample_rate=self._sample_rate)

            self._stream = self.__sound_callback()
            next(self._stream)

        self._device.start(self._stream)
        self._played = True
        self._paused = False

    def unpause(self):
        if self._played:
            return

        if not self._paused or self._device is None:
            raise RuntimeError("Cannot unpause invalid playback")

        self._device = miniaudio.PlaybackDevice(
            output_format=miniaudio.SampleFormat.SIGNED16,
            nchannels=self._channels,
            sample_rate=self._sample_rate)

        self._device.start(self._stream)
        self._played = True
        self._paused = False

    def pause(self):
        self._device.close()
        self._played = False
        self._paused = True

    def stop(self):
        self._device.close()
        self._device = None
        self._played = False
        self._paused = False

    def finished(self):
        return self._finished
