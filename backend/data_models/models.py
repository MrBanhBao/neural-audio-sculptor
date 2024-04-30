from typing import Union, List

import numpy as np
import torch
import yaml
from pydantic import BaseModel


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
    hop_length: int
    block_size: int


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

        if backend.device is None:
            backend.device = torch.device(
                "cuda:0" if (torch.cuda.is_available()) else "cpu"
            )
        return cls(backend=backend, frontend=frontend, audio=audio)


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

    z: Union[torch.Tensor, None] = None
    direction_z: Union[torch.Tensor, None] = None
    ws: Union[torch.Tensor, None] = None
    direction_ws: Union[torch.Tensor, None] = None

    @classmethod
    def random_init(cls, z_dim: int, num_ws: int, device=None):
        """
        Creates a StyleGanStore with random initialized values.

        Parameters:
            z_dim (int): Dimension ot th latent vector z (specified by model)
            num_ws (int): Number of style vector ws (specified by model)
            device (str): Device (cpu, cuda) where tensors are stored.

        Returns:
            StyleGanStore
        """
        z = torch.randn([1, z_dim]).to(device)
        direction_z = torch.from_numpy(np.random.choice([-1, 1], size=[1, z_dim])).to(
            device
        )
        ws = torch.randn([1, num_ws, z_dim]).to(device)
        direction_ws = torch.from_numpy(
            np.random.choice([-1, 1], size=[1, num_ws, z_dim])
        ).to(device)
        return cls(z=z, direction_z=direction_z, ws=ws, direction_ws=direction_ws)


class AudioMetaData(BaseModel):
    artist: str
    title: str
    path: str
    file_name: str
    num_frames: int
    sample_rate: int
    duration: float
    image: str


class StringValue(BaseModel):
    value: str


class FloatValue(BaseModel):
    value: float

class PlaybackState(BaseModel):
    play: bool = False
    loop: bool = True
    mute: bool = False
