import logging
import shutil
import os

import requests

from utils.api_key_utils import ApiKeyUtils
from utils.config_utils import ConfigUtils
from errors.send_error import SendError


class TelegramMediaSender:
    """Custom media sender class for telegrams native api"""

    __default_telegram_api_url = "https://api.telegram.org/bot"

    def __init__(self) -> None:
        self.__telegram_options = ConfigUtils.get_app_config().telegram_bot_options
        self.__bot_key = ApiKeyUtils.get_telegram_bot_key()
        self.__logger = logging.getLogger(f"tyd.{self.__class__.__name__}")
        __base_url_config = ConfigUtils.get_app_config().telegram_bot_options.base_url
        self.__base_url = __base_url_config if __base_url_config is not None else self.__default_telegram_api_url

    def send_text(self, chat_id: int, text: str) -> None:
        try: 
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }

            url = f"{self.__base_url}{self.__bot_key}/sendMessage"
            timeout = self.__telegram_options.text_timeout_seconds

            resp = requests.post(url, data=payload, timeout=timeout).json()
            self.__logger.info(resp)

            if(not resp['ok']):
                self.__logger.warning(resp)
                raise SendError(f"Could not send message, Telegram: {resp['description']}")

        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            raise SendError()


    def send_audio(self, chat_id: int, file_path: str, title: str, remove=False) -> None:
        try:
            with open(file_path, 'rb') as audio:
                payload = {
                    'chat_id': chat_id,
                    'title': title,
                    'parse_mode': 'HTML'
                }
                files = {
                    'audio': audio.read(),
                }
                url = f"{self.__base_url}{self.__bot_key}/sendAudio"
                timeout = self.__telegram_options.audio_timeout_seconds

                resp = requests.post(url, data=payload, files=files, timeout=timeout).json()
                self.__logger.info(resp)

                if(not resp['ok']):
                    self.__logger.warning(resp)
                    raise SendError(f"Could not send audio, Telegram: {resp['description']}")

        except (requests.Timeout, requests.ConnectionError):
            self.__logger.warning("Could not send audio, timeout")
            raise SendError("Could not send audio, timeout")

        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            raise SendError("Could not sent audio")

        finally:
            if(remove):
                self.__logger.info(f"Deleting folder {file_path}")
                
                # Try to delete folder
                folder_name, _ = os.path.split(file_path)
                shutil.rmtree(folder_name, ignore_errors=True)

    def send_video(self, chat_id: int, file_path: str, title: str, remove=False) -> None:
        try:
            with open(file_path, 'rb') as video:
                payload = {
                    'chat_id': chat_id,
                    'title': title,
                    'parse_mode': 'HTML'
                }
                files = {
                    'video': video.read(),
                }
                url = f"{self.__base_url}{self.__bot_key}/sendVideo"
                timeout = self.__telegram_options.video_timeout_seconds

                resp = requests.post(url, data=payload, files=files, timeout=timeout).json()
                self.__logger.info(resp)

                if(not resp['ok']):
                    self.__logger.warning(resp)
                    raise SendError(f"Could not send video, Telegram: {resp['description']}")

        except (requests.Timeout, requests.ConnectionError):
            self.__logger.warning("Could not send video, timeout")
            raise SendError("Could not send video, timeout")

        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            raise SendError("Could not sent video")

        finally:
            if(remove):
                self.__logger.info(f"Deleting folder {file_path}")

                # Try to delete folder
                folder_name, _ = os.path.split(file_path)
                shutil.rmtree(folder_name, ignore_errors=True)
