#!/usr/bin/env python3
from configuration import JSONConfiguration, ConfigurationSchemeV1
from playlist import basic_playlist
from keyboard import XKeyboard
from player import MiniaudioPlayer
import time
import os

# read config if exists, otherwise tell user to run ./config.py
config = None
if os.path.isfile('config.json'):
    json_config_loader = JSONConfiguration()
    json_config_loader.load_config_from_file('config.json')

    if json_config_loader.get_version() == 1:
        config = ConfigurationSchemeV1(json_config_loader)

if not config:
    print('Cannot find a valid config file. Try running ./config.py first.')
    exit(-1)

# TODO: Detect which keyboard class to use automatically
keyboard = XKeyboard(
    increase_rate=config.increase_rate,
    decay_rate=config.decay_rate,
    cap_kps=config.cap_kps
)

# TODO: Get playlist type from config
playlist = basic_playlist(config.path_to_dir)
player = None

# start the keyboard kps
keyboard.start()

# factor update loop
while True:
    try:
        if player is None or player.finished():
            try:
                next_song = next(playlist)
                print("Now playing ♫: ", next_song)
            except StopIteration:
                print('No more songs to play. Exiting...')
                player = None
                exit()
            player = MiniaudioPlayer(next_song)
            player.play()

        if keyboard.kps == 0.0:
            player.pause()
        else:
            player.speed_factor = keyboard.kps / keyboard.cap_kps
            player.unpause()
        time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit):
        print('Please be patient while we quit gracefully',
              '(CTRL + C again to force)...')
        if player is not None:
            player.stop()
        keyboard.stop()
        exit()
