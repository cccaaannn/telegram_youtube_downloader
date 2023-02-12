import textwrap

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram_media_sender import TelegramMediaSender
from youtube_downloader import YoutubeDownloader
from youtube_searcher import YoutubeSearcher
from download_thread import DownloadThread

from decorators.telegram_bot_command_interceptor import TelegramBotCommandInterceptor
from decorators.telegram_bot_error_handler import TelegramBotErrorHandler
from utils.logger_factory import LoggerFactory
from statics.content_type import ContentType
from errors.search_error import SearchError
from utils.api_key_utils import ApiKeyUtils


class TelegramBot:
    def __init__(self) -> None:
        self.__bot_key = ApiKeyUtils.get_telegram_bot_key()
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)

        self.downloader = YoutubeDownloader()
        self.media_sender = TelegramMediaSender()
        self.youtube_searcher = YoutubeSearcher()

    @staticmethod
    def __video_title_formatter(title, duration, title_length=45) -> str:
        """Formats video title for search menu. Ex: test..."""
        formatted_title = f"({duration}) {title}"
        if(len(formatted_title) > title_length):
            formatted_title = formatted_title[:title_length]
            formatted_title += "..."
        return formatted_title

    def start(self):
        """Starts pooling (blocking)"""

        def error(update, context):
            self.__logger.error(f"Update {update} caused error {context.error}")

        @TelegramBotErrorHandler.command_handler(self.__logger, function_name="about", function_usage="/about")
        @TelegramBotCommandInterceptor.secured_command(function_claims={"all", "about"})
        def about(update, context):
            ans = textwrap.dedent("""\
                [About]

                Telegram YouTube downloader is an open source project visit projects GitHub page
                https://github.com/cccaaannn/telegram_youtube_downloader

                Author Can Kurt""")
            update.message.reply_text(ans)

        @TelegramBotErrorHandler.command_handler(self.__logger, function_name="help", function_usage="/help")
        @TelegramBotCommandInterceptor.secured_command(function_claims={"all", "help"})
        def help(update: Update, context: CallbackContext):
            ans = textwrap.dedent(f"""\
                [Commands]

                [Video download] Max: ({self.downloader.get_max_video_duration()})
                /video <download url>
                /video <format> <download url>
                /v <download url>

                [Audio download] Max: ({self.downloader.get_max_audio_duration()})
                /audio <download url>
                /audio <format> <download url>
                /a <download url>

                [Search]
                /search <query>
                /s <query>

                [Utilities]
                /about
                /help
                /formats
                /sites

                Maximum durations are set by the operator of the bot.""")
            update.message.reply_text(ans)

        @TelegramBotErrorHandler.command_handler(self.__logger, function_name="formats", function_usage="/formats")
        @TelegramBotCommandInterceptor.secured_command(function_claims={"all", "formats"})
        def formats(update, context):
            ans = f"[Available formats]\n\n[audio]\n{self.downloader.get_download_formats(ContentType.AUDIO)}\n[video]\n{self.downloader.get_download_formats(ContentType.VIDEO)}\nThese are only preferred formats and may not be available for the video."
            update.message.reply_text(ans)

        @TelegramBotErrorHandler.command_handler(self.__logger, function_name="sites", function_usage="/sites")
        @TelegramBotCommandInterceptor.secured_command(function_claims={"all", "sites"})
        def sites(update, context):
            ans = f"[Supported sites]\n\n{self.downloader.get_allowed_url_names()}"
            update.message.reply_text(ans)

        @TelegramBotErrorHandler.command_handler(self.__logger, function_name="audio", function_usage="/audio <download url> or /audio <format> <download url>\n/formats for available formats")
        @TelegramBotCommandInterceptor.secured_command(function_claims={"all", "audio"})
        def audio(update, context):
            if(len(context.args) > 2 or len(context.args) < 1):
                raise ValueError()

            chat_id = update.message.chat.id

            # Check arguments
            if(len(context.args) == 2):
                dl_format_name = context.args[0]
                url = context.args[1]
            if(len(context.args) == 1):
                url = context.args[0]
                dl_format_name = None

            update.message.reply_text("⬇️🎧 Download Starting...")

            dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type=ContentType.AUDIO, dl_format_name=dl_format_name)
            dt.start()

        @TelegramBotErrorHandler.command_handler(self.__logger, function_name="video", function_usage="/video <download url> or /video <format> <download url>\n/formats for available formats")
        @TelegramBotCommandInterceptor.secured_command(function_claims={"all", "video"})
        def video(update, context):
            if(len(context.args) > 2 or len(context.args) < 1):
                raise ValueError()

            chat_id = update.message.chat.id

            # Check arguments
            if(len(context.args) == 2):
                dl_format_name = context.args[0]
                url = context.args[1]
            if(len(context.args) == 1):
                url = context.args[0]
                dl_format_name = None

            update.message.reply_text("⬇️📽️ Download Starting...")

            dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type=ContentType.VIDEO, dl_format_name=dl_format_name)
            dt.start()

        @TelegramBotErrorHandler.command_handler(self.__logger, function_name="search", function_usage="/search <query>")
        @TelegramBotCommandInterceptor.secured_command(function_claims={"all", "search"})
        def search(update, context):
            # Bot can be started without youtube api key
            if(not self.youtube_searcher.is_initialized()):
                update.message.reply_text("Search is not activated by the operator of this bot")
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

            # Fill keyboard and user_data[urls], keyboard's callback_data can not hold url info since it is too large so it is stored in user_data provided by telegram bot library
            context.user_data["urls"] = []
            keyboard = []

            for index, result in enumerate(search_result):
                context.user_data["urls"].append(result["url"])
                keyboard.append([InlineKeyboardButton(TelegramBot.__video_title_formatter(result["title"], result["duration"]), callback_data=index)]) # limit title size with 50 characters

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
 
                dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type=ContentType.AUDIO, dl_format_name=None)
                dt.start()

            if(data == "{{video}}"):
                query.edit_message_text(text=f"⬇️📽️ Download Starting...\n\nDownloading from\n{url}", reply_markup=None)

                dt = DownloadThread(downloader=self.downloader, media_sender=self.media_sender, url=url, chat_id=chat_id, content_type=ContentType.VIDEO, dl_format_name=None)
                dt.start()


        self.__logger.info("Starting...")
        updater = Updater(self.__bot_key, use_context=True)
        dp = updater.dispatcher
        self.__logger.info("Bot started, good downloading...")

        # command handler
        dp.add_handler(CommandHandler("about", about))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("formats", formats))
        dp.add_handler(CommandHandler("sites", sites))

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
