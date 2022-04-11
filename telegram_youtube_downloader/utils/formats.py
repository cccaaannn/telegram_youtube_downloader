class Formats():
    video_formats={
        "best": "bestvideo+bestaudio/best",
        "worst": "worstvideo+worstaudio/worst",
        "1080p": "137+bestaudio/best", 
        "720p": "136+bestaudio/best", 
        "480p": "135+bestaudio/best", 
        "360p": "134+bestaudio/best", 
        "240p": "133+bestaudio/best"
        }

    @classmethod
    def to_string(cls):
        formats_str = ""
        for index, format in enumerate(cls.video_formats.keys()):
            formats_str += f"'{format}'"
            if(len(cls.video_formats.keys())-1 != index):
                formats_str += ", "
        return formats_str
