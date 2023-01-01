from apiclient.discovery import build
import isodate

from utils.logger_factory import LoggerFactory
from errors.search_error import SearchError
from utils.api_key_utils import ApiKeyUtils
from utils.config_utils import ConfigUtils


class YoutubeSearcher:
    def __init__(self) -> None:
        self.__api_key = ApiKeyUtils.get_youtube_api_key()
        self.__search_options = ConfigUtils.read_cfg_file()["youtube_search_options"]
        self.__logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.__youtube_url_base = "https://www.youtube.com/watch?v="
        self.__is_initialized = False
        if(self.__api_key):
            self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)            
            self.__is_initialized = True


    def __getVideoDuration(self, videoId):
        """Fetches and converts video duration from iso ISO 8601 to h:m:s format, catches any errors"""
        try:
            video_detail = self.__youtube.videos().list(id=videoId, part='contentDetails', maxResults=1).execute()
            return str(isodate.parse_duration(video_detail['items'][0]["contentDetails"]["duration"]))
        except Exception as e:
            self.__logger.warn("Unknown error", exc_info=True)
            return "??:??"


    def is_initialized(self):
        return self.__is_initialized

    def search(self, query):
        if(not self.__is_initialized):
            raise SearchError("Search is not available")

        try:
            self.__logger.info(f"Search ran with query '{query}'")

            search_results = self.__youtube.search().list(q=query, part='snippet', type='video', maxResults=self.__search_options["max_results"]).execute()

            result = []
            for item in search_results['items']:
                temp = {
                    "title": item["snippet"]["title"],
                    "url":  self.__youtube_url_base + item["id"]["videoId"],
                    "duration": self.__getVideoDuration(item["id"]["videoId"])
                }
                result.append(temp)

            if(len(result) == 0):
                raise SearchError(f"No results found for query {query}")

            return result

        except SearchError as se:
            self.__logger.warn(str(se))
            raise se
        except:
            self.__logger.error("Unknown error", exc_info=True)
            raise SearchError()
