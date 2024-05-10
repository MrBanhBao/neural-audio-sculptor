import os
from typing import Dict

import librosa
import numpy as np
import numpy.typing as npt
from scipy.io import wavfile
from spleeter.separator import Separator

import utils.store as store
from utils import load_json, normalize_array, save_dict_as_json

sample_rate = store.config.audio.sample_rate
frame_length = store.config.audio.frame_length
hop_length = store.config.audio.hop_length
cache_dir = store.config.backend.cache_dir

seperator = Separator("spleeter:5stems")


def make_mono(audio_data: npt.NDArray[np.float32]) -> npt.NDArray:
    """
    Converts an numpy array containing stereo audio data to a mono audio.

    Parameters:
        audio_data (NDArray[Shape['*, 2'], Float32]): numpy array with stereo audio data.

    Returns:
        audio_data (NDArray[Shape['*, 1'], Float32]): converted numpy array with mono audio data.
    """
    return (audio_data[:, 0] + audio_data[:, 1]) / 2


def split_audio(audio_data: npt.NDArray[np.float32], save_dir: str) -> Dict[str, npt.NDArray[np.float32]]:
    """
    Splits Audio data in 5 components (vocals, drums, bass, piano, other)
    by using spleeter in this environment.

    Parameters:
        audio_data (npt.NDArray[np.float32]): Audio data as numpy array

    Returns:
        splitted_audio (Dict[str, NDArray[Shape["*, 2"], Float32]]):
        Dict containing audio data of keys ('vocals', 'drums', 'bass', 'piano', 'other')
    """

    splitted_audio = seperator.separate(audio_data)

    for track_name, audio in splitted_audio.items():
        file = os.path.join(save_dir, f"{track_name}.wav")
        wavfile.write(file, sample_rate, audio)

    return splitted_audio


def calculate_audio_features(audio_tracks: Dict[str, npt.NDArray[np.float32]], folder_name: str):
    changed = False
    json_file = os.path.join(cache_dir, folder_name, 'features.json')
    feature_data = load_json(json_file)

    for track_name, value in audio_tracks.items():
        if track_name not in feature_data:
            feature_data[track_name] = {}

        if "rms" not in feature_data[track_name]:
            values = librosa.feature.rms(
                y=make_mono(value),
                frame_length=frame_length,
                hop_length=hop_length,
                center=True,
            )[0]
            feature_data[track_name]["rms"] = normalize_array(values)
            print('Calculating rms...')
            changed = True

        if "pitch" not in feature_data[track_name]:
            values = pitches_over_time(
                y=make_mono(value),
                frame_length=frame_length,
                hop_length=hop_length,
                sr=sample_rate
            )
            feature_data[track_name]["pitch"] = normalize_array(values)
            print('Calculating pitch...')
            changed = True

        if "tempo" not in feature_data[track_name]:
            values = tempo_over_time(y=make_mono(value),
                frame_length=frame_length,
                hop_length=hop_length,
                sr=sample_rate)
            feature_data[track_name]["tempo"] = normalize_array(values)
            print('Calculating tempo...')
            changed = True

        if "onset" not in feature_data[track_name]:
            values = librosa.onset.onset_strength(y=make_mono(value),
                                                  sr=sample_rate,
                                                  hop_length=hop_length,)
            feature_data[track_name]["onset"] = normalize_array(values)
            print('Calculating onset...')
            changed = True

        if "energy" not in feature_data[track_name]:
            values = energy_over_time(y=make_mono(value),
                                     frame_length=frame_length,
                                     hop_length=hop_length)
            feature_data[track_name]["energy"] = normalize_array(values)
            print('Calculating energy...')
            changed = True

    store.audio_features = feature_data
    if changed:
        save_dict_as_json(feature_data, json_file)

    print('Done loading/cauclating features...')
    store.isFeaturesReady = True



def energy_over_time(y: npt.NDArray[np.float32], frame_length: int=441, hop_length: int=512):
    """
    This function estimates energy in overlapping windows of an audio file

    Args:
        y (npt.NDArray[np.float32]): Audio Data as numpy array
        frame_length (int): Size of the window in frames (samples)
        hop_length (int): Hop length between windows in frames (samples)

    Returns:
        energies npt.NDArray[np.float32]: List of energy values for each window
    """
    energies = []

    # Iterate through audio in overlapping windows
    for start in np.arange(0, len(y), hop_length):
        end = start + frame_length

        # Ensure window stays within audio bounds
        if end > len(y):
            end = len(y)
        window = y[start:end]

        # Calculate energy within the window
        energy = np.sum(window**2)

        energies.append(energy)

    return np.array(energies)


def pitches_over_time(y: npt.NDArray[np.float32], frame_length: int = 2048,
                      hop_length: int = 512, sr: int = 44100):
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=hop_length, n_fft=frame_length)
    pitch = np.argmax(chroma, axis=0)
    return pitch


def tempo_over_time(y: npt.NDArray[np.float32], frame_length: int = 2048,
                    hop_length: int = 512, sr: int = 44100):
    tempogram = librosa.feature.tempogram(y=y, sr=sr, hop_length=hop_length, win_length=frame_length)
    tempo = np.average(tempogram, axis=0)
    return tempo

