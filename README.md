# TypeSound

![TypeSound CI](https://github.com/jameshi16/TypeSound/workflows/TypeSound%20CI/badge.svg)

Type or your music stops :knife:.

This tool was created for [@jameshi16](https://github.com/jameshi16) to have fun and mess around with simple audio manipulation, unit testing and GitHub actions. Also he needed [blog](https://codingindex.xyz) content.

# Setting up

Create a virtual environment, clone the repository, install all the pip packages in `requirements.txt`, run `config.py`, then run `main.py`.

```bash
virtualenv -p python3 ~/.environments/typesound
source ~/.environments/typesound/bin/activate
git clone https://github.com/jameshi16/TypeSound.git
cd TypeSound
pip install -r requirements.txt
./config.py
./main.py
```

A configuration file named `config.json` will be created in the directory, which defines how TypeSound adjusts the music to your typing speed.

# Configuration

These are the configuration options that you have:

|Config Option|Description|Recommended Value|
|---|---|---|
|cap_kps|The maximum key per second (KPS) you can type. This should generally be lower than your actual KPS, because you want your music to sound normal when you type slightly slower than your peak.|For 100WPM typists, 9.0 is a good value.|
|decay_rate|An arbitary factor that defines how quickly effective KPS decays when you stop typing.|0.01|
|increase_rate|An arbitary factor that defines how much weight historic KPS has on the effective KPS. The lower the value, the more your instantenous KPS affects music playback rate.|0.1|
|path_to_dir|Path to your music folder. Confirmed supported music formats include `.wav` files and `.mp3` files|Your music folder|

# License

[MIT License](./LICENSE.md)
