from __future__ import unicode_literals
import youtube_dl
import logging
import re
import os


class youtube_downloader():
    """uses youtube_dl to download
    https://github.com/ytdl-org/youtube-dl
    """

    def __init__(self, 
    logger_name="telegram", 
    log_file=None, 
    log_level=20, 
    temp_folder_path="tmp", 
    temp_file_name="temp", 
    bad_chars={'"':'\'','<':'','>':'',':':'','/':'','\\':'','|':'','?':'','*':''},
    video_formats={"1080p":"137+bestaudio/best", "720p":"136+bestaudio/best", "480p":"135+bestaudio/best", "360p":"134+bestaudio/best", "240p":"133+bestaudio/best"},
    preferred_video_format="mp4",
    preferred_audio_codec="mp3",
    max_video_duration = 1200
    ):

        # downloader variables
        self.temp_folder_path = temp_folder_path
        self.temp_file_name = temp_file_name
        self.video_formats = video_formats
        self.bad_chars = bad_chars
        self.preferred_video_format = preferred_video_format
        self.preferred_audio_codec = preferred_audio_codec
        self.max_video_duration = max_video_duration
        self.__youtube_dl_options()

        # logging variables
        self.logger_name = logger_name
        self.log_file = log_file
        self.log_level = log_level
        self.__set_logger()

    # logging stuff
    def __set_logger(self):
        """creates the downloader logger"""
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
        """youtube_dl download templates"""
        self.ydl_opts_audio = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': self.preferred_audio_codec,
            'preferredquality': '192',
        }],
        "ffmpeg_location" : "ffmpeg/",
        'format': 'bestaudio/best',
        'noplaylist' : True,
        "outtmpl": os.path.join(self.temp_folder_path, self.temp_file_name + ".%(ext)s"),
        # "progress_hooks": [self.__hook],
        }

        self.ydl_opts_video = {
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': self.preferred_video_format,
        }],
        "ffmpeg_location" : "ffmpeg/",
        'format': 'bestvideo+bestaudio',
        # "yes_overwrites": True, # not working
        'noplaylist' : True,
        "outtmpl": os.path.join(self.temp_folder_path, self.temp_file_name + ".%(ext)s"),
        # "progress_hooks": [self.__hook],
        }

    def __is_youtube_link(self, link):
        pattern = r"https://(www.youtube.com/|www.m.youtube.com/|m.youtube.com/|youtu.be/)"
        compiled_pattern = re.compile(pattern)
        match = compiled_pattern.match(link)
        return match

    def __remove_keep_files_form_lists(self, l):
        """git cant track empty files so this removes .keep files from lists to prevent deletion or errors"""
        if(os.path.isfile(os.path.join(self.temp_folder_path, ".keep"))):
            l.remove(".keep")

    def __clear_temp_folder(self):
        """clears temp folder before download because youtube_dl can't override files and can't give you the path.
        I need to list all the temp folder to find downloaded file, there can't be another file here or exception occurres"""
        files = os.listdir(self.temp_folder_path)
        self.__remove_keep_files_form_lists(files)
        for f in files:
            os.remove(os.path.join(self.temp_folder_path, f))
        
    def __clean_bad_chars(self, filename):
        """cleans bad chars from the path because Bill Gates just wants to give me pain"""
        for char in self.bad_chars:
            filename = filename.replace(char, self.bad_chars[char])
        return filename

    def __rename_downloaded_file(self, video_title):
        """renames downloaded temp file to videos title. 
        there is no way to know the extension of the file that youtube_dl downloaded so I get all files in the temp folder and rename after download"""
        temp_file_locations = os.listdir(self.temp_folder_path)
        self.__remove_keep_files_form_lists(temp_file_locations)
        
        if(len(temp_file_locations) != 1):
            self.logger.error("multiple files exists in the temp folder")
            return 0, "downloaded video caused error (possibly because of the video format)"
        temp_file_location = os.path.join(self.temp_folder_path, temp_file_locations[0])

        if(not os.path.isfile(temp_file_location)):
            self.logger.error("downloaded file is not a path")
            return 0, "download error"

        try:
            # fix bad chars for windows
            video_title = self.__clean_bad_chars(video_title)

            _, file_extension = os.path.splitext(temp_file_location)
            new_file_path = os.path.normpath(os.path.join(self.temp_folder_path, video_title + file_extension))
            os.rename(temp_file_location, new_file_path)

            return 1, new_file_path
        except:
            self.logger.error("read the exception", exc_info=True)
            return 0, "downloaded video caused error (possibly because of the video title has some bad chars)"


    def get_video_formats(self):
        """returns video formats"""
        self.logger.info("Function name: get_video_types")
        str_formats = ""
        for str_format in self.video_formats:
            str_formats += str_format + " " 
        return str_formats

    def download(self, link, dl_type = "audio", dl_format = "default"):
        self.logger.info("Function name: download args: {0}, dl_type = {1}, dl_format = {2}".format(link, dl_type, dl_format))

        # parameter checking
        if(dl_type == "audio"):
            temp_ydl_options = self.ydl_opts_audio.copy()
        elif(dl_type == "video"):
            temp_ydl_options = self.ydl_opts_video.copy() # deep copy to keep the template

            if(dl_format not in self.video_formats):
                self.logger.warning("video format is not supported {0}".format(dl_format))
                return 0, "video format is not supported"
            
            # update the format in the template with the selected one
            temp_ydl_options.update({"format":self.video_formats[dl_format]})

        else:
            self.logger.warning("download type is not supported {0}".format(dl_type))
            return 0, "download type is not supported"

        # check the link
        match = self.__is_youtube_link(link)
        if(not match):
            self.logger.warning("link is not from youtube {0}".format(link))
            return 0, "link is not from youtube"

        # start download stage
        try:
            with youtube_dl.YoutubeDL(temp_ydl_options) as ydl:
                
                # get video info for checking duration
                meta = ydl.extract_info(link, download=False) 
                if(meta["duration"] > self.max_video_duration):
                    return 0, "video duration exceeds defined limit of {0} ".format(self.max_video_duration)

                # clear teh temp folder
                self.__clear_temp_folder()

                # download
                meta = ydl.extract_info(link, download=True) 

                # rename the temp video name with videos original title (bad windows path chars are replaced)
                path_status, info_or_path = self.__rename_downloaded_file(meta["title"])

                # if path_status is 0 return the error
                if(not path_status):
                    return 0, info_or_path

                # success
                return 1, info_or_path
        
        except:
            self.logger.error("download error", exc_info=True)
            return 0, "download error"





# if __name__ == "__main__":
#     link = 'https://www.youtube.com/watch?v=a3ICNMQW7Ok'

#     ytd = youtube_downloader()

#     status, path = ytd.download(link, dl_type="audio", dl_format="720p")

#     print(status, path)

