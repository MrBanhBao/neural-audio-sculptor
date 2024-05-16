from data_models.models import FeatureMapInfo

mappings_3d_infos = [
    FeatureMapInfo(id="translate_x", active=False, track_name="other", feature_name="rms", factor=0.1),
    FeatureMapInfo(id="translate_y", active=False, track_name="vocals", feature_name="rms", factor=0.1),
    FeatureMapInfo(id="translate_z", active=True, track_name="drums", feature_name="rms", factor=0.1),
    FeatureMapInfo(id="rotate_x", active=False, track_name="bass", feature_name="rms", factor=0.1),
    FeatureMapInfo(id="rotate_y", active=False, track_name="piano", feature_name="rms", factor=0.1),
    FeatureMapInfo(id="rotate_z", active=False, track_name="drums", feature_name="rms", factor=0.1),
]