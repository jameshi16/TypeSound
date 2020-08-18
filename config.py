#!/usr/bin/env python3
# config.py - Interactive configuration script
import time
import numpy
import os
from keyboard import XKeyboard
from configuration import JSONConfiguration, ConfigurationSchemeV1


def get_input_non_empty(input_str, cast=str):
    """Obtains inputs from STDIN, ensuring that they are not empty"""
    data = ''
    while True:
        try:
            data = input(input_str)
            if data.strip() == '':
                print('Empty input. Try again')
                continue
            return cast(data)
        except Exception:
            continue


def get_user_choice(prompt_str, valid_choices=['y', 'n']):
    """Obtains input from STDIN, constraining it to valid_choices"""
    data = get_input_non_empty(prompt_str).lower()
    while data not in valid_choices:
        data = get_input_non_empty(prompt_str).lower()

    return data


def infer_kps_routine():
    """A (large) routine to infer KPS from a user's typing behaviour"""
    keyboard = XKeyboard(increase_rate=0.0, decay_rate=0.0, cap_kps=9999999)
    keyboard.start()
    kps_history = []
    while True:
        try:
            kps_history.append(keyboard.kps)
            time.sleep(1)
        except KeyboardInterrupt:
            print('\nTerminating calculation...')
            keyboard.stop()
            break

    # get gradients
    kps_history_np = numpy.array(kps_history)
    kps_gradients = numpy.gradient(kps_history_np)
    minimum_gradient_indices = numpy.argsort(kps_gradients)
    ideal_gradient = kps_gradients[minimum_gradient_indices[0]]

    # collect 5 datapoints around the minimum gradients
    candidate_kps_history_slices = []
    for i in minimum_gradient_indices:
        if ideal_gradient < kps_gradients[minimum_gradient_indices[i]]:
            continue

        start_index = 0 if i - 2 < 0 else i - 2
        # pylint complains when i try to create a one-liner here
        end_index = i + 3
        if end_index > kps_history_np.size:
            end_index = kps_history_np.size - 1

        candidate_kps_history_slices.append(
            kps_history_np[start_index:end_index])

    # choose the right slices
    ideal_size = max(candidate_kps_history_slices, key=lambda x: x.size).size
    ideal_iterator = list(map(
        lambda x: x.size,
        filter(lambda x: x.size == ideal_size, candidate_kps_history_slices)))

    # reduce all kps
    reduced_candidate_slice = candidate_kps_history_slices[ideal_iterator[0]]
    for i in ideal_iterator:
        reduced_candidate_slice = numpy.maximum(
            reduced_candidate_slice, candidate_kps_history_slices[i])
    qed_kps = reduced_candidate_slice.mean()
    return qed_kps


def prompt_kps():
    """Automatically acquired KPS, or allow user to manually specify"""
    choice = get_user_choice('Would you like to get your KPS manually or '
                             + 'automatically? [M/A]: ', ['m', 'a'])
    # prompt / infer kps
    cap_kps = 0.0
    if choice == 'a':
        print('Visit a typing test website, like 10fastfingers '
              + 'or speed racer, and type away.')
        print('Once you are satisfied with your maximum speed, '
              + 'Press CTRL+C once.')
        max_kps = infer_kps_routine()
        cap_kps = max_kps * 0.6
    else:
        cap_kps = get_input_non_empty('Insert your max KPS (typical values '
                                      + 'range from 0.1 to 20.0): ', float)

    return cap_kps


def prompt_playlist_directory():
    print('\n\nPlaylist directory specifies the directory to play music from.')
    playlist_directory_prompt = 'Playlist directory: '
    playlist_directory = get_input_non_empty(playlist_directory_prompt)
    while True:
        while not os.path.exists(playlist_directory):
            print('That path does not seem to exist. Try again')
            playlist_directory = get_input_non_empty(playlist_directory_prompt)

        print('In your directory, these supported music files exists:')
        supported_files = list(
            filter(lambda x: os.path.splitext(x)[1] in ['.wav', '.mp3'],
                   os.listdir(playlist_directory)))
        if len(supported_files) == 0:
            print(' No supported files exists.')
        for supported_file in supported_files:
            print(' - ', os.path.split(supported_file)[1])

        if get_user_choice('Confirm directory? [Y/n]: ') == 'y':
            break

    return playlist_directory


def prompt_increase_decay_rate():
    # ask for increase/decay rate
    print('\n\nIncrease rate is how much weight the historic KPS has as ' +
          'the user types. The lower this number, the more effect ' +
          'the KPS is reliant on instantaneous KPS.')
    increase_rate_prompt = 'Increase rate (recommended 0.1): '
    increase_rate = get_input_non_empty(increase_rate_prompt, float)

    print('The higher the decay rate, the faster the reduction of KPS.')
    decay_rate_prompt = 'Decay rate (recommended 0.01): '
    decay_rate = get_input_non_empty(decay_rate_prompt, float)

    return (increase_rate, decay_rate)


def config_summary(config: ConfigurationSchemeV1):
    """Prints the config summary as defined in config variable"""
    print('---[ Config Summary ]---')
    print('Cap KPS: ', config.cap_kps)
    print('Playlist Directory: ', config.path_to_dir)
    print('Increase rate: ', config.increase_rate)
    print('Decay rate: ', config.decay_rate)


def edit_config(config: ConfigurationSchemeV1):
    """Returns True for a reloop, False for exiting a loop"""
    print('\n\n---[ Editing Options ]---')
    print('1) Cap KPS')
    print('2) Playlist directory')
    print('3) Increase rate / Decay rate')
    print('4) Save changes')

    try:
        choice = get_user_choice('Option > ', [str(x) for x in range(1, 5)])
    except KeyboardInterrupt:
        print(' Exiting...\n')
        return False

    if choice == '1':
        config.cap_kps = prompt_kps()
    elif choice == '2':
        config.path_to_dir = prompt_playlist_directory()
    elif choice == '3':
        (config.increase_rate,
         config.decay_rate) = prompt_increase_decay_rate()
    elif choice == '4':
        return False
    return True


print('--- [ Configuration Tool ] ---')
json_config_loader = JSONConfiguration()
config = ConfigurationSchemeV1(json_config_loader)
if not os.path.isfile('config.json'):
    print('config.json not found.')
    print('--- [ New Setup ] ---')
    print('Configuration tool intends to calculate Keys Per Second (KPS) '
          + 'of the user.')

    # ask user for kps
    cap_kps = prompt_kps()

    # ask user for playlist directory
    playlist_directory = prompt_playlist_directory()

    # ask user for increase / decay rate
    (increase_rate, decay_rate) = prompt_increase_decay_rate()

    # build configuration
    json_config_loader.load_config_from_string('{"version": 1}')
    config.cap_kps = cap_kps
    config.decay_rate = decay_rate
    config.increase_rate = increase_rate
    config.path_to_dir = playlist_directory

    print('\nNew configuration complete.')
else:
    json_config_loader.load_config_from_file('config.json')

while True:
    config_summary(config)
    if edit_config(config):
        print('\n')
        continue

    save_changes_intent = get_user_choice('Save changes? [Y/n]: ')
    if save_changes_intent == 'y':
        config.save_to_file('config.json')
        print('Changes saved to config.json')
        break
