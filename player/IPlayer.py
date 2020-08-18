# IPlayer.py - The music player interface capable of speed control.
from threading import RLock


class IPlayer:
    def __init__(self, path_to_file):
        self._speed_factor = 0.0
        self._speed_factor_lock = RLock()

    def play(self):
        raise NotImplementedError

    def unpause(self):
        """Play will throw an exception if the user calls it twice.
        Unpause silently fails instead."""
        raise NotImplementedError

    def pause(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def finished(self):
        raise NotImplementedError

    @property
    def speed_factor(self):
        with self._speed_factor_lock:
            return self._speed_factor

    @speed_factor.setter
    def speed_factor(self, value):
        with self._speed_factor_lock:
            self._speed_factor = value
