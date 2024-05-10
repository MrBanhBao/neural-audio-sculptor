import os
import pickle
import sys
from typing import Union, Dict, List

import torch

import utils.store as store
from configs.stylegan import speed_feature_maps_infos, ws_feature_maps_infos, ws_name_indices_mapping
from core.generators.helpers import init_feature_map_info_dict
from data_models import FeatureMapInfos, StyleGanStore

sys.path.insert(0, os.path.abspath("../backend/libs/stylegan2-ada-pytorch"))


class StyleGan2Ada:
    def __init__(self, model_file: str, device: str = None) -> None:
        self.Gs = None
        self.z_dim: Union[int, None] = None
        self.num_ws: Union[int, None] = None
        self.device: Union[str, None] = None
        self.store: Union[StyleGanStore, None] = None
        self.speed_feature_dict: Dict[str, FeatureMapInfos] = init_feature_map_info_dict(speed_feature_maps_infos)
        self.ws_feature_dict: Dict[str, FeatureMapInfos] = init_feature_map_info_dict(ws_feature_maps_infos)
        self.load_model(model_file, device)

    def load_model(self, model_file: str, device: Union[str, None] = None):
        with open(model_file, "rb") as f:
            try:
                self._set_device(device=device)
                self.Gs = pickle.load(f)["G_ema"].to(self.device)
                self.z_dim = self.Gs.z_dim
                self.num_ws = self.Gs.mapping.num_ws
                self.store = StyleGanStore.random_init(self.z_dim, self.num_ws)
            except Exception as e:
                print(e)

    def _set_device(self, device: Union[str, None] = None) -> None:
        if device is None:
            self.device = torch.device("cuda" if (torch.cuda.is_available()) else "cpu")
        else:
            self.device = device

    def calculate_ws(
        self,
        z: torch.Tensor,
        label: Union[int, None] = None,
        truncation_psi: float = 1.2,
    ) -> torch.Tensor:
        with torch.no_grad():
            ws = self.Gs.mapping(z, label, truncation_psi=truncation_psi)
            return ws

    def calculate_image(self, ws: torch.Tensor, noise_mode: str = "const"):
        img = self.Gs.synthesis(ws, noise_mode=noise_mode)
        return (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

    def forward(self, z: torch.Tensor, truncation_psi: float = 1.2, noise_mode="const"):
        ws = self.Gs.mapping(z, None, truncation_psi=truncation_psi)
        img = self.Gs.synthesis(ws, noise_mode=noise_mode)
        return (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

    def routine(self, index: int, label: Union[int, None] = None, truncation_psi: float = 1.2, noise_mode="const"):
        speed = self._calculate_speed_value(index=index)
        z: torch.Tensor = self.store.z_interpolate
        z_direction: torch.Tensor = self.store.z_direction

        z = z + (z_direction * speed)
        self.store.z_direction = z

        with torch.no_grad():
            ws: torch.Tensor = self.calculate_ws(z=z, label=label, truncation_psi=truncation_psi)
            ws = self._modify_ws(index, ws)

            img = self.calculate_image(ws, noise_mode=noise_mode)

        return img[0].cpu().numpy()

    def _calculate_speed_value(self, index: int) -> float:
        value = 0
        for featureMapInfo in self.speed_feature_dict.values():
            if featureMapInfo.active:
                track_name = featureMapInfo.track_name
                feature_name = featureMapInfo.feature_name
                factor = featureMapInfo.factor

                feature_value = store.audio_features[track_name][feature_name][index]
                value = value + (feature_value*factor)

        return value

    def _modify_ws(self, index: int,  ws: torch.Tensor) -> torch.Tensor:
        for featureMapInfo in self.ws_feature_dict.values():
            feature_info_id: str = featureMapInfo.id
            track_name: str = featureMapInfo.track_name
            feature_name: str = featureMapInfo.feature_name
            factor: float = featureMapInfo.factor

            ws_indices: List[int] = ws_name_indices_mapping[feature_info_id]
            feature_value: float = store.audio_features[track_name][feature_name][index]

            ws[:, ws_indices] = ws[:, ws_indices] + (self.store.ws_direction[:, ws_indices] * feature_value * factor)
        return ws
