from typing import Dict, List

from data_models import FeatureMapInfos


def init_feature_map_info_dict(feature_infos: List[FeatureMapInfos]) -> Dict[str, FeatureMapInfos]:
    feature_maps_info = {}
    for info in feature_infos:
        feature_maps_info[info.id] = info

    return feature_maps_info

