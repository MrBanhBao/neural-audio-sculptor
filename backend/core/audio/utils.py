import hashlib
import os
from typing import Dict

import numpy as np
import numpy.typing as npt
from spleeter.separator import Separator

import utils.store as store
from utils import create_directory

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


def split_audio(audio_data: npt.NDArray[np.float32]) -> Dict[str, npt.NDArray[np.float32]]:
    """
    Splits Audio data in 5 components (vocals, drums, bass, piano, other)
    by using spleeter in this environment.

    Parameters:
        audio_data (npt.NDArray[np.float32]): Audio data as numpy array

    Returns:
        splitted_aduio (Dict[str, NDArray[Shape["*, 2"], Float32]]):
        Dict containing audio data of keys ('vocals', 'drums', 'bass', 'piano', 'other')
    """

    hash_value = hashlib.sha1(audio_data).hexdigest()

    directory = os.path.join(cache_dir, hash_value)
    create_directory(directory)

    splits_data_file = os.path.join(directory, "splits.npy")

    if not os.path.exists(splits_data_file):
        result = seperator.separate(audio_data)
        np.save(splits_data_file, result)
        return result
    else:
        print(f'{hash_value}, Found in cache.')
        return np.load(splits_data_file, allow_pickle=True).item()
