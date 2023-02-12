class AuthorizationError(Exception):
    def __init__(self, msg="Not authorized", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)