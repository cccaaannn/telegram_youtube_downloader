import pathlib
import uuid
import os

from utils.utils import Utils


class YoutubeDlOptions:
    def __init__(self):
        self.__dynamic_options = Utils.read_cfg_file()["youtube_downloader_options"]

        save_dir = self.__get_random_dir_path()
        self.__audio_options = {

            # For youtube dl
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.__dynamic_options["preferred_audio_codec"]
            }],
            'format': f'bestaudio/best[filesize<{self.__dynamic_options["max_file_size"]}]',
            'noplaylist': True,
            "outtmpl": os.path.join(save_dir, "TEMP" + ".%(ext)s"),

            # For custom downloader class 
            "dl_type": "audio",
            "save_dir": save_dir,
            "max_duration_seconds": self.__dynamic_options["max_audio_duration_seconds"]
        }

        self.__video_options = {

            # For youtube dl
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': self.__dynamic_options["preferred_video_format"]
            }],
            'format': f'(bestvideo+bestaudio)[filesize<{self.__dynamic_options["max_file_size"]}]',
            # "yes_overwrites": True, # not working
            'noplaylist': True,
            "outtmpl": os.path.join(save_dir, "TEMP" + ".%(ext)s"),

            # For custom downloader class 
            "dl_type": "video",
            "save_dir": save_dir,
            "max_duration_seconds": self.__dynamic_options["max_video_duration_seconds"]
        }

        # add ffmpeg_location if exists
        if(self.__dynamic_options["ffmpeg_location"]):
            self.__audio_options["ffmpeg_location"] = self.__dynamic_options["ffmpeg_location"]
            self.__video_options["ffmpeg_location"] = self.__dynamic_options["ffmpeg_location"]

    def __get_random_dir_path(self):
        path = os.path.join("temp", str(uuid.uuid4()))
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def set_video_format(self, format):
        self.__video_options.update({"format": f'({format})[filesize<{self.__dynamic_options["max_file_size"]}]'})

    # def set_audio_format(self, format):
    #     self.__audio_options.update( {"format": f'{format}[filesize<{self.__dynamic_options["max_file_size"]}]'})

    def to_audio(self):
        return self.__audio_options

    def to_video(self):
        return self.__video_options
