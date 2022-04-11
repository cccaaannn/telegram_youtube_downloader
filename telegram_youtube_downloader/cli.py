import argparse
import sys
import os

from telegram_bot import TelegramBot

from utils.logger_factory import LoggerFactory
from utils.utils import Utils


class Cli:
    def __init__(self) -> None:
        self.telegram_options = Utils.read_cfg_file()["telegram_bot_options"]
        self.bot_key_env_name = self.telegram_options["bot_key_env_variable_name"]
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__, file_handler=False)

    def start(self):
        parser = argparse.ArgumentParser(description="Youtube telegram downloader", epilog=f"Uses environment variable <{self.bot_key_env_name}> for the Telegram bot key if no arguments passed")
        mutually_exclusive_group = parser.add_mutually_exclusive_group()
        mutually_exclusive_group.add_argument("-k", "--use_key", dest="use_key", metavar="<key>", type=str, help="Telegram bot key")
        mutually_exclusive_group.add_argument("-f", "--use_file", dest="use_file", metavar="<path>", type=Utils.path_type, help="File path for Telegram bot key")

        # Get arguments
        args = parser.parse_args()
        if(args.use_key):
            os.environ[self.bot_key_env_name] = args.use_key
        elif(args.use_file):
            os.environ[self.bot_key_env_name] = Utils.read_file(args.use_file)

        if(not os.environ.get(self.bot_key_env_name, None)):
            self.__logger.error(f"A telegram bot key must presents at {self.bot_key_env_name} environment variable")
            sys.exit(1)

        # Start bot
        tb = TelegramBot()
        tb.start()



if __name__ == "__main__":
    cli = Cli()
    cli.start()
