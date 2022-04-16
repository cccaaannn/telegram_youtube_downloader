import argparse
import sys
import os

from telegram_bot import TelegramBot

from utils.logger_factory import LoggerFactory
from utils.utils import Utils
from utils.statics import Statics


class Cli:
    def __init__(self) -> None:
        self.bot_key_env_name = Statics.TELEGRAM_BOT_ENVIRONMENT_NAME
        self.youtube_api_key_env_name = Statics.YOUTUBE_API_ENVIRONMENT_NAME
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__, file_handler=False)

    def start(self):
        parser = argparse.ArgumentParser(description="Youtube telegram downloader", epilog=f"Uses environment variable <{self.bot_key_env_name}> for the Telegram bot key if no arguments passed")
        mutually_exclusive_group = parser.add_mutually_exclusive_group()
        mutually_exclusive_group.add_argument("-k", "--use_key", dest="use_key", metavar="<key>", type=str, help="Telegram bot and YouTube api key")
        mutually_exclusive_group.add_argument("-f", "--use_file", dest="use_file", metavar="<path>", type=Utils.path_type, help="File path for Telegram bot and YouTube api key")

        # Get arguments
        args = parser.parse_args()
        if(args.use_key):
            api_keys = args.use_key.split(",")
            if(len(api_keys) == 2):
                os.environ[self.youtube_api_key_env_name] = api_keys[1]
            os.environ[self.bot_key_env_name] = api_keys[0]

        elif(args.use_file):
            api_keys = Utils.read_file_lines(args.use_file)
            if(len(api_keys) == 2):
                os.environ[self.youtube_api_key_env_name] = api_keys[1]
            os.environ[self.bot_key_env_name] = api_keys[0]
            
        if(not os.environ.get(self.bot_key_env_name, None)):
            self.__logger.error(f"A telegram bot key must presents at {self.bot_key_env_name} environment variable")
            sys.exit(1)

        # Start bot
        tb = TelegramBot()
        tb.start()



if __name__ == "__main__":
    cli = Cli()
    cli.start()
