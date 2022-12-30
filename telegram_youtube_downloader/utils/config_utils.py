import os

import yaml


class ConfigUtils:
    @staticmethod
    def read_cfg_file(path="telegram_youtube_downloader/configs/config.yaml"):
        abs_path = os.path.join(os.getcwd(), path)
        with open(abs_path, "r") as file:
            cfg = yaml.safe_load(file)
        return cfg
