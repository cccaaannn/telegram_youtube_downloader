import shutil
import re
import os

import yt_dlp as yt

from youtube_dl_options import YoutubeDlOptions
from errors.download_error import DownloadError
from utils.logger_factory import LoggerFactory
from utils.formats import Formats


class YoutubeDownloader:
    def __init__(self) -> None:
        # self.__download_options = Utils.read_cfg_file()["youtube_downloader_options"]
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.__bad_chars = {'"': '\'', '<': '', '>': '', ':': '', '/': '', '\\': '', '|': '', '?': '', '*': ''}

    def __is_youtube_url(self, url):
        """Checks if provided url is from youtube"""
        pattern = r"https://(www.youtube.com/|www.m.youtube.com/|m.youtube.com/|youtu.be/)"
        compiled_pattern = re.compile(pattern)
        match = compiled_pattern.match(url)
        return match

    def __clean_bad_chars(self, filename):
        """Cleans bad chars from the path for Windows"""
        for char in self.__bad_chars:
            filename = filename.replace(char, self.__bad_chars[char])
        return filename

    def __rename_downloaded_file(self, video_title, folder_path):
        """
        Renames downloaded temp file to videos title. 
        There is no way to know the extension of the file that youtube_dl downloaded (also might be converted) 
        so this function gets all files in a directory, if only 1 file exists this should be the downloaded and converted file so renames and retruns it else raises DownloadError
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

    def __download(self, url, options):
        """Download base for different content types"""
        self.__logger.info(f"Downloading from url: {url}")

        # Check the url
        match = self.__is_youtube_url(url)
        if(not match):
            self.__logger.warning(f"Url is not from youtube {url}")
            raise DownloadError("Url is not from youtube")

        # Start download stage
        try:
            with yt.YoutubeDL(options) as ydl:

                # Get video info for checking duration
                meta = ydl.extract_info(url, download=False)
                max_duration = options["max_duration_seconds"]
                if(meta["duration"] > max_duration):
                    raise DownloadError(f"Video duration exceeds defined limit of {max_duration} seconds")

                # Download
                meta = ydl.extract_info(url, download=True)
                meta = ydl.sanitize_info(meta)

                # Rename the temp video name with videos original title (bad windows path chars are replaced)
                path = self.__rename_downloaded_file(meta["title"], options["save_dir"])
                return path

        # Delete folder on exception
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


    def download_audio(self, url):
        options = YoutubeDlOptions()
        path = self.__download(url, options.to_audio())
        return path


    def download_video(self, url, video_format="720p"):
        if(video_format not in Formats.video_formats):
            self.__logger.warning(f"Video format {video_format} is not supported")
            raise DownloadError(f"Video format {video_format} is not supported")

        options = YoutubeDlOptions()
        options.set_video_format(Formats.video_formats[video_format])

        path = self.__download(url, options.to_video())
        return path
