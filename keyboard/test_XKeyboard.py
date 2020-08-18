import unittest
from .XKeyboard import XKeyboard
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import event


class DummyDisplay:
    """Copied from
    https://github.com/python-xlib/python-xlib/test/__init__.py"""
    def get_resource_class(self, x):
        return None

    event_classes = event.event_class


class MockDisplay:
    """Can't use magic mock here,
    cuz there exists environments without displays
    which throws an exception"""
    def __init__(self):
        self.has_extension_return = False
        self.create_context_run = False
        self.enable_context_run = False
        self.disable_context_run = False
        self.free_context_run = False
        self.display = DummyDisplay()

    def has_extension(self, _: str) -> bool:
        return self.has_extension_return

    def record_create_context(self, *args):
        self.create_context_run = True
        return 123

    def record_enable_context(self, ctx, *args):
        if ctx == 123:
            self.enable_context_run = True
        return

    def record_disable_context(self, ctx, *args):
        if ctx == 123:
            self.disable_context_run = True
        return

    def record_free_context(self, ctx, *args):
        if ctx == 123:
            self.free_context_run = True
        return


class MockReplyRequest:
    def __init__(self):
        self.category = None
        self.client_swapped = None
        self.data = None


class TestXKeyboard(unittest.TestCase):
    def setUp(self):
        fake_display = MockDisplay()
        fake_display.has_extension_return = True
        self.display = fake_display
        self.xkeyboard = XKeyboard(display_instance=fake_display)

    def test_NoRecordExtension(self):
        fake_display = MockDisplay()
        fake_display.has_extension_return = False
        with self.assertRaises(
            RuntimeError,
            msg="Cannot use X11 method to get key events"
        ):
            XKeyboard(display_instance=fake_display)

    def test_StartAndStop(self):
        self.xkeyboard.start()
        self.assertTrue(self.xkeyboard.is_started)
        self.assertTrue(self.display.create_context_run)
        self.assertTrue(self.display.enable_context_run)
        self.assertFalse(self.display.disable_context_run)
        self.assertFalse(self.display.free_context_run)

        with self.assertRaises(
            RuntimeError,
            msg="Tried to start XKeyboard that is already started"
        ):
            self.xkeyboard.start()

        self.xkeyboard.stop()
        self.assertFalse(self.xkeyboard.is_started)
        self.assertTrue(self.display.create_context_run)
        self.assertTrue(self.display.enable_context_run)
        self.assertTrue(self.display.disable_context_run)
        self.assertTrue(self.display.free_context_run)

        with self.assertRaises(
            RuntimeError,
            msg="Tried to stop XKeyboard that is already stopped"
        ):
            self.xkeyboard.stop()

    def test_Callback(self):
        event_data = event.AnyEvent._fields.to_binary(
            type=X.KeyPress,
            detail=1,
            sequence_number=123,
            data=b""
        )

        reply = MockReplyRequest()
        reply.category = record.FromServer
        reply.client_swapped = False
        reply.data = event_data

        self.xkeyboard._record_callback(reply)
        self.assertEqual(self.xkeyboard._buffer_kps, 1)
        self.xkeyboard._buffer_kps = 0

    def test_CallbackFail(self):
        event_data = event.AnyEvent._fields.to_binary(
            type=X.KeyRelease,
            detail=1,
            sequence_number=123,
            data=b""
        )

        reply = MockReplyRequest()
        reply.category = record.FromServer
        reply.client_swapped = False
        reply.data = event_data

        self.xkeyboard._record_callback(reply)
        self.assertEqual(self.xkeyboard._buffer_kps, 0)
        self.xkeyboard._buffer_kps = 0
