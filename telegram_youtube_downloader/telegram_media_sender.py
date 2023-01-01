import shutil
import os

import requests

from utils.logger_factory import LoggerFactory
from utils.api_key_utils import ApiKeyUtils
from utils.config_utils import ConfigUtils
from errors.send_error import SendError


class TelegramMediaSender:
    """Custom media sender class for telegrams native api"""

    def __init__(self) -> None:
        self.__telegram_options = ConfigUtils.read_cfg_file()["telegram_bot_options"]
        self.__bot_key = ApiKeyUtils.get_telegram_bot_key()
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)

    def send_text(self, chat_id, text):
        try: 
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }

            url = f"https://api.telegram.org/bot{self.__bot_key}/sendMessage"
            timeout = self.__telegram_options["text_timeout_seconds"]

            resp = requests.post(url, data=payload, timeout=timeout).json()
            self.__logger.info(resp)

            if(not resp['ok']):
                self.__logger.warn(resp)
                raise SendError(f"Could not send message, Telegram: {resp['description']}")

        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            raise SendError()


    def send_audio(self, chat_id, file_path, remove=False):
        try:
            _, file_name = os.path.split(file_path)

            with open(file_path, 'rb') as audio:
                payload = {
                    'chat_id': chat_id,
                    'title': file_name,
                    'parse_mode': 'HTML'
                }
                files = {
                    'audio': audio.read(),
                }
                url = f"https://api.telegram.org/bot{self.__bot_key}/sendAudio"
                timeout = self.__telegram_options["audio_timeout_seconds"]

                resp = requests.post(url, data=payload, files=files, timeout=timeout).json()
                self.__logger.info(resp)

                if(not resp['ok']):
                    self.__logger.warn(resp)
                    raise SendError(f"Could not send audio, Telegram: {resp['description']}")

        except (requests.Timeout, requests.ConnectionError):
            self.__logger.warn("Could not send audio, timeout")
            raise SendError("Could not send audio, timeout")

        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            raise SendError("Could not sent audio")

        finally:
            if(remove):
                self.__logger.info(f"Deleting folder {file_path}")
                
                # Try to delete folder
                folder_name, _ = os.path.split(file_path)
                shutil.rmtree(folder_name, ignore_errors=True, onerror=None)

    def send_video(self, chat_id, file_path, remove=False):
        try:
            _, file_name = os.path.split(file_path)

            with open(file_path, 'rb') as video:
                payload = {
                    'chat_id': chat_id,
                    'title': file_name,
                    'parse_mode': 'HTML'
                }
                files = {
                    'video': video.read(),
                }
                url = f"https://api.telegram.org/bot{self.__bot_key}/sendVideo"
                timeout = self.__telegram_options["video_timeout_seconds"]

                resp = requests.post(url, data=payload, files=files, timeout=timeout).json()
                self.__logger.info(resp)

                if(not resp['ok']):
                    self.__logger.warn(resp)
                    raise SendError(f"Could not send video, Telegram: {resp['description']}")

        except (requests.Timeout, requests.ConnectionError):
            self.__logger.warn("Could not send video, timeout")
            raise SendError("Could not send video, timeout")

        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            raise SendError("Could not sent video")

        finally:
            if(remove):
                self.__logger.info(f"Deleting folder {file_path}")

                # Try to delete folder
                folder_name, _ = os.path.split(file_path)
                shutil.rmtree(folder_name, ignore_errors=True, onerror=None)
