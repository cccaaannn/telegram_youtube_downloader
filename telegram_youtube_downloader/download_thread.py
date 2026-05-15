import time
import logging
import threading

from telegram_youtube_downloader.errors.send_error import SendError
from telegram_youtube_downloader.youtube_downloader import YoutubeDownloader
from telegram_youtube_downloader.statics.content_type import ContentType
from telegram_youtube_downloader.errors.download_error import DownloadError
from telegram_youtube_downloader.telegram_media_sender import TelegramMediaSender


class DownloadThread(threading.Thread):
	def __init__(
		self,
		downloader: YoutubeDownloader,
		media_sender: TelegramMediaSender,
		url: str,
		chat_id: int,
		content_type: ContentType,
		dl_format_name: "str | None",
	) -> None:
		super().__init__()
		self.__logger = logging.getLogger(f"tyd.{self.__class__.__name__}")
		self.downloader = downloader
		self.media_sender = media_sender
		self.url = url
		self.chat_id = chat_id
		self.content_type = content_type
		self.dl_format_name = dl_format_name

	def __run_for_audio(self) -> None:
		download_start = time.time()
		result = self.downloader.download(self.url, ContentType.AUDIO, self.dl_format_name)
		self.__logger.info(
			f"Download completed {result}, took {float(time.time() - download_start):.3f} seconds"
		)

		self.media_sender.send_text(self.chat_id, "⬆️🎧 Download finished, sending...")

		upload_start = time.time()
		self.media_sender.send_audio(
			chat_id=self.chat_id, file_path=result.file_path, title=result.video_title, remove=True
		)
		self.media_sender.send_text(self.chat_id, "🥳")
		self.__logger.info(
			f"Upload completed, took {float(time.time() - upload_start):.3f} seconds"
		)

		self.__logger.info(
			f"Total operation took {float(time.time() - download_start):.3f} seconds"
		)

	def __run_for_video(self) -> None:
		download_start = time.time()
		result = self.downloader.download(self.url, ContentType.VIDEO, self.dl_format_name)
		self.__logger.info(
			f"Download completed {result}, took {float(time.time() - download_start):.3f} seconds"
		)

		self.media_sender.send_text(self.chat_id, "⬆️📽️ Download finished, sending...")

		upload_start = time.time()
		self.media_sender.send_video(
			chat_id=self.chat_id, file_path=result.file_path, title=result.video_title, remove=True
		)
		self.media_sender.send_text(self.chat_id, "🥳")
		self.__logger.info(
			f"Upload completed, took {float(time.time() - upload_start):.3f} seconds"
		)

		self.__logger.info(
			f"Total operation took {float(time.time() - download_start):.3f} seconds"
		)

	def run(self) -> None:
		self.__logger.info(f"Download started for url {self.url}")

		try:
			# TODO Might convert to inheritance later
			if self.content_type == ContentType.AUDIO:
				self.__run_for_audio()
			elif self.content_type == ContentType.VIDEO:
				self.__run_for_video()
			else:
				pass

		except (DownloadError, SendError) as e:
			self.__logger.warning(str(e))
			# Try to answer on error
			try:
				self.media_sender.send_text(chat_id=self.chat_id, text=f"💩 {str(e)}")
			except:
				self.__logger.error(
					f"User notifying attempt (via message) for an error failed due to another error during message sending, {str(e)}",
					exc_info=True,
				)
		except Exception as e:
			self.__logger.error("Unknown error", exc_info=True)
			# Try to answer on error
			try:
				self.media_sender.send_text(chat_id=self.chat_id, text="🤷🏻‍♂️ Unknown error")
			except:
				self.__logger.error(
					f"User notifying attempt (via message) for an error failed due to another error during message sending, {str(e)}",
					exc_info=True,
				)
