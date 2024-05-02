import os
from typing import Dict

import numpy as np
import numpy.typing as npt
from scipy.io import wavfile
from spleeter.separator import Separator

import utils.store as store

cache_dir = store.config.backend.cache_dir
sample_rate = store.config.audio.sample_rate
track_names = store.track_names
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
