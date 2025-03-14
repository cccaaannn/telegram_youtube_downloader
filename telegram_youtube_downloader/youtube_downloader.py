import datetime
import logging
import shutil
import re
import os

import yt_dlp as yt

from data.downloader_result import DownloaderResult
from youtube_dl_options import YoutubeDlOptions
from errors.download_error import DownloadError
from statics.content_type import ContentType
from utils.config_utils import ConfigUtils
from data.dl_format import DlFormat


class YoutubeDownloader:
    def __init__(self) -> None:
        self.__download_options = ConfigUtils.get_app_config().youtube_downloader_options
        self.__logger = logging.getLogger(f"tyd.{self.__class__.__name__}")

    def __is_allowed_url(self, url: str) -> bool:
        """Checks if provided url is on the allowed url list"""
        allowed_patterns = self.__download_options.allowed_url_patterns
        matches = []
        for allowed_pattern in allowed_patterns:
            compiled_pattern = re.compile(allowed_pattern.pattern)
            matches.append(compiled_pattern.match(url))
        return any(matches)

    def __get_downloaded_file_path(self, folder_path: str) -> str:
        """
        Returns downloaded file's full path.
        ** There is no (current) way to know the extension of the file that youtube_dl downloaded (also might be converted)
        so this function gets all files in a directory, if only 1 file exists this should be the downloaded file so it renames and returns it, else raises DownloadError
        """

        all_files = os.listdir(folder_path)

        if(len(all_files) != 1):
            self.__logger.error(f"Multiple files exists in the folder '{folder_path}'")
            raise DownloadError()

        downloaded_file_path = os.path.join(folder_path, all_files[0])

        if(not os.path.isfile(downloaded_file_path)):
            self.__logger.error("Downloaded file is not a valid path")
            raise DownloadError()

        return downloaded_file_path

    def __perform_download(self, url: str, options: dict) -> DownloaderResult:
        """Download base for different content types"""
        self.__logger.info(f"Downloading from url: {url} with options: {options}")

        # Check the url
        match = self.__is_allowed_url(url)
        if(not match):
            self.__logger.warning(f"Url is not on the allowed url list '{url}'")
            raise DownloadError("Url is not on the allowed url list")

        # Start download stage
        try:
            with yt.YoutubeDL(options) as ydl:

                # Get video info for checking duration
                meta = ydl.extract_info(url, download=False)

                if not isinstance(meta, dict):
                    self.__logger.error("Cannot extract video metadata")
                    raise DownloadError("Cannot extract video metadata")

                max_duration = options["max_duration_seconds"]
                content_type = options["content_type"]

                duration = meta.get("duration", None)
                if(duration is None):
                    raise DownloadError(f"Cannot get video duration")
                if(duration > max_duration):
                    raise DownloadError(f"Maximum allowed video duration for '{content_type.value}' download is {str(datetime.timedelta(seconds=max_duration))}")

                # Download
                meta = ydl.extract_info(url, download=True)
                meta = ydl.sanitize_info(meta)

                if not isinstance(meta, dict):
                    self.__logger.error("Cannot extract video metadata")
                    raise DownloadError("Cannot extract video metadata")

                # Get saved file path
                downloaded_file_path = self.__get_downloaded_file_path(options["save_dir"])

                # Build response
                result = DownloaderResult(
                    file_path=downloaded_file_path,
                    video_title=str(meta.get("title", "Unknown")),
                )

                return result

        # Delete folder on exception
        except yt.utils.DownloadError as de:
            self.__logger.warning(str(de))
            self.__logger.info(f"Deleting folder {options['save_dir']}")
            shutil.rmtree(options["save_dir"], ignore_errors=True)
            raise DownloadError("Download error (yt_dlp download error)")
        except DownloadError as de:
            self.__logger.warning(str(de))
            self.__logger.info(f"Deleting folder {options['save_dir']}")
            shutil.rmtree(options["save_dir"], ignore_errors=True)
            raise de
        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            self.__logger.info(f"Deleting folder {options['save_dir']}")
            shutil.rmtree(options["save_dir"], ignore_errors=True)
            raise DownloadError()



    def __get_download_format_from_name(self, content_type: ContentType, format_name: str) -> DlFormat:
        """Returns full format dict for a format name, raises DownloadError if format is not supported. Ex: ({name: test, value: 'best/best', is_default: false})"""
        dl_formats = self.__download_options.formats.from_string(content_type.value)
        for dl_format in dl_formats:
            if(dl_format.name == format_name):
                return dl_format
        self.__logger.warning(f"{content_type.value} format '{format_name}' is not supported")
        raise DownloadError(f"{content_type.value} format '{format_name}' is not supported")

    def __get_default_download_format(self, content_type: ContentType) -> DlFormat:
        """Returns the default format for a content type, raises DownloadError if no default is set"""
        dl_formats = self.__download_options.formats.from_string(content_type.value)
        for dl_format in dl_formats:
            if(dl_format.is_default):
                return dl_format
        self.__logger.error(f"No default format configured for {content_type.value}")
        raise DownloadError(f"No default format configured for {content_type.value}")

    def get_max_video_duration(self) -> str:
        return str(datetime.timedelta(seconds=self.__download_options.max_video_duration_seconds))

    def get_max_audio_duration(self) -> str:
        return str(datetime.timedelta(seconds=self.__download_options.max_audio_duration_seconds))

    def get_allowed_url_names(self) -> str:
        """Returns allowed site names in readable way"""
        allowed_patterns = self.__download_options.allowed_url_patterns
        url_names = ""
        for allowed_pattern in allowed_patterns:
            url_names += f"{allowed_pattern.name}\n"
        return url_names

    def get_download_formats(self, content_type: ContentType) -> str:
        """Returns download formats in readable way"""
        video_formats = self.__download_options.formats.from_string(content_type.value)
        format_names = ""
        for video_format in video_formats:
            is_default = ' (Default)' if video_format.is_default else ''
            format_names += f"{video_format.name}{is_default}\n"
        return format_names

    def download(self, url: str, content_type: ContentType, download_format_name: "str | None") -> DownloaderResult:
        """Generic download function, sets download_format to default if download_format_name is None"""
        if(not download_format_name):
            dl_format = self.__get_default_download_format(content_type=content_type)
        else: 
            dl_format = self.__get_download_format_from_name(content_type=content_type, format_name=download_format_name)

        options = YoutubeDlOptions()
        options.set_format(content_type, dl_format.value)

        result = self.__perform_download(url, options.get_for_content_type(content_type))
        return result
