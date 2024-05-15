import os
import random
from typing import Literal, Optional, Dict, Tuple, List, Union

import torch
from PIL import Image
from PIL.Image import Image as PilImage

import utils.store as store
from configs.streamdiffusion import speed_feature_maps_infos
from core.generators.stream_diffusion.utis import StreamDiffusionWrapper
from core.generators.utils import create_direction_vector, has_passed
from core.transformations.geometric_transformations import transform_3D, transform_2D
from data_models import Transform2DArgs, Transform3DArgs, StreamDiffusionStore, FeatureMapInfo
from utils import list_files
from utils.utils import init_feature_map_info_dict


class StreamDiffuser:
    def __init__(self,
                 image_dir: str,
                 prompt: str = "",
                 negative_prompt: str = "low quality, bad quality, blurry, low resolution",
                 model_id_or_path: str = "JamesFlare/pastel-mix",
                 lora_dict: Optional[Dict[str, float]] = None,
                 width: int = 512,
                 height: int = 512,
                 acceleration: Literal["none", "xformers", "tensorrt"] = "tensorrt",
                 use_denoising_batch: bool = True,
                 guidance_scale: float = 20,
                 cfg_type: Literal["none", "full", "self", "initialize"] = "none",
                 seed: int = 2,
                 similar_image_filter_threshold: float = 0.98,
                 t_index_list=[32, 49], frame_buffer_size=1, warmup=10,  model="img2img", output_type='pil'):
        self.speed_feature_dict: Dict[str, FeatureMapInfo] = init_feature_map_info_dict(speed_feature_maps_infos)
        self.image_dir = image_dir
        self.img_file_list: Union[List[str]] = list_files(image_dir)
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.store = StreamDiffusionStore()

        if guidance_scale <= 1.0:
            cfg_type = "none"

        self.stream = StreamDiffusionWrapper(model_id_or_path=model_id_or_path,
            lora_dict=lora_dict,
            dtype=torch.float32,
            t_index_list=t_index_list,
            frame_buffer_size=frame_buffer_size,
            width=width,
            height=height,
            warmup=warmup,
            acceleration=acceleration,
            mode=model,
            use_denoising_batch=use_denoising_batch,
            cfg_type=cfg_type,
            seed=seed,
            similar_image_filter_threshold=similar_image_filter_threshold,
            output_type=output_type)

        self._init()

    def _init(self):
        self._prepare()
        self._warmup()
        self.fill_store()

    def _prepare(self):
        self.stream.prepare(
            prompt=self.prompt,
            negative_prompt=self.negative_prompt,
            num_inference_steps=50,
        )

    def _warmup(self):
        for _ in range(self.stream.batch_size - 1):
            self.stream.latent2img(latent=self.store.stream_diffusion.image_latent_1)

    def fill_store(self):
        index_word = {
            0: "start",
            1: "target",
            3: "next"
        }

        random_img_files = random.sample(self.img_file_list, 3)
        self.store.sampled_file_names = random_img_files

        for i, file in enumerate(random_img_files):
            image_pil: PilImage = Image.open(os.path.join(self.image_dir, file))
            image_tensor = self.stream.preprocess_image(image_pil)
            image_latent = self.stream.stream.encode_image(image_tensor)

            setattr(self.store, f'image_pil_{index_word[i]}', image_pil)
            setattr(self.store, f'image_latent_{index_word[i]}', image_latent)

            if i == 0:
                self.store.interpolate_pil = image_pil
                self.store.interpolate_latent = image_latent

        self.store.direction_vector = create_direction_vector(self.store.image_latent_start, self.store.image_latent_targe)

    def routine(self, index: int, scale: int = 2, transform_args: Union[Transform2DArgs, Transform3DArgs, None] = None) -> PilImage:
        speed = self._calculate_speed_value(index=index)
        interpolate_latent: torch.Tensor = self.store.image_interpolate_latent
        direction_vector: torch.Tensor = self.store.direction_vector
        target_latent: torch.Tensor = self.store.image_latent_target
        # modify interpolate latent
        interpolate_latent = interpolate_latent + (speed * direction_vector)

        image_out = self.stream.latent2img(latent=interpolate_latent)
        # Do transformation if args are given
        if transform_args:
            image_out = self._transform_interpolated_image(image_out, transform_args)
        image_out = self.stream.postprocess_image(image_out)
        image_out = image_out.resize((self.stream.width*scale, self.stream.height*scale), Image.Resampling.LANCZOS)

        if has_passed(interpolate_latent, target_latent, direction_vector):
            self.store.image_pil_start = self.store.image_latent_target
            self.store.image_latent_start = self.store.image_latent_target

            # get new image file
            random_image_file = random.sample(self.img_file_list, 1)[0]
            while random_image_file in self.store.file_names:
                print('resampling!!!!!!!!!!!!!!')
                random_image_file = random.sample(self.img_file_list, 1)[0]
            self.store.sampled_file_names.append(random_image_file) # add random image file
            self.store.sampled_file_names.popleft() # remove start image file

            image_pil = Image.open(os.path.join(self.image_dir, random_image_file))
            image_array, image_latent = self._transform_interpolated_image(image_pil, transform_args)
            self.store.image_pil_target = image_pil
            self.store.image_latent_target = image_latent

            self.store.direction_vector = create_direction_vector(self.store.image_latent_start, self.store.image_latent_targe)

        return image_out

    def _transform_interpolated_image(self, image: PilImage, transform_args: Transform3DArgs) -> Tuple[torch.Tensor, torch.Tensor]:
        args = transform_args.dict()
        image_tensor: torch.Tensor = self.stream.preprocess_image(image)
        if isinstance(transform_args, Transform3DArgs):
            image_tensor: torch.Tensor = transform_3D(image_tensor, **args)
        else:
            image_tensor: torch.Tensor = transform_2D(image_tensor, **args)
        image_latent: torch.Tensor = self.stream.stream.encode_image(image_tensor)
        return image_tensor, image_latent

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
