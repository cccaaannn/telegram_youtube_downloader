import threading
import time

from telegram_media_sender import TelegramMediaSender
from youtube_downloader import YoutubeDownloader

from utils.logger_factory import LoggerFactory
from errors.download_error import DownloadError
from errors.send_error import SendError


class DownloadThread(threading.Thread):
    def __init__(self, downloader: YoutubeDownloader, media_sender: TelegramMediaSender, url: str, chat_id: str, content_type: str, quality: str=None) -> None:
        super().__init__()
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.downloader = downloader
        self.media_sender = media_sender
        self.url = url
        self.chat_id = chat_id
        self.content_type = content_type
        self.quality = quality


    def __run_for_audio(self):
        download_start = time.time()
        path = self.downloader.download_audio(self.url)
        self.__logger.info(f"Download completed with path {path}, took {float(time.time() - download_start):.3f} seconds")

        self.media_sender.send_text(self.chat_id, "⬆️🎧 Download finished, sending...")

        upload_start = time.time()
        self.media_sender.send_audio(chat_id=self.chat_id, file_path=path, remove=True)
        self.media_sender.send_text(self.chat_id, "🥳")
        self.__logger.info(f"Upload completed, took {float(time.time() - upload_start):.3f} seconds")
        
        self.__logger.info(f"Total operation took {float(time.time() - download_start):.3f} seconds")

    def __run_for_video(self):
        download_start = time.time()
        path = self.downloader.download_video(self.url, self.quality)
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
            if(self.content_type == "audio"):
                self.__run_for_audio()
            elif(self.content_type == "video"):
                self.__run_for_video()
            else:
                pass

        except DownloadError or SendError as e:
            self.__logger.warn(str(e))
            # Try to answer on error
            try:
                self.media_sender.send_text(chat_id=self.chat_id, text=f"💩 {str(e)}")
            except:
                pass
        except:
            self.__logger.error("Unknown error", exc_info=True)
            # Try to answer on error
            try:
                self.media_sender.send_text(chat_id=self.chat_id, text="🤷🏻‍♂️ Unknown error")
            except:
                pass

