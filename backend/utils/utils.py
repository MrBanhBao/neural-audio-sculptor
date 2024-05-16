import copy
import io
import json
import os
from typing import List, Union, Dict

import numpy as np
import torch
from PIL import Image
from PIL.Image import Image as PilImage
from numpy import typing as npt

from data_models import File, Folder, Transform3DArgs, FeatureMapInfo


def create_nested_file_structure(root_path: str) -> Folder:
    """
    Function which builds an object with Folders and Files.

    Parameters:
        root_path (str): Path of the root folder/directory.

    Returns:
        Folder: An object which contains nested Folders or Files.
    """  # noqa: E501

    root_name = os.path.basename(__check_path(root_path))
    nested_structure = {
        "name": root_name,
        "files": __create_file_structure(root_path),
    }

    return Folder(**nested_structure)

def list_files(directory):
    files = []
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Check if the path is a file (not a directory)
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return files

def __check_path(path: str) -> str:
    """
    Checks if path ends with a slash or backslash  to prevent os.path.basename
    from returning an empty string.

    Parameters:
        path (str): a path to a folder or file.

    Returns:
        path (str): a path without trailing slash or backslash.
    """  # noqa: E501

    if path[-1] == "/" or path[-1] == "\\":
        path = path[0:-1]

    return path


def __create_file_structure(path: str) -> List[Union[Folder, File]]:
    """
    Creates a list of nested Folder or Files.

    Parameters:
        path (str): a path to a folder or file.

    Returns:
        file_structure (List[Union[Folder, File]]): list of nested Folder or Files.
    """  # noqa: E501

    items = os.listdir(path)
    file_structure: List[Union[Folder, File]] = []

    for item in items:
        if item[0] == ".":
            continue
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folder_item = {
                "name": item,
                "files": __create_file_structure(item_path),
            }
            file_structure.append(Folder(**folder_item))
        elif os.path.isfile(item_path):
            file_item = {"name": item, "path": item_path}
            file_structure.append(File(**file_item))

    return file_structure

def create_directory(path: str) -> None:
    """
    Create a directory if it does not exist.

    Parameters:
        path (str): The path of the directory to be created.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(f"Error creating directory '{path}': {e}")


def is_splitted(files: List[str]) -> bool:
    for file_name in files:
        if not os.path.exists(file_name):
            return False
    return True


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert NumPy arrays to lists
        return json.JSONEncoder.default(self, obj)


def save_dict_as_json(dictionary: Dict, target_file: str):
    with open(target_file, 'w') as json_file:
        json.dump(dictionary, json_file, cls=NumpyEncoder)


def load_json(file: str) -> Dict:
    if os.path.exists(file):
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            return data
    else:
        data = {}
        return data


def normalize_array(x: npt.NDArray) -> npt.NDArray:
    return (x-np.min(x))/(np.max(x)-np.min(x))


def img_array_to_image_byte_pil(img_array: torch.Tensor, format: str = "JPEG") -> bytes:
    img = Image.fromarray(img_array)
    with io.BytesIO() as buf:
        img.save(buf, format=format)
        img_bytes = buf.getvalue()
        return img_bytes


def img_pil_to_bytes(img: PilImage, format: str = "JPEG") -> bytes:
    with io.BytesIO() as buf:
        img.save(buf, format=format)
        img_bytes = buf.getvalue()
        return img_bytes

def init_feature_map_info_dict(feature_infos: List[FeatureMapInfo]) -> Dict[str, FeatureMapInfo]:
    feature_maps_info = {}
    for info in feature_infos:
        feature_maps_info[info.id] = info

    return feature_maps_info

def set_transform3d_maps(index: int, args:Transform3DArgs,
                         map_infos: List[FeatureMapInfo],
                         feature_dict: Dict[str, Dict[str, List[float]]]):
    args_copy = copy.deepcopy(args)
    for map_info in map_infos:
        feat_id: str = map_info.id
        track_name: str = map_info.track_name
        feature_name: str = map_info.feature_name
        factor: float = map_info.factor
        feature_value: float = feature_dict[track_name][feature_name][index+1] - feature_dict[track_name][feature_name][index]
        value = feature_value * factor
        if map_info.active:
            setattr(args_copy, feat_id, getattr(args_copy, feat_id) + value)
        else:
            setattr(args_copy, feat_id, getattr(args_copy, feat_id))
    return args_copy
