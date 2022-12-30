import logging
import pathlib
import os

from utils.config_utils import ConfigUtils


class LoggerFactory:
    @staticmethod
    def get_logger(logger_name, file_handler=True):
        """creates logger"""

        cfg = ConfigUtils.read_cfg_file()["logger_options"]
        logger = logging.getLogger(logger_name)
        if(not logger.handlers):

            logger.setLevel(cfg["log_level"])

            # log formatter
            formatter = logging.Formatter(f"[{logger_name}] [%(levelname)s] (%(threadName)s) (%(asctime)s) %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
            
            # stream handler
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            # file handler
            if(file_handler):
                log_path = cfg["log_path"]
                if(not os.path.isabs(log_path)):
                    log_path = os.path.join(os.getcwd(), log_path)

                # Create path
                pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)

                log_file_path = os.path.join(log_path, logger_name + ".log")
                file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        return logger