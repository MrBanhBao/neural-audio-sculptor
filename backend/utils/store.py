from data_models import Config, Transform2DArgs, Transform3DArgs

CONFIG_FILE = "../config.yaml"

config: Config = Config.load(config_file=CONFIG_FILE)

args_2D = Transform2DArgs()
args_3D = Transform3DArgs()
# styleGan: StyleGanStore = StyleGanStore()
