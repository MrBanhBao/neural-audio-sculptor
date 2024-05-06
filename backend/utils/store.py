from typing import Dict, List

from data_models import Config, Transform2DArgs, Transform3DArgs

CONFIG_FILE = "../frontend/static/config.yaml"

config: Config = Config.load(config_file=CONFIG_FILE)

args_2D = Transform2DArgs()
args_3D = Transform3DArgs()
# styleGan: StyleGanStore = StyleGanStore()

track_names = ['vocals', 'drums', 'bass', 'piano', 'other']

isFeaturesReady = False
features: Dict[str, Dict[str, List[float]]] = {}