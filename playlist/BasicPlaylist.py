# BasicPlaylist.py - Playlists are essentially generators
from typing import Generator
import os


def get_play_paths(path: str) -> [str]:
    if os.path.isfile(path):
        return [path]

    if os.path.isdir(path):
        return list(map(lambda x: x.path, os.scandir(path)))

    raise RuntimeError("Cannot get music file paths")


def basic_playlist(
    path: str,
    *,
    supported_extensions=[".mp3", ".wav"]
) -> Generator[str, None, None]:
    try:
        paths = get_play_paths(path)
    except FileNotFoundError:
        print("Can't find directory for the playlist")
        return
    except RuntimeError as e:
        print("Error while initializing basic playlist: ", e)
        return

    for supported_file in filter(
        lambda x: os.path.splitext(x)[1] in supported_extensions,
        paths
    ):
        yield supported_file
    return
