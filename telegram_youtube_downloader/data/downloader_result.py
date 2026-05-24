from dataclasses import dataclass


@dataclass
class DownloaderResult:
	file_path: str
	file_name: str
