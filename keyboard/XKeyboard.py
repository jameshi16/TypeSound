from . import IBaseKeyboard
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq
from threading import Thread


class XKeyboard(IBaseKeyboard):
    """X11 method to get keyboard event.
    Unlike the keyboard package, this does not require
    root privileges"""
    def __init__(
        self,
        *,
        increase_rate=0.01,
        decay_rate=0.1,
        cap_kps=9,
        display_instance=display.Display()
    ):
        super().__init__(
            increase_rate=increase_rate,
            decay_rate=decay_rate,
            cap_kps=cap_kps
        )
        self.local_dpy = display_instance
        self.record_dpy = display_instance
        self._keyboard_thread = None

        if not self.record_dpy.has_extension("RECORD"):
            raise RuntimeError("Cannot use X11 method to get key events")

    def _record_callback(self, reply: rq.ReplyRequest):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            return
        if not len(reply.data) or reply.data[0] < 2:
            return

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(
                data, self.record_dpy.display, None, None)

            if event.type == X.KeyPress:
                with self._kps_lock:
                    self._buffer_kps += 1

    def start(self):
        """Enables the X11 recording context to listen to keyboard"""
        if self._is_started:
            raise RuntimeError(
                "Tried to start XKeyboard that is already started")

        self.ctx = self.record_dpy.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.KeyRelease),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }])
        self._keyboard_thread = Thread(
            target=self.record_dpy.record_enable_context,
            args=(self.ctx, self._record_callback)
        )
        self._keyboard_thread.daemon = True
        self._keyboard_thread.start()
        self._start_kps_change()
        self._is_started = True

    def stop(self):
        """Disables the X11 recording context to listen to keyboard"""
        if not self._is_started:
            raise RuntimeError(
                "Tried to stop XKeyboard that is already stopped")
        self.record_dpy.record_disable_context(self.ctx)
        self.record_dpy.record_free_context(self.ctx)
        self._stop_kps_change()
        # NOTE: I have no idea why, but record_disable_context doesn't actually
        # stop the record_enable_context thread. We'll just time it out.
        # Keyboard thread is a daemon thread and only spawns once,
        # so it'll gracefully exit with the python program.
        self._keyboard_thread.join(1)
        self._is_started = False
