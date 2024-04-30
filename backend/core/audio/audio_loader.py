import base64
import io
import math
from typing import Tuple

import numpy as np
import numpy.typing as npt
from PIL import Image
from spleeter.audio.adapter import AudioAdapter
from tinytag import TinyTag

from data_models import AudioMetaData


class AudioLoader:
    """
    Loads audio data as numpy arrays.

    Args:
        sample_rate (int): Sample rate of loaded audio file.

    Attributes:
        audio_adapter (AudioAdapter): Spleeter's audio loader.
        sample_rate (int): Sample rate of loaded audio file.
        sound_devices
    """

    def __init__(self, sample_rate: int = 44100) -> None:
        self.audio_adapter: AudioAdapter = AudioAdapter.default()
        self.sample_rate: int = sample_rate

    def load_audio(self, path: str) -> Tuple[npt.NDArray[np.float32], AudioMetaData]:
        """
        Loads audio data via spleeter's audio adapter.

        Parameters:
            path (str): path to audio file.

        Returns:
            audio_data (NDArray[Shape['*, *'], Float32]): audio data.
        """

        audio_data: npt.NDArray[np.float32]
        audio_data, sample_rate = self.audio_adapter.load(
            path, sample_rate=self.sample_rate
        )

        audio_meta_data = self.load_meta_data(
            path=path, sample_rate=int(sample_rate), num_frames=len(audio_data)
        )

        return audio_data, audio_meta_data

    def load_meta_data(self, path: str, sample_rate: int, num_frames: int) -> AudioMetaData:
        if TinyTag.is_supported(path):
            tag = TinyTag.get(path, image=True)

            img_base64 = None
            if tag.get_image() is not None or tag.get_image() == "":
                img_bytes = tag.get_image()
                img_pil = Image.open(io.BytesIO(img_bytes))

                with io.BytesIO() as buf:
                    img_pil.save(buf, format="JPEG")
                    img_bytes = buf.getvalue()
                    img_base64 = base64.b64encode(img_bytes)

            data = {
                "artist": tag.artist,
                "title": tag.title,
                "path": path,
                "file_name": path.split("/")[-1],
                "sample_rate": sample_rate,
                "num_frames": num_frames,
                "duration": math.ceil(tag.duration),  # in seconds
                "image": img_base64
            }
            return AudioMetaData(**data)

    def load_cover(self, path: str) -> bytes:
        tag = TinyTag.get(path, image=True)

        img_bytes = None
        if tag.get_image() is not None or tag.get_image() == "":
            img_bytes = tag.get_image()
            img_pil = Image.open(io.BytesIO(img_bytes))

            with io.BytesIO() as buf:
                img_pil.save(buf, format="JPEG")
                img_bytes = buf.getvalue()

        return img_bytes
