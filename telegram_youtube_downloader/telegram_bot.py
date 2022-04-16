from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_media_sender import TelegramMediaSender
from youtube_downloader import YoutubeDownloader
from youtube_searcher import YoutubeSearcher
from download_thread import DownloadThread

from annotations.telegram_bot_error_handler import TelegramBotErrorHandler
from utils.logger_factory import LoggerFactory
from errors.search_error import SearchError
from utils.formats import Formats
from utils.utils import Utils


class TelegramBot:
    def __init__(self) -> None:
        self.__bot_key = Utils.get_telegram_bot_key()
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)

        self.downloader = YoutubeDownloader()
        self.media_sender = TelegramMediaSender()
        self.youtube_searcher = YoutubeSearcher()

    def start(self):
        """Starts pooling (blocking)"""

        def error(update, context):
            self.__logger.error(f"Update {update} caused error {context.error}")

        @TelegramBotErrorHandler.command_handler(self.__logger, function_usage="/about")
        def about(update, context):
            ans = "Telegram YouTube downloader is an open source project visit projects GitHub page\nhttps://github.com/cccaaannn/telegram_youtube_downloader\n\n Author Can Kurt"
            update.message.reply_text(ans)

        @TelegramBotErrorHandler.command_handler(self.__logger, function_usage="/help")
        def help(update, context):
            ans = f"Commands\n\n/about\n/help\n/formats\n/audio <youtube link> Max: ({self.downloader.get_max_audio_duration()})\n/video <youtube link> Max: ({self.downloader.get_max_video_duration()})\n/video 480p <youtube link>\n/search <query> (Makes youtube search)\nMaximum durations are set by the operator of the bot.\n\nIt is also possible to use main commands with their first letter.\n/a <youtube link>\n/v <youtube link>\n/s <query>"
            update.message.reply_text(ans)

        @TelegramBotErrorHandler.command_handler(self.__logger, function_usage="/formats")
        def formats(update, context):
            ans = f"Available formats are: {Formats.to_string()}\nTheese are only preferred formats and may not be available for the video."
            update.message.reply_text(ans)

        @TelegramBotErrorHandler.command_handler(self.__logger, function_usage="/audio <youtube link>")
        def audio(update, context):
            
            # If there is no args[0] exception handler decorator will handle it
            url = context.args[0]
            chat_id = update.message.chat.id

            update.message.reply_text("⬇️🎧 Download Starting...")
            
            dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type="audio")
            dt.start()


        @TelegramBotErrorHandler.command_handler(self.__logger, function_usage="/video <youtube link> or /video 480p <youtube link>")
        def video(update, context):

            chat_id = update.message.chat.id

            # Check arguments
            if(len(context.args) == 2):
                quality = context.args[0]
                url = context.args[1]
                if(quality not in Formats.video_formats):
                    self.__logger.warning(f"Video format {quality} is not supported")
                    raise ValueError()
            elif(len(context.args) == 1):
                url = context.args[0]
                quality = "default"
            else:
                raise ValueError()

            update.message.reply_text("⬇️📽️ Download Starting...")

            dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type="video", quality=quality)
            dt.start()


        @TelegramBotErrorHandler.command_handler(self.__logger)
        def search(update, context):
            # Bot can be started without youtube api key
            if(not self.youtube_searcher.is_initiliazed()):
                update.message.reply_text("Search is not available")
                return

            # Get and validate query from params
            # Ex: /search sample youtube video  ->  args[0]=sample ...
            query = ' '.join(context.args).strip()
            if(not query or query.isspace()):
                update.message.reply_text("Invalid search query")
                return

            # Run search
            try:
                search_result = self.youtube_searcher.search(query=query)
            except SearchError as se:
                self.__logger.warn(str(se))
                update.message.reply_text(str(se))
                return

            # Fill keyboard and user_data[urls], keyboard's callback_data can not hold url info since it is too large so it is stored in user_data provied by telegram bot library
            context.user_data["urls"] = []
            keyboard = []

            for index, result in enumerate(search_result):
                context.user_data["urls"].append(result["url"])
                keyboard.append([InlineKeyboardButton(Utils.video_title_formatter(result["title"], result["duration"]), callback_data=index)]) # limmit title size with 50 characters

            update.message.reply_text("Choose a video", reply_markup=InlineKeyboardMarkup(keyboard))


        @TelegramBotErrorHandler.menu_handler(self.__logger)
        def search_video_selection_menu_handler(update, context):
            """
            Handles every menu callback except {{video}} or {{audio}}
            When user makes a selection it is saved to user_data["selected_url"] and second menus keyboard is sent.
            """

            data = update.callback_query.data
            query = update.callback_query

            # Since first menu is always called by /search command user_data["urls"] will be full
            context.user_data["selected_url"] = context.user_data["urls"][int(data)]
            keyboard = [[InlineKeyboardButton(f'audio - Max ({self.downloader.get_max_audio_duration()})', callback_data='{{audio}}'), InlineKeyboardButton(f'video - Max ({self.downloader.get_max_video_duration()})', callback_data='{{video}}')]]
            query.edit_message_text(text="Download this video as", reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True))


        @TelegramBotErrorHandler.menu_handler(self.__logger)
        def search_download_type_menu_handler(update, context):
            """
            Handles only {{video}} and {{audio}} menu callbacks
            When user makes a selection, using it and user_data["selected_url"] starts download process
            """

            chat_id = update.callback_query.message.chat.id
            url = context.user_data["selected_url"]

            data = update.callback_query.data
            query = update.callback_query

            # Clear user_data
            del context.user_data["selected_url"]
            del context.user_data["urls"]

            if(data == "{{audio}}"):
                query.edit_message_text(text=f"⬇️🎧 Download Starting...\n\nDownloading from\n{url}", reply_markup=None)
                
                dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type="audio")
                dt.start()

            if(data == "{{video}}"):
                query.edit_message_text(text=f"⬇️📽️ Download Starting...\n\nDownloading from\n{url}", reply_markup=None)
                
                dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type="video", quality="default")
                dt.start()



        self.__logger.info("Starting...")
        updater = Updater(self.__bot_key, use_context=True)
        dp = updater.dispatcher
        self.__logger.info("Bot started, good downloading...")

        # command handler
        dp.add_handler(CommandHandler("about", about))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("formats", formats))
        
        dp.add_handler(CommandHandler("audio", audio, pass_args=True))
        dp.add_handler(CommandHandler("a", audio, pass_args=True))
        
        dp.add_handler(CommandHandler("video", video, pass_args=True))
        dp.add_handler(CommandHandler("v", video, pass_args=True))
        
        dp.add_handler(CommandHandler("search", search))
        dp.add_handler(CommandHandler("s", search))
        dp.add_handler(CallbackQueryHandler(search_video_selection_menu_handler, pattern=r"^(?!{{video}}$|{{audio}}$).*"))  # Everything except {{video}} or {{audio}}
        dp.add_handler(CallbackQueryHandler(search_download_type_menu_handler, pattern=r"^{{video}}$|^{{audio}}$"))         # Only {{video}} or {{audio}}

        # error handler
        dp.add_error_handler(error)

        # start bot
        updater.start_polling()
        updater.idle()
