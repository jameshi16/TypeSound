import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from .BasicPlaylist import get_play_paths, basic_playlist


class TestBasicPlaylist(unittest.TestCase):
    @patch('os.path')
    @patch('os.scandir')
    def test_PlayPaths(self, scandir_mock, path_mock):
        path_mock.isfile.return_value = True
        self.assertEqual(get_play_paths('no matter'), ['no matter'])

        path_mock.isfile.return_value = False
        path_mock.isdir.return_value = True
        fakeDirEntry = MagicMock()
        type(fakeDirEntry).path = PropertyMock(return_value='testing')
        scandir_mock.return_value = [fakeDirEntry]
        self.assertEqual(get_play_paths('no matter'), ['testing'])

        path_mock.isfile.return_value = False
        path_mock.isdir.return_value = False
        with self.assertRaises(
            RuntimeError,
            msg='Cannot get music file paths'
        ):
            get_play_paths('no matter')

    @patch(__name__.split('.', 1)[0] + '.BasicPlaylist.get_play_paths')
    def test_BasicPlaylist(self, playpath_mock):
        playpath_mock.return_value = ['test1.wav', 'test2.mp3', 'test3.midi']
        playlist = basic_playlist('no matter')
        self.assertEqual(['test1.wav', 'test2.mp3'], list(playlist))

        playpath_mock.side_effect = FileNotFoundError()
        playlist = basic_playlist('no matter')
        with self.assertRaises(StopIteration):
            next(playlist)

        playpath_mock.side_effect = RuntimeError()
        playlist = basic_playlist('no matter')
        with self.assertRaises(StopIteration):
            next(playlist)
