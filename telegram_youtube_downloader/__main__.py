from telegram_youtube_downloader.cli import Cli
from telegram_youtube_downloader.utils.config_utils import ConfigUtils
from telegram_youtube_downloader.utils.logger_utils import LoggerFactory


def bootstrap():
	ConfigUtils.init_config()
	LoggerFactory.init_logger()

	cli = Cli()
	cli.start()


if __name__ == "__main__":
	bootstrap()
