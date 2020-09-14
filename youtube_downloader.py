from __future__ import unicode_literals
import youtube_dl
import logging
import os


class youtube_downloader():
    """uses youtube_dl to download
    https://github.com/ytdl-org/youtube-dl
    """

    def __init__(self, temp_folder_path = "tmp", log_file=None, log_level=20):
        
        # downloader variables
        self.__youtube_dl_options()
        self.temp_folder_path = temp_folder_path

        self.possible_extensions = ['.mp4', '.mkv', '.webm', ".mp3"]

        # logging variables
        self.logger_name = __name__
        self.log_file = log_file
        self.log_level = log_level
        self.__set_logger()

    # logging stuff
    def __set_logger(self):
        self.logger = logging.getLogger(self.logger_name)  

        if(not self.logger.handlers):
            self.logger.setLevel(self.log_level)
            
            # log formatter
            formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

            # stream handler
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

            # file handler
            if(self.log_file):
                file_handler = logging.FileHandler(self.log_file)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            

    def  __youtube_dl_options(self):
        self.ydl_opts_audio = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        "ffmpeg_location" : "ffmpeg/",
        'format': 'bestaudio/best',
        # "verbose": True, 
        'noplaylist' : True,
        "outtmpl": "tmp" + "/%(title)s.%(ext)s",
        # "progress_hooks": [self.__hook],
        }

        self.ydl_opts_video = {
        "ffmpeg_location" : "ffmpeg/",
        'format': 'bestvideo+bestaudio',
        # "verbose": True,
        # "yes_overwrites": True, # not working
        'noplaylist' : True,
        "outtmpl": "tmp" + "/%(title)s.%(ext)s",
        # "progress_hooks": [self.__hook],
        }

        self.video_formats = {"1080p":"137+bestaudio/best", "720p":"136+bestaudio/best", "480p":"135+bestaudio/best", "360p":"134+bestaudio/best", "240p":"133+bestaudio/best"}



    def __find_file_extension(self, path_without_extension):
        """this function exists because youtube-dl does not gives me the path -___-"""
        for possible_extension in self.possible_extensions:
            if os.path.isfile(os.path.join(self.temp_folder_path, path_without_extension + possible_extension)):
                return os.path.join(self.temp_folder_path, path_without_extension + possible_extension)
        else:
            return 0


    def get_video_types(self):
        self.logger.info("Function name: get_video_types")
        return str(self.video_formats)


    def rm_downloaded_file(self, path):
        # self.logger.info("Function name: rm_downloaded_file args: {0}".format(path))
        self.logger.info("Function name: rm_downloaded_file") # cant log some unicode characters
        if(os.path.normpath(os.path.normcase(os.path.dirname(path))) == os.path.normpath(os.path.normcase(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.temp_folder_path)))):
            if os.path.isfile(path):
                os.remove(path)
        else:
            self.logger.warning("path is not in the {0}".format(self.temp_folder_path))

        # print(os.path.normcase(os.path.dirname(path)))
        # print(os.path.normcase(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.temp_folder_path)))


    def download(self, link, dl_type = "audio", dl_format = "720p"):
        self.logger.info("Function name: download args: {0}, dl_type = {1}, dl_format = {2}".format(link, dl_type, dl_format))

        temp_ydl_options = {}
        if(dl_type == "audio"):
            temp_ydl_options = self.ydl_opts_audio.copy()
        elif(dl_type == "video"):
            temp_ydl_options = self.ydl_opts_video.copy() # deep copy to keep the template

            if(dl_format not in self.video_formats):
                self.logger.warning("video format is not supported {0}".format(dl_format))
                return 0, "video format is not supported"
            
            temp_ydl_options.update({"format":self.video_formats[dl_format]})

        else:
            self.logger.warning("download type is not supported {0}".format(dl_type))
            return 0, "download type is not supported"


        try:
            with youtube_dl.YoutubeDL(temp_ydl_options) as ydl:
                
                # youtube_dl can not override existing video for some reason so I delete it before
                meta = ydl.extract_info(link, download=False)
                old_file = self.__find_file_extension(meta["title"])
                if(old_file):
                    old_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), old_file)
                    self.rm_downloaded_file(old_file)
                    # os.remove(old_file)

                # download
                meta = ydl.extract_info(link, download=True)
                # ydl.download([link])

                downloaded_file_path = self.__find_file_extension(meta["title"])

                if(not downloaded_file_path):
                    self.logger.error("downloaded video extension is not supported, video title is {0}".format(meta["title"]))
                    return 0, "downloaded video extension is not supported"

                # success
                return 1, downloaded_file_path
        
        except:
            self.logger.error("download error", exc_info=True)
            return 0, "download error"






if __name__ == "__main__":
    link = 'https://www.youtube.com/watch?v=a3ICNMQW7Ok'

    ytd = youtube_downloader()

    status, path = ytd.download(link, dl_type="audio", dl_format="720p")

    print(status, path)

    # delete if exists
    # if(status):
    #     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    #     ytd.rm_downloaded_file(path)





