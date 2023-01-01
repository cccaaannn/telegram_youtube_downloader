# Configurations

---

## Table of contents
- [logger_options](#`logger_options`)
- [telegram_bot_options](#`telegram_bot_options`)
- [youtube_search_options](#`youtube_search_options`)
- [youtube_downloader_options](#`youtube_downloader_options`)
    - [audio_options and video_options](#`audio_options`-and-`video_options`)
    - [allowed_url_patterns](#`allowed_url_patterns`)
    - [formats](#`formats`)
- [Full config example](#Full-config-example)

<br>

### Configuration file `telegram_youtube_downloader\configs\config.yaml`.

---

### `logger_options`
```yaml
logger_options:
  log_path: logs   # Can be abs path
  log_level: 20    # info
```

---

### `telegram_bot_options`
### Timeouts for different media types
```yaml
telegram_bot_options:
  text_timeout_seconds: 30
  video_timeout_seconds: 300 
  audio_timeout_seconds: 300
```

---

### `youtube_search_options`
```yaml
youtube_search_options:
  max_results: 5   # Limit search results with 5
```

---

### `youtube_downloader_options`
```yaml
youtube_downloader_options:
  max_video_duration_seconds: 1200   # 20 min
  max_audio_duration_seconds: 3000   # 50 min
  ffmpeg_location: null              # 'null' will try to get from env as ffmpeg
```

### `audio_options` and `video_options`
### audio_options and video_options are directly passed to youtube_dl on their respective download types, you can add different flags to change download configurations.
### `format` property will be overridden by the default format on the formats section
```yaml
youtube_downloader_options:
  audio_options:
    postprocessors: 
      - key: "FFmpegExtractAudio"
        preferredcodec: "mp3"
    format: "bestaudio/best"
    noplaylist: true

  video_options:
    postprocessors: 
      - key: "FFmpegVideoConvertor"
        preferedformat: "mp4"
    format: "bestvideo+bestaudio"
    noplaylist: true
```

### `allowed_url_patterns` 
### Array of url regex for allowed paths, names will be used on `/sites` command
### Restrict sites with.
```yaml
allowed_url_patterns:
  - name: youtube
    pattern: "^https://(.*\\.?youtube.com/.*$|youtu.be$)"
  - name: instagram
    pattern: "^https://.*instagram.com/.*$"
  - name: twitter
    pattern: "^https://.*twitter.com/.*$"
  - name: facebook
    pattern: "^https://.*facebook.com/.*$"
```
### Allow all sites. Downloads still will be restricted by [supported sites of the yt-dlp lib](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
```yaml
allowed_url_patterns:
  - name: All sites allowed
    pattern: "^https://.*$"
```

### `formats`
### There has to be one value with `is_default=true` flag, it will be used on all downloads that does not specified a format.
### More format values can be found on [youtube-dl documentation](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#format-selection-examples) 
```yaml
youtube_downloader_options:
  formats:
    VIDEO:
      - name: best
        value: "bestvideo+bestaudio/best"
      - name: worst
        value: "worstvideo+worstaudio/worst"
      - name: 1080p
        value: "137+bestaudio/best"
      - name: 720p
        value: "136+bestaudio/best"
        is_default: true
      - name: 480p
        value: "135+bestaudio/best"
      - name: 360p
        value: "134+bestaudio/best"
      - name: 240p
        value: "133+bestaudio/best"
    AUDIO:
      - name: best
        value: "bestaudio/best"
        is_default: true
      - name: worst
        value: "worstaudio/worst"
```

---

### Full config example
```yaml
logger_options:
  log_path: logs                                  # Can be abs path
  log_level: 20                                   # info

telegram_bot_options:
  text_timeout_seconds: 30
  video_timeout_seconds: 300                      # 5 min  
  audio_timeout_seconds: 300                      # 5 min

youtube_search_options:
  max_results: 5                                  # Limit search results with 5

youtube_downloader_options:
  max_video_duration_seconds: 1200                # 20 min
  max_audio_duration_seconds: 3000                # 50 min
  ffmpeg_location: null                           # 'null' will try to get from env as ffmpeg

  audio_options:                                  # audio_options are directly passed to youtube_dl on audio downloads
    postprocessors: 
      - key: "FFmpegExtractAudio"
        preferredcodec: "mp3"
    format: "bestaudio/best"                      # format will be overridden by the default format on the formats section
    noplaylist: true

  video_options:                                  # video_options are directly passed to youtube_dl on video downloads
    postprocessors: 
      - key: "FFmpegVideoConvertor"
        preferedformat: "mp4"
    format: "bestvideo+bestaudio"                 # format will be overridden by the default format on the formats section
    noplaylist: true

  allowed_url_patterns:                           # Array of url regex for allowed paths, names will be used on '/sites' command
    - name: All sites allowed
      pattern: "^https://.*$"
  
  formats:
    VIDEO:
      - name: best
        value: "bestvideo+bestaudio/best"
      - name: worst
        value: "worstvideo+worstaudio/worst"
      - name: 1080p
        value: "137+bestaudio/best"
      - name: 720p
        value: "136+bestaudio/best"
        is_default: true
      - name: 480p
        value: "135+bestaudio/best"
      - name: 360p
        value: "134+bestaudio/best"
      - name: 240p
        value: "133+bestaudio/best"
    AUDIO:
      - name: best
        value: "bestaudio/best"
        is_default: true
      - name: worst
        value: "worstaudio/worst"

```