from collections import deque
from typing import Union, List, Literal

import numpy as np
import torch
import yaml
from PIL.Image import Image as PilImage
from pydantic import BaseModel

from core.generators.utils import create_direction_vector


class BackendConfig(BaseModel):
    """
    Represents the configurations for the backend part of the application.

    Attributes:
        host (str): IP of the host of the API server.
        port (int): Port number of the running API server.
        device (Union[str, None]): Device torch/tensorflow operation will be running on.
        cache_dir (str): Path of the cache directory.
        music_dir (str): Path of the music directory.
        stylegan_checkpoints (str): Directory containing checkpoint files for the StyleGan generator.
    """

    class Config:
        arbitrary_types_allowed = True

    host: str
    port: int
    device: Union[str, None]
    cache_dir: str
    music_dir: str
    stylegan_checkpoints: str


class FrontendConfig(BaseModel):
    """
    Represents the configurations for the frontend part of the application.

    Attributes:
        host (str): IP of the host of the API server.
        port (int): Port number of the running API server.
    """

    host: str
    port: int


class AudioConfig(BaseModel):
    """
    Represents the configurations for audio settings.

    Attributes:
        host (str): IP of the host of the API server.
        hop_length (int): Port number of the running API server.
    """

    sample_rate: int
    block_size: int
    hop_length: int
    frame_length: int


class StreamDiffusionConfig(BaseModel):
    image_inputs: str
    model_id: str
    t_index_list: List[int]

class Config(BaseModel):
    """
    Represents the configurations for the backend and frontend part of the application.

    Attributes:
        backend (BackendConfig): configurations for the backend part of the application.
        frontend (FrontendConfig): configurations for the frontend part of the application.
    """

    backend: BackendConfig
    frontend: FrontendConfig
    audio: AudioConfig
    stream_diffusion: StreamDiffusionConfig

    @classmethod
    def load(cls, config_file):
        """
        Loads config yaml file and creates a configuration object.

        Parameters:
            config_file (str): path to config file.

        Returns:
            Config: Config objects holding information of given configurations.
        """
        with open(config_file) as f:
            config_dict = yaml.safe_load(f)
            backend = BackendConfig(**config_dict["backend"])
            frontend = FrontendConfig(**config_dict["frontend"])
            audio = AudioConfig(**config_dict["audio"])
            stream_diffusion = StreamDiffusionConfig(**config_dict["stream_diffusion"])

        if backend.device is None:
            backend.device = torch.device(
                "cuda" if (torch.cuda.is_available()) else "cpu"
            )
        return cls(backend=backend, frontend=frontend, audio=audio, stream_diffusion=stream_diffusion)


class File(BaseModel):
    """
    Represents a File.

    Attributes:
        name (str): Name of the file.
        path (int): Path of the file.
    """

    name: str
    path: str


class Folder(BaseModel):
    """
    Represents a folder which contains nested Files and Folders.

    Attributes:
        name (str): Name of the Folder.
        files (List[Union[File, "Folder"]]): List of nested Files and Folders.
    """

    name: str
    files: List[Union[File, "Folder"]]


class Transform2DArgs(BaseModel):
    """
    Represents arguments for the 2D matrix transformations

    Attributes:
        rotate_angle (float): Degree value for rotation.
        translate_x (float): Translate value for translating in (left/right).
        translate_y (float): Translate value for translating in (up/down).
        scale_x (float): Scale value in width.
        scale_y (float): Scale value in height.
    """
    padding_mode: Literal['border', 'zeros', 'reflection'] = "reflection"
    rotate_angle: float = 0
    translate_x: float = 0
    translate_y: float = 0
    scale_x: float = 1
    scale_y: float = 1


class Transform3DArgs(BaseModel):
    """
    Represents arguments for the DD matrix transformations.

    Attributes:
        rotate_x (float): Value for rotation on x-axis.
        rotate_y (float): Value for rotation on y-axis.
        rotate_z (float): Value for rotation on z-axis.
        translate_x (float): Value for translation on x-axis.
        translate_y (float): Value for translation on y-axis.
        translate_z (float): Value for translation on z-axis.
    """
    padding_mode: Literal['border', 'zeros', 'reflection'] = "reflection"
    rotate_x: float = 0
    rotate_y: float = 0
    rotate_z: float = 0
    translate_x: float = 0
    translate_y: float = 0
    translate_z: float = 0


class StyleGanStore(BaseModel):
    """
    Holds information for the image synthesis process of the StyleGan model.

    Attributes:
        z Union[torch.Tensor, None]: Latent vector z.
        direction_z Union[torch.Tensor, None]: Direction vector added to z.
        ws Union[torch.Tensor, None]: Style vector ws.
        direction_ws Union[torch.Tensor, None]: Direction vector added to ws.
    """

    class Config:
        arbitrary_types_allowed = True

    z_start: Union[torch.Tensor, None] = None
    z_target: Union[torch.Tensor, None] = None
    z_interpolate: Union[torch.Tensor, None] = None
    z_direction: Union[torch.Tensor, None] = None
    ws_direction: Union[torch.Tensor, None] = None

    @classmethod
    def random_init(cls, z_dim: int, num_ws: int, device=None):
        """
        Creates a StyleGanStore with random initialized values.

        Parameters:
            z_dim (int): Dimension ot th latent vector z (specified by generator model)
            num_ws (int): Number of style vector ws (specified by generator model)
            device (str): Device (cpu, cuda) where tensors are going to be stored.

        Returns:
            StyleGanStore
        """
        if device is None:
            device = torch.device("cuda" if (torch.cuda.is_available()) else "cpu")

        z_start = torch.randn([1, z_dim]).to(device)
        z_target = torch.randn([1, z_dim]).to(device)
        z_direction = create_direction_vector(z_start, z_target).to(device)

        ws_direction = torch.from_numpy(
            np.random.choice([-1, 1], size=[1, num_ws, z_dim])
        ).to(device)
        return cls(
            z_start=z_start,
            z_target=z_target,
            z_interpolate=z_start,
            z_direction=z_direction,
            ws_direction=ws_direction,
        )


class AudioMetaData(BaseModel):
    artist: Union[str, None]
    title: Union[str, None]
    path: str
    file_name: str
    num_frames: int
    sample_rate: int
    duration: float


class StringValue(BaseModel):
    value: Union[str, None]


class FloatValue(BaseModel):
    value: float


class IntegerValue(BaseModel):
    value: int


class BooleanValue(BaseModel):
    value: bool


class PlaybackState(BaseModel):
    play: bool = False
    loop: bool = True
    mute: bool = False


class SelectedAudioTrack(BaseModel):
    name: str
    active: bool


class FeatureMapInfo(BaseModel):
    id: Union[str, int]
    active: bool
    track_name: str
    feature_name: str
    factor: float

    @classmethod
    def init(
        cls, id: Union[str, int], active: bool, track_name: str, feature_name: str, factor: float
    ):
        return cls(
            id=id,
            active=active,
            track_name=track_name,
            feature_name=feature_name,
            factor=factor,
        )


class StreamDiffusionStore(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    prompt: Union[str, None] = None
    sampled_file_names: deque = None

    image_pil_start: Union[PilImage, None] = None
    image_latent_start: Union[torch.Tensor, None] = None

    image_pil_target: Union[PilImage, None] = None
    image_latent_target: Union[torch.Tensor, None] = None

    image_pil_next: Union[PilImage, None] = None
    image_latent_next: Union[torch.Tensor, None] = None

    image_interpolate_pil: Union[torch.Tensor, None] = None
    image_interpolate_latent: Union[torch.Tensor, None] = None

    direction_vector: Union[torch.Tensor, None] = None
    latent_direction: Union[torch.Tensor, None] = None


class ImageData(BaseModel):
    image: str


class ImageInputPreviewData(BaseModel):
    name: str
    path: str
    images: List[str]


class Landmark(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0