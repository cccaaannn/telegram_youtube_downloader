from logging.handlers import RotatingFileHandler
import logging
import pathlib
import sys
import os
import io

from utils.config_utils import ConfigUtils


class LoggerFactory:
    @staticmethod
    def init_logger():
        cfg = ConfigUtils.get_app_config().logger_options

        # log formatter
        formatter = logging.Formatter(
            "[%(name)s] [%(levelname)s] (%(threadName)s) (%(asctime)s) %(message)s", 
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        root_logger = logging.getLogger()
        root_logger.setLevel(cfg.root_log_level)

        app_logger = logging.getLogger("tyd")   # App log prefix
        app_logger.setLevel(cfg.app_log_level)
        app_logger.propagate = False            # Prevent duplicate logs

        # stream handler
        stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        stream_handler = logging.StreamHandler(stream)
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)
        app_logger.addHandler(stream_handler)

        # file handler
        log_path = cfg.log_path
        if(not os.path.isabs(log_path)):
            log_path = os.path.join(os.getcwd(), log_path)

        # Create path
        pathlib.Path(log_path).mkdir(parents=True, exist_ok=True)

        max_bytes = cfg.max_bytes
        backup_count = cfg.backup_count

        log_file_path = os.path.join(log_path, "tyd.log")
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        app_logger.addHandler(file_handler)
