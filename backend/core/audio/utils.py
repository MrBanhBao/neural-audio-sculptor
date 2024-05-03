import os
from typing import Dict

import librosa
import numpy as np
import numpy.typing as npt
from scipy.io import wavfile
from spleeter.separator import Separator

import utils.store as store

sample_rate = store.config.audio.sample_rate
frame_length = store.config.audio.frame_length
hop_length = store.config.audio.hop_length

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

def calulate_audio_features(audio_tracks: Dict[str, npt.NDArray[np.float32]]):
    for key, value in audio_tracks.items():
        audio_feature = librosa.feature.rms(
            y=make_mono(value),
            frame_length=frame_length,
            hop_length=hop_length,
            center=True,
        )

    print("Feature calculation done!!!!")