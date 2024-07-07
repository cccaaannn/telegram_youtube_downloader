from dataclasses import dataclass


@dataclass
class DownloaderResult:
    file_path: str
    video_title: str
