import datetime
import shutil
import re
import os

import yt_dlp as yt

from youtube_dl_options import YoutubeDlOptions
from errors.download_error import DownloadError
from utils.logger_factory import LoggerFactory
from statics.content_type import ContentType
from utils.config_utils import ConfigUtils


class YoutubeDownloader:
    def __init__(self) -> None:
        self.__download_options = ConfigUtils.read_cfg_file()["youtube_downloader_options"]
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.__bad_chars = {'"': '\'', '<': '', '>': '', ':': '', '/': '', '\\': '', '|': '', '?': '', '*': ''}

    def __is_allowed_url(self, url: str) -> bool:
        """Checks if provided url is on the allowed url list"""
        allowed_patterns = self.__download_options["allowed_url_patterns"]
        matches = []
        for allowed_pattern in allowed_patterns:
            compiled_pattern = re.compile(allowed_pattern["pattern"])
            matches.append(compiled_pattern.match(url))
        return any(matches)

    def __clean_bad_chars(self, filename: str) -> str:
        """Cleans bad chars from the path for Windows"""
        for char in self.__bad_chars:
            filename = filename.replace(char, self.__bad_chars[char])
        return filename

    def __rename_downloaded_file(self, video_title: str, folder_path: str) -> str:
        """
        Renames downloaded temp file to videos title. 
        ** There is no (current) way to know the extension of the file that youtube_dl downloaded (also might be converted) 
        so this function gets all files in a directory, if only 1 file exists this should be the downloaded file so it renames and returns it, else raises DownloadError
        """

        all_files = os.listdir(folder_path)

        if(len(all_files) != 1):
            self.__logger.error(f"Multiple files exists in the folder '{folder_path}'")
            raise DownloadError()

        downloaded_file = os.path.join(folder_path, all_files[0])

        if(not os.path.isfile(downloaded_file)):
            self.__logger.error("Downloaded file is not a valid path")
            raise DownloadError()

        try:
            # fix bad chars for windows
            video_title = self.__clean_bad_chars(video_title)

            # Rename
            _, file_extension = os.path.splitext(downloaded_file)
            new_file_path = os.path.join(folder_path, video_title + file_extension)
            os.rename(downloaded_file, new_file_path)

            return new_file_path
        except:
            self.__logger.error("Unknown error", exc_info=True)
            raise DownloadError()

    def __perform_download(self, url: str, options: dict) -> str:
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
                max_duration = options["max_duration_seconds"]
                content_type = options["content_type"]
                duration = meta.get("duration", None)
                if(duration is None):
                    raise DownloadError(f"Can not get video duration")
                if(duration > max_duration):
                    raise DownloadError(f"Maximum allowed video duration for '{content_type.value}' download is {str(datetime.timedelta(seconds=max_duration))}")

                # Download
                meta = ydl.extract_info(url, download=True)
                meta = ydl.sanitize_info(meta)

                # Rename the temp video name with videos original title (bad windows path chars are replaced)
                path = self.__rename_downloaded_file(meta["title"], options["save_dir"])
                return path

        # Delete folder on exception
        except yt.utils.DownloadError as de:
            self.__logger.warn(str(de))
            self.__logger.info(f"Deleting folder {options['save_dir']}")
            shutil.rmtree(options["save_dir"], ignore_errors=True, onerror=None)
            raise DownloadError("Download error (Site might be not supported)")
        except DownloadError as de:
            self.__logger.warn(str(de))
            self.__logger.info(f"Deleting folder {options['save_dir']}")
            shutil.rmtree(options["save_dir"], ignore_errors=True, onerror=None)
            raise de
        except Exception:
            self.__logger.error("Unknown error", exc_info=True)
            self.__logger.info(f"Deleting folder {options['save_dir']}")
            shutil.rmtree(options["save_dir"], ignore_errors=True, onerror=None)
            raise DownloadError()



    def __get_download_format_from_name(self, content_type: ContentType, format_name: str) -> dict:
        """Returns full format dict for a format name, raises DownloadError if format is not supported. Ex: ({name: test, value: 'best/best', is_default: false})"""
        dl_formats = self.__download_options["formats"][content_type.value]
        for dl_format in dl_formats:
            if(dl_format['name'] == format_name):
                return dl_format
        self.__logger.warning(f"{content_type.value} format '{format_name}' is not supported")
        raise DownloadError(f"{content_type.value} format '{format_name}' is not supported")

    def __get_default_download_format(self, content_type: ContentType) -> str:
        """Returns the default format for a content type, raises DownloadError if no default is set"""
        dl_formats = self.__download_options["formats"][content_type.value]
        for dl_format in dl_formats:
            if(dl_format.get('is_default', False)):
                return dl_format
        self.__logger.error(f"No default format configured for {content_type.value}")
        raise DownloadError(f"No default format configured for {content_type.value}")

    def get_max_video_duration(self) -> str:
        return str(datetime.timedelta(seconds=self.__download_options["max_video_duration_seconds"]))

    def get_max_audio_duration(self) -> str:
        return str(datetime.timedelta(seconds=self.__download_options["max_audio_duration_seconds"]))

    def get_allowed_url_names(self) -> str:
        """Returns allowed site names in readable way"""
        allowed_patterns = self.__download_options["allowed_url_patterns"]
        url_names = ""
        for allowed_pattern in allowed_patterns:
            url_names += f"{allowed_pattern['name']}\n"
        return url_names

    def get_download_formats(self, content_type: ContentType) -> str:
        """Returns download formats in readable way"""
        video_formats = self.__download_options["formats"][content_type.value]
        format_names = ""
        for video_format in video_formats:
            is_default = ' (Default)' if video_format.get('is_default', False) else ''
            format_names += f"{video_format['name']}{is_default}\n"
        return format_names

    def download(self, url: str, content_type: ContentType, download_format_name: "str | None") -> str:
        """Generic download function, sets download_format to default if download_format_name is None"""
        if(not download_format_name):
            dl_format = self.__get_default_download_format(content_type=content_type)
        else: 
            dl_format = self.__get_download_format_from_name(content_type=content_type, format_name=download_format_name)

        options = YoutubeDlOptions()
        options.set_format(content_type, dl_format["value"])

        path = self.__perform_download(url, options.get_for_content_type(content_type))
        return path
