## **telegram_youtube_downloader**
---
Telegram bot for downloading and sending youtube videos.

![](https://img.shields.io/github/repo-size/cccaaannn/telegram_youtube_downloader?style=flat-square) [![GitHub license](https://img.shields.io/github/license/cccaaannn/telegram_youtube_downloader?style=flat-square)](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/LICENSE)


### **Bot commands**
- /help
- /formats
- /audio "youtube link"
- /video "youtube link" or /video 480p "youtube link"

<br/>

### **Setting it up**
- Download ffmpeg for your os from [ffmpeg.org](https://ffmpeg.org/).
- Put ffmpeg files in the ffmpeg folder in the project.
- Get a telegram bot key.
- Pass the key to the run_bot function.
- It will work. (I hope 🤷🏻‍♂️)

<br/>

### **Configurations**
Configuration file contains several options.
- Logger name, file path-name, log level.
- Bad chars and their replacements. (mostly for windows)
- Video formats and their command names. (for more video formats youtube_dl documentations [youtube_dl](https://youtube-dl.org/))
- Preferred video format and audio codec.
- Audio and video sending timeout intervals. (if you are running this on a slow internet, increase those)
- Maximum allowed video duration.
- Function usage descriptions.
- Temp file location.




