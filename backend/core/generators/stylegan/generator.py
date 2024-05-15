import os
import pickle
import sys
from typing import Union, Dict, List

import numpy as np
import torch

import utils.store as store
from configs.stylegan import speed_feature_maps_infos, ws_feature_maps_infos, ws_name_indices_mapping
from core.generators.utils import has_passed, create_direction_vector
from core.transformations.geometric_transformations import transform_3D, transform_2D
from data_models import FeatureMapInfo, StyleGanStore, Transform3DArgs, Transform2DArgs
from utils.utils import init_feature_map_info_dict

sys.path.insert(0, os.path.abspath("../backend/libs/stylegan2-ada-pytorch"))

class StyleGan2Ada:
    def __init__(self, model_file: str, device: str = None) -> None:
        self.Gs = None
        self.z_dim: Union[int, None] = None
        self.num_ws: Union[int, None] = None
        self.device: Union[str, None] = None
        self.store: Union[StyleGanStore, None] = None
        self.speed_feature_dict: Dict[str, FeatureMapInfo] = init_feature_map_info_dict(speed_feature_maps_infos)
        self.ws_feature_dict: Dict[str, FeatureMapInfo] = init_feature_map_info_dict(ws_feature_maps_infos)
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

    def calculate_image_with_transformation(self, ws: torch.Tensor, target_layer_idx: int = 3, noise_mode: str = "const",
                                            transform_args: Union[Transform2DArgs, Transform3DArgs, None] = None):
        w_idx = 0
        x = None
        img_tensor = None

        for layer_idx, block in enumerate(self.Gs.synthesis.children()):
            cur_ws = ws.narrow(1, w_idx, block.num_conv + block.num_torgb)
            x, img_tensor = block(x, img_tensor, cur_ws, noise_mode=noise_mode)

            if layer_idx == target_layer_idx:
                if isinstance(transform_args, Transform3DArgs):
                    x = transform_3D(tensor=x,
                                     rotate_x=transform_args.rotate_x,
                                     rotate_y=transform_args.rotate_y,
                                     rotate_z=transform_args.rotate_z,
                                     translate_x=transform_args.translate_x,
                                     translate_y=transform_args.translate_y,
                                     translate_z=transform_args.translate_z,
                                     padding_mode=transform_args.padding_mode)
                elif isinstance(transform_args, Transform2DArgs):
                    x = transform_2D(tensor=x,
                                     rotate_angle=transform_args.rotate_angle,
                                     translate_x=transform_args.translate_x,
                                     translate_y=transform_args.translate_y,
                                     scale_x=transform_args.scale_x,
                                     scale_y=transform_args.scale_y,
                                     padding_mode=transform_args.padding_mode)
                else:
                    pass
            w_idx += block.num_conv

        return (img_tensor.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

    def forward(self, z: torch.Tensor, truncation_psi: float = 1.2, noise_mode="const"):
        ws = self.Gs.mapping(z, None, truncation_psi=truncation_psi)
        img = self.Gs.synthesis(ws, noise_mode=noise_mode)
        return (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

    def routine(self, index: int, label: Union[int, None] = None,
                truncation_psi: float = 1.2, noise_mode="const",
                transform_args: Union[Transform2DArgs, Transform3DArgs, None] = None):
        speed = self._calculate_speed_value(index=index)
        z_interpolate: torch.Tensor = self.store.z_interpolate
        z_direction: torch.Tensor = self.store.z_direction
        z_target: torch.Tensor = self.store.z_target

        z_interpolate = z_interpolate + (z_direction * speed)

        with torch.no_grad():
            ws: torch.Tensor = self.calculate_ws(z=z_interpolate, label=label, truncation_psi=truncation_psi)
            ws = self._modify_ws(index, ws)


            if transform_args:
                img = self.calculate_image_with_transformation(ws=ws, target_layer_idx=3, transform_args=transform_args)
            else:
                img = self.calculate_image(ws, noise_mode=noise_mode)

        # change target when it was reached
        if has_passed(z_interpolate, z_target, z_direction):
            self.store.z_start = z_target
            self.store.z_target = torch.randn([1, self.z_dim]).to(self.device)
            self.store.z_direction = create_direction_vector(self.store.z_start, self.store.z_target)
            self.store.ws_direction = torch.from_numpy(np.random.choice([-1, 1], size=[1, self.num_ws, self.z_dim])).to(self.device)

        # Update store
        self.store.z_interpolate = z_interpolate

        return img[0].cpu().numpy()

    def _calculate_speed_value(self, index: int) -> float:
        value = 0
        if store.audio_features:
            for featureMapInfo in self.speed_feature_dict.values():
                if featureMapInfo.active:
                    track_name = featureMapInfo.track_name
                    feature_name = featureMapInfo.feature_name
                    factor = featureMapInfo.factor

                    feature_value = store.audio_features[track_name][feature_name][index]
                    value = value + (feature_value*factor)
        return value

    def _modify_ws(self, index: int,  ws: torch.Tensor) -> torch.Tensor:
        if store.audio_features:
            for featureMapInfo in self.ws_feature_dict.values():
                if featureMapInfo.active:
                    feature_info_id: str = featureMapInfo.id
                    track_name: str = featureMapInfo.track_name
                    feature_name: str = featureMapInfo.feature_name
                    factor: float = featureMapInfo.factor

                    ws_indices: List[int] = ws_name_indices_mapping[feature_info_id]
                    feature_value: float = store.audio_features[track_name][feature_name][index]

                    ws[:, ws_indices] = ws[:, ws_indices] + (self.store.ws_direction[:, ws_indices] * feature_value * factor)
        return ws

    def get_speed_feature_infos(self) -> List[FeatureMapInfo]:
        return list(self.speed_feature_dict.values())

    def modify_speed_feature_dict(self, featureMapInfo: FeatureMapInfo) -> bool:
        try:
            feat_id = featureMapInfo.id
            self.speed_feature_dict[feat_id] = featureMapInfo
            return True
        except Exception as e:
            print(e)
            return False

    def delete_speed_feature_dict(self, featureMapInfo: FeatureMapInfo) -> bool:
        try:
            feat_id = featureMapInfo.id
            del self.speed_feature_dict[feat_id]
            return True
        except Exception as e:
            print(e)
            return False

    def get_ws_feature_infos(self) -> List[FeatureMapInfo]:
        return list(self.ws_feature_dict.values())

    def modify_ws_feature_dict(self, featureMapInfo: FeatureMapInfo):
        try:
            feat_id = featureMapInfo.id
            self.ws_feature_dict[feat_id] = featureMapInfo
            return True
        except Exception as e:
            print(e)
            return False

    def delete_ws_feature_dict(self, featureMapInfo: FeatureMapInfo):
        try:
            feat_id = featureMapInfo.id
            del self.ws_feature_dict[feat_id]
            return True
        except Exception as e:
            print(e)
            return False
