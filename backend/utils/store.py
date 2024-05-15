from typing import Dict, List, Literal

import torch

from configs.transform import mappings_3d_infos
from data_models import (
    Config,
    Transform2DArgs,
    Transform3DArgs
)
from data_models import FeatureMapInfo
from utils.utils import init_feature_map_info_dict

# general configs
CONFIG_FILE = "../frontend/static/config.yaml"
config: Config = Config.load(config_file=CONFIG_FILE)

# transformation
args_2D = Transform2DArgs()
manual_args_3D = Transform3DArgs()
mapping_args_3D = Transform3DArgs()

transform_3d_mapping_dict: Dict[str, FeatureMapInfo] = init_feature_map_info_dict(mappings_3d_infos)
transformation_mode: Literal['mapping', 'manual'] = "mapping"
padding_modes: List[str] = ['border', 'zeros', 'reflection']

# audio
track_names = ["main", "vocals", "drums", "bass", "piano", "other"]
feature_names = ["rms", "pitch", "tempo", "onset", "energy"]
isFeaturesReady = False
audio_features: Dict[str, Dict[str, List[float]]] = {}

# torch
device = torch.device("cuda" if (torch.cuda.is_available()) else "cpu")


generators = ["StyleGan", "StreamDiffusion"]
current_generator: Literal["StyleGan", "StreamDiffusion"] = "StyleGan"