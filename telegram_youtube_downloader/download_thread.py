import threading
import time

from telegram_media_sender import TelegramMediaSender
from youtube_downloader import YoutubeDownloader

from errors.download_error import DownloadError
from utils.logger_factory import LoggerFactory
from statics.content_type import ContentType
from errors.send_error import SendError


class DownloadThread(threading.Thread):
    def __init__(self, downloader: YoutubeDownloader, media_sender: TelegramMediaSender, url: str, chat_id: str, content_type: ContentType, dl_format_name: "str | None") -> None:
        super().__init__()
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.downloader = downloader
        self.media_sender = media_sender
        self.url = url
        self.chat_id = chat_id
        self.content_type = content_type
        self.dl_format_name = dl_format_name


    def __run_for_audio(self):
        download_start = time.time()
        path = self.downloader.download(self.url, ContentType.AUDIO, self.dl_format_name)
        self.__logger.info(f"Download completed with path {path}, took {float(time.time() - download_start):.3f} seconds")

        self.media_sender.send_text(self.chat_id, "⬆️🎧 Download finished, sending...")

        upload_start = time.time()
        self.media_sender.send_audio(chat_id=self.chat_id, file_path=path, remove=True)
        self.media_sender.send_text(self.chat_id, "🥳")
        self.__logger.info(f"Upload completed, took {float(time.time() - upload_start):.3f} seconds")
        
        self.__logger.info(f"Total operation took {float(time.time() - download_start):.3f} seconds")

    def __run_for_video(self):
        download_start = time.time()
        path = self.downloader.download(self.url, ContentType.VIDEO, self.dl_format_name)
        self.__logger.info(f"Download completed with path {path}, took {float(time.time() - download_start):.3f} seconds")

        self.media_sender.send_text(self.chat_id, "⬆️📽️ Download finished, sending...")

        upload_start = time.time()
        self.media_sender.send_video(chat_id=self.chat_id, file_path=path, remove=True)
        self.media_sender.send_text(self.chat_id, "🥳")
        self.__logger.info(f"Upload completed, took {float(time.time() - upload_start):.3f} seconds")

        self.__logger.info(f"Total operation took {float(time.time() - download_start):.3f} seconds")


    def run(self):
        self.__logger.info(f"Download started for url {self.url}")

        try:
            # TODO Might convert to inheritance later
            if(self.content_type == ContentType.AUDIO):
                self.__run_for_audio()
            elif(self.content_type == ContentType.VIDEO):
                self.__run_for_video()
            else:
                pass

        except (DownloadError, SendError) as e:
            self.__logger.warn(str(e))
            # Try to answer on error
            try:
                self.media_sender.send_text(chat_id=self.chat_id, text=f"💩 {str(e)}")
            except:
                self.__logger.error(f"User notifying attempt (via message) for an error failed due to another error during message sending, {str(e)}", exc_info=True)
        except Exception as e:
            self.__logger.error("Unknown error", exc_info=True)
            # Try to answer on error
            try:
                self.media_sender.send_text(chat_id=self.chat_id, text="🤷🏻‍♂️ Unknown error")
            except:
                self.__logger.error(f"User notifying attempt (via message) for an error failed due to another error during message sending, {str(e)}", exc_info=True)

