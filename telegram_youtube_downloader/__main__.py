from utils.logger_utils import LoggerFactory
from utils.config_utils import ConfigUtils
from cli import Cli


def bootstrap():
    ConfigUtils.init_config()
    LoggerFactory.init_logger()

    cli = Cli()
    cli.start()

if __name__ == "__main__":
    bootstrap()
