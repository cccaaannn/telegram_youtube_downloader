# Telegram YouTube downloader
---
Multithreaded Telegram bot that downloads YouTube videos, you can run it with [single](#Docker) command.

![GitHub top language](https://img.shields.io/github/languages/top/cccaaannn/telegram_youtube_downloader?color=blue&style=for-the-badge) ![GitHub repo size](https://img.shields.io/github/repo-size/cccaaannn/telegram_youtube_downloader?color=purple&style=for-the-badge) [![GitHub](https://img.shields.io/github/license/cccaaannn/telegram_youtube_downloader?color=green&style=for-the-badge)](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/LICENSE) [![Docker Pulls](https://img.shields.io/docker/pulls/cccaaannn/telegram_youtube_downloader?color=blue&style=for-the-badge)](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader) [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/cccaaannn/telegram_youtube_downloader/latest?color=orange&style=for-the-badge)](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader)

## Table of contents
- [Demo](#Demo)
- [Bot commands](#Bot-commands)
- [Setting it up](#Setting-it-up)
    - [Docker](#Docker)
    - [Ubuntu](#Ubuntu)
    - [Windows](#Windows)
- [Search command](#Search-command)
- [Alternative ways to pass keys](#Alternative-ways-to-pass-keys)
- [Configurations](#Configurations)

## Demo
<img src="https://github.com/cccaaannn/readme_media/blob/master/media/telegram_youtube_downloader/gifs/example_download_audio.gif?raw=true" alt="drawing" width="250"/> <img src="https://github.com/cccaaannn/readme_media/blob/master/media/telegram_youtube_downloader/gifs/example_download_menu.gif?raw=true" alt="drawing" width="253"/>

<br/>

## Bot commands
- `/about`
- `/help`
- `/formats`
- `/audio` \<youtube link>
- `/video` \<youtube link> or `/video` 1080p \<youtube link>
- `/search` \<query>

<br/>

## Setting it up
### Docker
1. Get a telegram bot key.
2. (optional) Get a youtube api key. [See search command](#Search-command)
3. Install Docker. [docker docs](https://docs.docker.com/engine/install/ubuntu/)
```shell
sudo apt update
sudo apt install docker.io -y
```
4. Run the container with your bot key. [docker image](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader)
```shell
sudo docker run -d --name telegram_youtube_downloader -e TELEGRAM_BOT_KEY=<YOUR_BOT_KEY> cccaaannn/telegram_youtube_downloader:latest
```
- (optional) To run bot with search feature
```shell
sudo docker run -d --name telegram_youtube_downloader -e TELEGRAM_BOT_KEY=<YOUR_BOT_KEY> -e YOUTUBE_API_KEY=<YOUR_API_KEY> cccaaannn/telegram_youtube_downloader:latest
```
- (optional) Also you can map logs to a volume.
```shell
sudo docker run -d --name telegram_youtube_downloader -e TELEGRAM_BOT_KEY=<YOUR_BOT_KEY> -e YOUTUBE_API_KEY=<YOUR_API_KEY> -v /home/can/logs:/telegram_youtube_downloader/logs cccaaannn/telegram_youtube_downloader:latest
```

<br>

### Ubuntu
1. Get a telegram bot key.
2. (optional) Get a youtube api key. [See search command](#Search-command)
3. Install ffmpeg
```shell
sudo apt update
sudo apt upgrade -y
sudo apt install ffmpeg -y
```
4. Install python and virtualenv
```shell
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.7 -y

sudo apt install python3-virtualenv -y
```
5. Add your bot key to environment. Also check the [alternative ways to pass keys](#Alternative-ways-to-pass-keys).
```shell
export TELEGRAM_BOT_KEY=<YOUR_BOT_KEY>
source /etc/environment
```
- (optional) To run bot with search feature
```shell
export YOUTUBE_API_KEY=<YOUR_API_KEY>
source /etc/environment
```
6. Install the repository and run the bot 
```shell
# Install repository
git clone https://github.com/cccaaannn/telegram_youtube_downloader.git
cd telegram_youtube_downloader

# Create virtualenv
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run
python telegram_youtube_downloader
```

<br/>

### Windows

1. Get a telegram bot key.
2. (optional) Get a youtube api key. [See search command](#Search-command)
3. Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/).
4. Add `ffmpeg` to environment or add the path to `telegram_youtube_downloader\configs\config.yaml`. [configurations](#Configurations).
5. Install python from [python.org](https://www.python.org/downloads/).
6. Install requirements.
```shell
pip install -r requirements.txt
```
7. Run on cmd/terminal. Also check [Alternative ways to pass keys](#Alternative-ways-to-pass-keys).

```shell
python telegram_youtube_downloader -k <YOUR_BOT_KEY>
```
- (optional) To run bot with search feature
```shell
python telegram_youtube_downloader -k <YOUR_BOT_KEY>,<YOUR_API_KEY>
```

<br/>

## Search command
- `/search` is an optional feature, and requires a youtube api key.
- With search enabled you can make youtube searches and download from search results that listed as a button menu. 
- You can get the key from [console.developers.google.com](https://console.developers.google.com/)

<br/>

## Alternative ways to pass keys
1. With environment (Default)
    - `TELEGRAM_BOT_KEY` key must be present on environment variables.
    - To use `/search`, `YOUTUBE_API_KEY` key must be present on environment variables.
```shell
python telegram_youtube_downloader
```
2. With file
    - First line has to be <YOUR_BOT_KEY>.
    - To use `/search`, <YOUR_API_KEY> should be on the second line.
```shell
python telegram_youtube_downloader -f <FILE_PATH_FOR_KEYS>
```
3. Directly
```shell
python telegram_youtube_downloader -k <YOUR_BOT_KEY>
```
```shell
python telegram_youtube_downloader -k <YOUR_BOT_KEY>,<YOUR_API_KEY>
```

<br/>

## Configurations
Configuration file `telegram_youtube_downloader\configs\config.yaml`.
```yaml
logger_options:
  log_path: logs                                  # Can be abs path
  log_level: 20                                   # info

youtube_downloader_options:
  preferred_video_format: mp4
  preferred_audio_codec: mp3
  default_video_quality: 720p
  max_video_duration_seconds: 1200                # 20 min
  max_audio_duration_seconds: 7200                # 2 hours
  max_file_size: 45M                              # Telegram bots can send up to 50M
  ffmpeg_location: null                           # null will try to get from env as ffmpeg

telegram_bot_options:
  text_timeout_seconds: 30
  video_timeout_seconds: 300                      # 5 min  
  audio_timeout_seconds: 300                      # 5 min

youtube_search_options:
  max_results: 5                                  # Limit search results with 5
```

