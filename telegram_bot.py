from telegram.ext import Updater, CommandHandler
import logging
import json

# import downloader class
from youtube_downloader import youtube_downloader


# logger functions
def create_logger(logger_name, log_file=None, log_level=20):

    logger = logging.getLogger(logger_name)  

    if(not logger.handlers):
        logger.setLevel(log_level)
        
        # log formatter
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        # stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # file handler
        if(log_file):
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger

def command_logger(logger, function_usages):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info("Function name: {0} User info: {1}".format(func.__name__, args[0].message.from_user))
                func(*args, **kwargs)
            except(IndexError, ValueError): 
                logger.warning("function name: {0} username:{1}".format(func.__name__, args[0].message.from_user.username), exc_info=True)
                args[0].message.reply_text(function_usages[func.__name__])
            except:
                logger.error("function name: {0} username:{1}".format(func.__name__, args[0].message.from_user.username), exc_info=True)
                args[0].message.reply_text("something went wrong")
        return wrapper
    return decorator


# utilities
def function_usages_str(function_usages):
    usages_str = ""
    for i in function_usages:
        usages_str += "command: {0} {1}\n".format(i, function_usages[i])
    return usages_str

def read_cfg_file(cfg_path):
    try:
        with open(cfg_path,"r") as file:
            d = json.load(file)
        return d
    except:
        return 0


def run_bot(botkey, cfg_path = "cfg/options.cfg"):

    # set options
    cfg_dict = read_cfg_file(cfg_path)
    if(cfg_dict):
        # youtube downloader options
        yt_downloader_logger_name = cfg_dict["yt_downloader"]["yt_downloader_logger_name"]
        yt_downloader_logger_file = cfg_dict["yt_downloader"]["yt_downloader_logger_file"]
        yt_downloader_log_level = cfg_dict["yt_downloader"]["yt_downloader_log_level"]
        temp_folder_path = cfg_dict["yt_downloader"]["temp_folder_path"]
        temp_file_name = cfg_dict["yt_downloader"]["temp_file_name"]
        bad_chars = cfg_dict["yt_downloader"]["bad_chars"]
        video_formats = cfg_dict["yt_downloader"]["video_formats"]
        preferred_video_format = cfg_dict["yt_downloader"]["preferred_video_format"]
        preferred_audio_codec = cfg_dict["yt_downloader"]["preferred_audio_codec"]
        ffmpeg_location = cfg_dict["yt_downloader"]["ffmpeg_location"]
        max_video_duration = cfg_dict["yt_downloader"]["max_video_duration"]

        # telegram bot options
        telegram_logger_name = cfg_dict["telegram_bot"]["telegram_logger_name"]
        telegram_logger_file = cfg_dict["telegram_bot"]["telegram_logger_file"]
        telegram_bot_log_level = cfg_dict["telegram_bot"]["telegram_bot_log_level"]
        timeout_audio = cfg_dict["telegram_bot"]["timeout_audio"]
        timeout_video = cfg_dict["telegram_bot"]["timeout_video"]
        function_usages = cfg_dict["telegram_bot"]["function_usages"]
    else:
        print("cfg file is broken")
        return


    # set logger
    logger = create_logger(telegram_logger_name, log_file=telegram_logger_file, log_level=telegram_bot_log_level)

    # create downloader object
    ytd = youtube_downloader(
    logger_name=yt_downloader_logger_name,
    log_file=yt_downloader_logger_file,
    log_level=yt_downloader_log_level, 
    temp_folder_path=temp_folder_path,
    temp_file_name=temp_file_name,
    bad_chars=bad_chars,
    video_formats=video_formats,
    preferred_video_format=preferred_video_format,
    preferred_audio_codec=preferred_audio_codec,
    ffmpeg_location=ffmpeg_location,
    max_video_duration=max_video_duration
    )

    
    # telegram functions
    def error(update, context):
        """Log Errors caused by Updates."""
        logger.error('Update "%s" caused error "%s"', update, context.error)

    @command_logger(logger, function_usages)
    def help(update, context):
        """Send a message when the command /help is issued."""
        usages_str = function_usages_str(function_usages)
        update.message.reply_text(usages_str)

    @command_logger(logger, function_usages)
    def formats(update, context):
        """Sends video download formats"""
        formats = ytd.get_video_formats()
        update.message.reply_text(formats)

    @command_logger(logger, function_usages)
    def audio(update, context):

        link = context.args[0]

        # download
        update.message.reply_text("please wait...")
        status, path = ytd.download(link, dl_type="audio")

        # send error mesages
        if(not status):
            update.message.reply_text(path)
            return

        # send file
        update.message.reply_text("sending...")
        context.bot.send_audio(chat_id=update.message.chat.id, audio=open(path, 'rb'), timeout=timeout_audio)

    @command_logger(logger, function_usages)
    def video(update, context):
        
        if(len(context.args) == 2):
            quality = context.args[0]
            link = context.args[1]
        elif(len(context.args) == 1):
            link = context.args[0]
            quality = "default"
        else:
            update.message.reply_text(function_usages["video"])
            return

        # download
        update.message.reply_text("please wait...")
        status, path = ytd.download(link, dl_type="video", dl_format=quality)

        # send error mesages
        if(not status):
            update.message.reply_text(path)
            return

        # send file
        update.message.reply_text("sending...")
        context.bot.send_video(chat_id=update.message.chat.id, video=open(path, 'rb'), timeout=timeout_video)


    logger.info("Bot started, have a good downloading...")
    updater = Updater(botkey, use_context=True)
    dp = updater.dispatcher

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


