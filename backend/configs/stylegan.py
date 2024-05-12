import uuid
from typing import List

from data_models.models import FeatureMapInfo

speed_feature_maps_infos: List[FeatureMapInfo] = [
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="vocals",
            feature_name="energy",
            factor=1.5,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="drums",
            feature_name="onset",
            factor=2.5,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="bass",
            feature_name="rms",
            factor=1,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="piano",
            feature_name="pitch",
            factor=1,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="other",
            feature_name="rms",
            factor=1,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="main",
            feature_name="rms",
            factor=1,
        ),
    ]


ws3_steps = {
    "ws0_2": [0, 1, 2],
    "ws3_5": [3, 4, 5],
    "ws6_8": [6, 7, 8],
    "ws9_11": [9, 10, 11],
    "ws12_14": [12, 13, 14],
    "ws15": [15],
}

ws2_steps = {
    "ws1-2": [0, 1],
    "ws3-4": [2, 3],
    "ws5-6": [4, 5],
    "ws7-8": [6, 7],
    "ws9-10": [8, 9],
    "ws11-12": [10, 11],
    "ws13-14": [12, 13],
    "ws15-16": [14, 15],
}

ws1_steps = {
    "ws1": [0],
    "ws2": [1],
    "ws3": [2],
    "ws4": [3],
    "ws5": [4],
    "ws6": [5],
    "ws7": [6],
    "ws8": [7],
    "ws9": [8],
    "ws10": [9],
    "ws11": [10],
    "ws12": [11],
    "ws13": [12],
    "ws14": [13],
    "ws15": [14],
    "ws16": [15]
}

ws_name_indices_mapping = ws2_steps

list3_steps = [
        FeatureMapInfo.init(
            id="ws0_2",
            active=True,
            track_name="vocals",
            feature_name="energy",
            factor=0.3,
        ),
        FeatureMapInfo.init(
            id="ws3_5",
            active=True,
            track_name="drums",
            feature_name="onset",
            factor=0.3,
        ),
        FeatureMapInfo.init(
            id="ws6_8",
            active=True,
            track_name="bass",
            feature_name="rms",
            factor=0.3,
        ),
        FeatureMapInfo.init(
            id="ws9_11",
            active=True,
            track_name="piano",
            feature_name="pitch",
            factor=0.3,
        ),
        FeatureMapInfo.init(
            id="ws12_14",
            active=True,
            track_name="other",
            feature_name="rms",
            factor=0.3,
        ),
        FeatureMapInfo.init(
            id="ws12_14",
            active=True,
            track_name="main",
            feature_name="rms",
            factor=0.3,
        ),
        FeatureMapInfo.init(
            id="ws15",
            active=True,
            track_name="main",
            feature_name="rms",
            factor=0.3,
        ),
    ]

list2step = [
    FeatureMapInfo(id="ws1-2", active=True, track_name="drums", feature_name="rms", factor=3),
    FeatureMapInfo(id="ws3-4", active=True, track_name="vocals", feature_name="rms", factor=3),
    FeatureMapInfo(id="ws5-6", active=True, track_name="other", feature_name="rms", factor=3),
    FeatureMapInfo(id="ws7-8", active=True, track_name="bass", feature_name="rms", factor=3),
    FeatureMapInfo(id="ws9-10", active=True, track_name="piano", feature_name="rms", factor=3),
    FeatureMapInfo(id="ws11-12", active=False, track_name="drums", feature_name="rms", factor=3),
    FeatureMapInfo(id="ws13-14", active=False, track_name="drums", feature_name="rms", factor=3),
    FeatureMapInfo(id="ws15-16", active=False, track_name="main", feature_name="rms", factor=3)]

list1step = [
    FeatureMapInfo(id="ws1", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws2", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws3", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws4", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws5", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws6", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws7", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws8", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws9", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws10", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws11", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws12", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws13", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws14", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws15", active=True, track_name="drums", feature_name="rms", factor=1),
    FeatureMapInfo(id="ws16", active=True, track_name="drums", feature_name="rms", factor=1)
]
ws_feature_maps_infos: List[FeatureMapInfo] = list2step