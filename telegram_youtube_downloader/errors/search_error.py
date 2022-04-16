class SearchError(Exception):
    def __init__(self, msg="Search error", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)