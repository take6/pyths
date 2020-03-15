import os
import toml


def load_config():
    home_dir = os.getenv('HOME')
    config_dir = '.pyths'
    config_file = os.path.join(home_dir, config_dir, 'config.toml')
    if os.path.exists(config_file):
        config = toml.load(config_file)
    else:
        config = {}

    return config


CONFIG = load_config()
