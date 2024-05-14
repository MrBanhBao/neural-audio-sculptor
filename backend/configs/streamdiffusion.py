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