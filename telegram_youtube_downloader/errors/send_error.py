class SendError(Exception):
    def __init__(self, msg="Could not send message", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)