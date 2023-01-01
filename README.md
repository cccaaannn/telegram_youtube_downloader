# Telegram YouTube downloader
---
## Telegram bot for downloading video or audio from [multiple](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) sites, you can run it with [single](#Running) command.

![GitHub top language](https://img.shields.io/github/languages/top/cccaaannn/telegram_youtube_downloader?color=blue&style=for-the-badge) [![GitHub release](https://img.shields.io/github/v/release/cccaaannn/telegram_youtube_downloader?color=blueviolet&style=for-the-badge)](https://github.com/cccaaannn/telegram_youtube_downloader/releases?style=flat-square) [![GitHub](https://img.shields.io/github/license/cccaaannn/telegram_youtube_downloader?color=brightgreen&style=for-the-badge)](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/LICENSE) [![Docker Pulls](https://img.shields.io/docker/pulls/cccaaannn/telegram_youtube_downloader?color=blue&style=for-the-badge)](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader) [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/cccaaannn/telegram_youtube_downloader/latest?color=teal&style=for-the-badge)](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader)

## Table of contents
- [Demo](#Demo)
- [Commands](#Commands)
  - [Download](#Download)
  - [Search](#Search)
  - [Utilities](#Utilities)
- [Running](#Running)
- [Docs](#Docs)

## Demo
<img src="https://github.com/cccaaannn/readme_media/blob/master/media/telegram_youtube_downloader/gifs/example_download_audio.gif?raw=true" alt="drawing" width="250"/> <img src="https://github.com/cccaaannn/readme_media/blob/master/media/telegram_youtube_downloader/gifs/example_download_menu.gif?raw=true" alt="drawing" width="253"/>

<br/>

## Commands

### 1. Download
```shell
/video <download url>
/video <format> <download url>
/v <download url>
```
```shell
/audio <download url>
/audio <format> <download url>
/a <download url>
```

### 3. Search
Makes a YouTube search to download. [Also see setup/search](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md#Search-command)
```shell
/search <query>
/s <query>
```

### 2. Utilities
General
```shell
/about
/help
```
Returns available formats. [See configurations](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md)
```shell
/formats
```
Returns available sites. [See configurations](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md)
```shell
/sites
```

## Running
You can also run the bot without Docker and with multiple other ways check [Setup](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md) for more information.
### Docker 
Run the container with your telegram bot key. [telegram_youtube_downloader docker image](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader)
```shell
sudo docker run -d --name telegram_youtube_downloader --restart unless-stopped -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> cccaaannn/telegram_youtube_downloader:latest
```

Example with all flags [Setup with Docker](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md#Docker)
  - Search feature [Setup/search](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md#Search-command)
  - Mapped logs
  - Custom configurations
```shell
sudo docker run -d --name telegram_youtube_downloader --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e YOUTUBE_API_KEY=<YOUTUBE_API_KEY> \
-v <YOUR_CONFIGS_PATH>/configs:/telegram_youtube_downloader/telegram_youtube_downloader/configs \
-v <YOUR_LOGS_PATH>/logs:/telegram_youtube_downloader/logs \
cccaaannn/telegram_youtube_downloader:latest
```

## Docs
### Also see
### [Setup](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md) for more ways to run the bot.
### [Configurations](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md) for all configurable options.
