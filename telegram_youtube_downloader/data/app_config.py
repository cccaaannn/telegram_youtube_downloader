from dataclasses import dataclass, field
from typing import List, Optional
import inspect

from statics.default_command_type import DefaultCommandType
from statics.authorization_mode import AuthorizationMode
from data.dl_format import DlFormat


@dataclass
class LoggerOptions:
	log_path: str
	root_log_level: int
	app_log_level: int
	backup_count: int
	max_bytes: int

@dataclass
class AuthorizationUser:
	id: int
	claims: str

	def split_claims(self):
		return self.claims.split(",")

@dataclass
class AuthorizationOptions:
	mode: AuthorizationMode
	users: List[AuthorizationUser] = field(default_factory=list)

@dataclass
class TelegramBotOptions:
	text_timeout_seconds: int
	video_timeout_seconds: int
	audio_timeout_seconds: int
	base_url: Optional[str] = None
	default_command: Optional[DefaultCommandType] = None
	authorization_options: AuthorizationOptions = field(default_factory=lambda: AuthorizationOptions(AuthorizationMode.DISABLED, []))

@dataclass
class YoutubeSearchOptions:
	max_results: int

@dataclass
class AllowedUrlPattern:
	name: str
	pattern: str

@dataclass
class YoutubeFormats:
	VIDEO: List[DlFormat]
	AUDIO: List[DlFormat]
	def from_string(self, content_type: str) -> List[DlFormat]:
		if content_type == "VIDEO":
			return self.VIDEO
		if content_type == "AUDIO":
			return self.AUDIO
		return []

@dataclass
class YoutubeDownloaderOptions:
	max_video_duration_seconds: int
	max_audio_duration_seconds: int
	audio_options: dict = field(default_factory=dict)
	video_options: dict = field(default_factory=dict)
	allowed_url_patterns: List[AllowedUrlPattern] = field(default_factory=list)
	formats: YoutubeFormats = field(default_factory=lambda: YoutubeFormats([], []))

@dataclass
class AppConfig:
	logger_options: LoggerOptions
	telegram_bot_options: TelegramBotOptions
	youtube_search_options: YoutubeSearchOptions
	youtube_downloader_options: YoutubeDownloaderOptions

	def __str__(self) -> str:
		return inspect.cleandoc(f""" \
		Config(
		  logger_options={self.logger_options}
		  telegram_bot_options={self.telegram_bot_options}
		  youtube_search_options={self.youtube_search_options}
		  youtube_downloader_options=YoutubeDownloaderOptions(
		    max_video_duration_seconds={self.youtube_downloader_options.max_video_duration_seconds}
		    max_audio_duration_seconds={self.youtube_downloader_options.max_audio_duration_seconds}
		    audio_options={self.youtube_downloader_options.audio_options}
		    video_options={self.youtube_downloader_options.video_options}
		    allowed_url_patterns={self.youtube_downloader_options.allowed_url_patterns}
		    formats={self.youtube_downloader_options.formats}
		  )
		)""")
