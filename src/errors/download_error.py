class DownloadError(Exception):
    def __init__(self, msg="Download error", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)