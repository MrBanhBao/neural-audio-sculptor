import glob
import os

import utils.store as store
from core.audio import AudioLoader
from core.audio.utils import split_audio, calculate_audio_features
from data_models import Config
from utils import is_splitted, create_directory

CONFIG_FILE = "../frontend/static/config.yaml"
config: Config = Config.load(config_file=CONFIG_FILE)

sample_rate = config.audio.sample_rate
cache_dir = config.backend.cache_dir
music_dir = config.backend.music_dir
audio_extensions = ['*.mp3', '*.wav', '*.flac', '*.aac', '*.ogg']
track_names = store.track_names

if __name__ == '__main__':
    audio_loader = AudioLoader(sample_rate=sample_rate)
    audio_files = []

    # Iterate through each audio file extension
    for ext in audio_extensions:
        # Use glob to find all files with the given extension in the directory
        audio_files.extend(glob.glob(os.path.join(music_dir, ext)))


    print(f"Found {len(audio_files)} in folder {music_dir}")
    # Iterate through each found audio file
    for audio_file in audio_files:
        audio_data_tracks = {}
        # Load audio
        audio_data, audio_meta_data = audio_loader.load_audio(audio_file)
        folder_name = os.path.splitext(audio_meta_data.file_name)[0]
        audio_data_tracks["main"] = audio_data

        directory = os.path.join(cache_dir, folder_name)
        files = [os.path.join(directory, f"{track}.wav") for track in track_names[1:]]

        if not is_splitted(files):
            print(f"Start splitting {audio_file}...")
            create_directory(directory)
            splitted_audio_data_tracks = split_audio(audio_data=audio_data, save_dir=directory)
            audio_data_tracks.update(splitted_audio_data_tracks)

            print(f"Calculate features {audio_file}...")
            calculate_audio_features(audio_data_tracks, folder_name)
        else:
            print("Allready splitted.")

