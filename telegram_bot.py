from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import os

from youtube_downloader import youtube_downloader


# options
telegram_logger = "log/telegram.log"
yt_download_logger = "log/yt_downloader.log"
temp_folder_path = "tmp"
timeout = 180000


# create downloader object
ytd = youtube_downloader(temp_folder_path = temp_folder_path, log_file = yt_download_logger)


# create logger
def __set_logger(logger_name, log_file=None, log_level=20):

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

# set logger
logger = __set_logger(__name__, log_file=telegram_logger)

def command_logger(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info("Function name: {0} User info: {1}".format(func.__name__, args[0].message.from_user))
                func(*args, **kwargs)
            except(IndexError, ValueError): 
                args[0].message.reply_text(function_usages[func.__name__])
                logger.warning("function name: {0} username:{1}".format(func.__name__, args[0].message.from_user.username), exc_info=True)
            except:
                args[0].message.reply_text("something went wrong")
                logger.error("function name: {0} username:{1}".format(func.__name__, args[0].message.from_user.username), exc_info=True)
        return wrapper
    return decorator



# utilities
def function_usages_str(function_usages):
    usages_str = ""
    for i in function_usages:
        usages_str += "command: {0} {1}\n".format(i, function_usages[i])
    return usages_str

def is_youtube_link(link):
    pattern = r"https://(www.youtube.com/|www.m.youtube.com/|m.youtube.com/)"
    compiled_pattern = re.compile(pattern)
    match = compiled_pattern.match(link)
    return match

function_usages = {"help": "usage /help", "audio": "usage /audio <youtube link>", "video": "usage /video <youtube link>"}



# telegram functions
def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)


@command_logger(logger)
def help(update, context):
    """Send a message when the command /help is issued."""
    usages_str = function_usages_str(function_usages)
    update.message.reply_text(usages_str)


@command_logger(logger)
def audio(update, context):

    link = context.args[0]

    # check the link
    match = is_youtube_link(link)
    if(not match):
        update.message.reply_text("link is not from youtube")
        return

    # download
    status, path = ytd.download(link, dl_type="audio")

    # send error mesages
    if(not status):
        update.message.reply_text(path)
        return

    # send file
    context.bot.send_audio(chat_id=update.message.chat.id, audio=open(path, 'rb'), timeout=timeout)

    # delete file (full path required for security)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    ytd.rm_downloaded_file(path)


@command_logger(logger)
def video(update, context):

    link = context.args[0]

    # check the link
    match = is_youtube_link(link)
    if(not match):
        update.message.reply_text("link is not from youtube")
        return

    # download
    status, path = ytd.download(link, dl_type="video", dl_format="480p")

    # send error mesages
    if(not status):
        update.message.reply_text(path)
        return

    # send file
    context.bot.send_video(chat_id=update.message.chat.id, video=open(path, 'rb'), timeout=timeout)

    # delete file (full path required for security)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    ytd.rm_downloaded_file(path)






def main(botkey):
    updater = Updater(botkey, use_context=True)

    # bot loop
    dp = updater.dispatcher

    # command handler
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("audio", audio, pass_args=True))
    dp.add_handler(CommandHandler("video", video, pass_args=True))

    # error handler
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()




