# IBaseKeyboard.py - Base class for all keyboard derivations
from threading import Thread, RLock
import asyncio


class IBaseKeyboard:
    """Base class for all subsequent keyboard classes"""
    def __init__(self, *, increase_rate=0.01, decay_rate=0.1, cap_kps=9):
        self._buffer_kps = 0
        self._cap_kps = cap_kps
        self._kps = 0
        self._kps_lock = RLock()
        self._increase_rate = increase_rate
        self._decay_rate = decay_rate
        self._rate_lock = RLock()
        self._is_started = False
        self._kps_up_thread = None
        self._kps_down_thread = None
        self._kill_signal = False
        self._kill_signal_lock = RLock()
        self._event_loop = None

    def _start_kps_change(self):
        self._event_loop = asyncio.new_event_loop()
        self._kps_thread = Thread(target=self._callback_kps_change)
        self._kps_thread.start()

    def _stop_kps_change(self):
        with self._kill_signal_lock:
            if self._kill_signal:
                raise RuntimeError("Already trying to kill")
            if not self._kps_thread:
                raise RuntimeError("No valid KPS thread")
            self._kill_signal = True
        self._kps_thread.join()
        self._event_loop.close()
        self._kill_signal = False

    def _callback_kps_change(self):
        async def kps_loop():
            await asyncio.wait((
                self._callback_kps_up(),
                self._callback_kps_down()
            ))
        self._event_loop.run_until_complete(kps_loop())

    async def _callback_kps_up(self):
        while not self._kill_signal:
            with self._kps_lock:
                if self._buffer_kps > self._kps:
                    self._kps = min((
                        (self.increase_rate * self._kps) + self._buffer_kps
                    ) / (self.increase_rate + 1), self._cap_kps)
                self._buffer_kps = 0
            await asyncio.sleep(1.0)

    async def _callback_kps_down(self):
        while not self._kill_signal:
            with self._kps_lock:
                if self._kps > 0:
                    self._kps -= (20.0 / self._kps) * (self.decay_rate / 10.0)
                    if self._kps < 0:
                        self._kps = 0
            await asyncio.sleep(0.1)

    @property
    def increase_rate(self):
        with self._rate_lock:
            return self._increase_rate

    @increase_rate.setter
    def increase_rate(self, value):
        with self._rate_lock:
            self._increase_rate = value
        return

    @property
    def decay_rate(self):
        with self._rate_lock:
            return self._decay_rate

    @decay_rate.setter
    def decay_rate(self, value):
        with self._rate_lock:
            self._decay_rate = value
        return

    def start(self):
        """Starts listening to the keyboard"""
        raise NotImplementedError

    def stop(self):
        """Stops listening to the keyboard"""
        raise NotImplementedError

    @property
    def is_started(self):
        return self._is_started

    @property
    def kps(self):
        with self._kps_lock:
            return self._kps

    @property
    def cap_kps(self):
        return self._cap_kps
