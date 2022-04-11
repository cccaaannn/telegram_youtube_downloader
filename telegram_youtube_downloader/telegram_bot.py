from telegram.ext import Updater, CommandHandler

from telegram_media_sender import TelegramMediaSender
from youtube_downloader import YoutubeDownloader
from download_thread import DownloadThread

from utils.logger_factory import LoggerFactory
from utils.formats import Formats
from utils.utils import Utils


class TelegramBot:
    def __init__(self) -> None:
        self.__bot_key = Utils.get_telegram_bot_key()
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)

        self.downloader = YoutubeDownloader()
        self.media_sender = TelegramMediaSender()

    def start(self):
        """Starts pooling (blocking)"""

        def error(update, context):
            self.__logger.error(f"Update {update} caused error {context.error}")

        @Utils.telegram_bot_exception_handler(self.__logger, function_usage="/help")
        def help(update, context):
            ans = "Commands\n/help\n/formats\n/audio <youtube link>\n/video <youtube link> or /video 480p <youtube link>"
            update.message.reply_text(ans)

        @Utils.telegram_bot_exception_handler(self.__logger, function_usage="/formats")
        def formats(update, context):
            ans = f"Available formats are: {Formats.to_string()}\nTheese are only preferred formats and may not be available for the video."
            update.message.reply_text(ans)

        @Utils.telegram_bot_exception_handler(self.__logger, function_usage="/audio <youtube link>")
        def audio(update, context):
            
            # If there is no args[0] exception handler decorator will handle it
            url = context.args[0]
            chat_id = update.message.chat.id

            update.message.reply_text("⬇️🎧 Download Starting...")
            
            dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type="audio")
            dt.start()


        @Utils.telegram_bot_exception_handler(self.__logger, function_usage="/video <youtube link> or /video 480p <youtube link>")
        def video(update, context):

            chat_id = update.message.chat.id

            # Check arguments
            if(len(context.args) == 2):
                quality = context.args[0]
                url = context.args[1]
                if(quality not in Formats.video_formats):
                    self.__logger.warning("Video format {quality} is not supported")
                    raise ValueError()
            elif(len(context.args) == 1):
                url = context.args[0]
                quality = "720p" # Default
            else:
                raise ValueError()

            update.message.reply_text("⬇️📽️ Download Starting...")

            dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type="video", quality=quality)
            dt.start()


        self.__logger.info("Starting...")
        updater = Updater(self.__bot_key, use_context=True)
        dp = updater.dispatcher
        self.__logger.info("Bot started, good downloading...")

        # command handler
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("formats", formats))
        dp.add_handler(CommandHandler("audio", audio, pass_args=True))
        dp.add_handler(CommandHandler("video", video, pass_args=True))

        # error handler
        dp.add_error_handler(error)

        # start bot
        updater.start_polling()
        updater.idle()
