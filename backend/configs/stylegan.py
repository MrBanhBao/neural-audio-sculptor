import uuid
from typing import List

from data_models.models import FeatureMapInfos

speed_feature_maps_infos: List[FeatureMapInfos] = [
        FeatureMapInfos.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="vocals",
            feature_name="energy",
            factor=1,
        ),
        FeatureMapInfos.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="drums",
            feature_name="onset",
            factor=1,
        ),
        FeatureMapInfos.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="bass",
            feature_name="rms",
            factor=1,
        ),
        FeatureMapInfos.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="piano",
            feature_name="pitch",
            factor=1,
        ),
        FeatureMapInfos.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="other",
            feature_name="rms",
            factor=1,
        ),
    ]


ws_name_indices_mapping = {
    "ws0_2": [0, 1, 2],
    "ws3_5": [3, 4, 5],
    "ws6_8": [6, 7, 8],
    "ws9_11": [9, 10, 11],
    "ws12_14": [12, 13, 14],
    "ws15_16": [15, 16],
}


ws_feature_maps_infos: List[FeatureMapInfos] = [
        FeatureMapInfos.init(
            id="ws0_2",
            active=True,
            track_name="vocals",
            feature_name="energy",
            factor=0.3,
        ),
        FeatureMapInfos.init(
            id="ws3_5",
            active=True,
            track_name="drums",
            feature_name="onset",
            factor=0.3,
        ),
        FeatureMapInfos.init(
            id="ws6_8",
            active=True,
            track_name="bass",
            feature_name="rms",
            factor=0.3,
        ),
        FeatureMapInfos.init(
            id="ws9_11",
            active=True,
            track_name="piano",
            feature_name="pitch",
            factor=0.3,
        ),
        FeatureMapInfos.init(
            id="ws12_14",
            active=True,
            track_name="other",
            feature_name="rms",
            factor=0.3,
        ),
        FeatureMapInfos.init(
            id="ws12_14",
            active=True,
            track_name="main",
            feature_name="rms",
            factor=0.3,
        ),
    ]