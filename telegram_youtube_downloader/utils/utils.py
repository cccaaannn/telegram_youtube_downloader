import argparse
import os

import yaml

from utils.statics import Statics


class Utils:
    @staticmethod
    def read_cfg_file(path="telegram_youtube_downloader/configs/config.yaml"):
        abs_path = os.path.join(os.getcwd(), path)
        with open(abs_path, "r") as file:
            cfg = yaml.safe_load(file)
        return cfg

    @staticmethod
    def read_file(file_name):
        with open(file_name,'r', encoding='utf-8') as file:
            content = file.read()
            return content

    @staticmethod
    def get_telegram_bot_key():
        return os.environ.get(Statics.TELEGRAM_BOT_ENVIRONMENT_NAME, None)

    @staticmethod
    def get_youtube_api_key():
        return os.environ.get(Statics.YOUTUBE_API_ENVIRONMENT_NAME, None)

    @staticmethod
    def path_type(p):
        if(os.path.isfile(p)):
            return p
        else:
            raise argparse.ArgumentTypeError("File does not exists")

    @staticmethod
    def video_title_formatter(title, duration, title_length=45):
        formatted_title = f"({duration}) {title}"

        if(len(formatted_title) > title_length):
            formatted_title = formatted_title[:title_length]
            formatted_title += "..."

        return formatted_title