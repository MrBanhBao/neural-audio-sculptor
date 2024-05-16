import uuid
from typing import List

from data_models.models import FeatureMapInfo

speed_feature_maps_infos: List[FeatureMapInfo] = [
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=True,
            track_name="vocals",
            feature_name="rms",
            factor=5
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=False,
            track_name="drums",
            feature_name="onset",
            factor=2.5,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=False,
            track_name="bass",
            feature_name="rms",
            factor=1,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=False,
            track_name="piano",
            feature_name="pitch",
            factor=1,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=False,
            track_name="other",
            feature_name="rms",
            factor=1,
        ),
        FeatureMapInfo.init(
            id=str(uuid.uuid4()),
            active=False,
            track_name="main",
            feature_name="rms",
            factor=1,
        ),
    ]

latent_feature_maps_info: List[FeatureMapInfo] = [
        FeatureMapInfo.init(
            id=0,
            active=True,
            track_name="bass",
            feature_name="rms",
            factor=2
        ),
        FeatureMapInfo.init(
            id=1,
            active=False,
            track_name="vocals",
            feature_name="rms",
            factor=1.2
        ),
        FeatureMapInfo.init(
            id=2,
            active=True,
            track_name="drums",
            feature_name="rms",
            factor=1.2
        ),
        FeatureMapInfo.init(
            id=3,
            active=False,
            track_name="vocals",
            feature_name="rms",
            factor=1.2
        )
]