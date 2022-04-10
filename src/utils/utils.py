import argparse
import os

import yaml


class Utils:
    @staticmethod
    def read_cfg_file(path="src/configs/config.yaml"):
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
        return os.environ['TELEGRAM_BOT_KEY']    

    @staticmethod
    def path_type(p):
        if(os.path.isfile(p)):
            return p
        else:
            raise argparse.ArgumentTypeError("File does not exists")

    @staticmethod
    def telegram_bot_exception_handler(logger, function_usage):
        """Logs function and error sends message on error"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    logger.info(f"Function: {func.__name__} User: {args[0].message.from_user}")
                    func(*args, **kwargs)
                except(IndexError, ValueError):
                    logger.warning(f"function: {func.__name__} User: {args[0].message.from_user}")
                    args[0].message.reply_text(f"Usage {function_usage}")
                except:
                    logger.error(f"function: {func.__name__} User:{args[0].message.from_user}", exc_info=True)
                    args[0].message.reply_text("Something went wrong")
            return wrapper
        return decorator
