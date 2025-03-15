# Telegram YouTube downloader
---
## Telegram bot for downloading video or audio from [multiple](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) sites, you can run it with [single](#running) command.

![GitHub top language](https://img.shields.io/github/languages/top/cccaaannn/telegram_youtube_downloader?color=blue&style=for-the-badge) [![GitHub release](https://img.shields.io/github/v/release/cccaaannn/telegram_youtube_downloader?color=blueviolet&style=for-the-badge)](https://github.com/cccaaannn/telegram_youtube_downloader/releases?style=flat-square) [![GitHub](https://img.shields.io/github/license/cccaaannn/telegram_youtube_downloader?color=brightgreen&style=for-the-badge)](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/LICENSE) [![Docker Pulls](https://img.shields.io/docker/pulls/cccaaannn/telegram_youtube_downloader?color=blue&style=for-the-badge)](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader) [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/cccaaannn/telegram_youtube_downloader/latest?color=teal&style=for-the-badge)](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader)

## Overview
- [Demo](#demo)
- [Commands](#commands)
- [Running and examples](#running)
- [Docs](#docs)

## Demo
<img src="https://github.com/cccaaannn/readme_media/blob/master/media/telegram_youtube_downloader/gifs/example_download_audio.gif?raw=true" alt="drawing" width="250"/> <img src="https://github.com/cccaaannn/readme_media/blob/master/media/telegram_youtube_downloader/gifs/example_download_menu.gif?raw=true" alt="drawing" width="253"/>

<br/>

## Commands

<details open>
<summary><strong>⏬ Download commands</strong></summary>

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
</details>

<details>
<summary><strong>🔎 Search command</strong></summary>

Performs a YouTube search to download. [Also see setup/search](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md#search-command)

```shell
/search <query>
/s <query>
```
</details>

<details>
<summary><strong>⚙️ Utility commands</strong></summary>

[See configurations](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md) for command configurations.

```shell
/formats
/sites
/help
/about
```
</details>

## Running

🚀 Simple usage. (To run without docker [see setup](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md))
```shell
docker run -d --name telegram_youtube_downloader --restart unless-stopped -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> cccaaannn/telegram_youtube_downloader:latest
```

<details>
<summary>🍪 Example with cookie file</summary>

You can use a [cookie file](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies) to download without getting blocked.

```shell
docker run -d --name telegram_youtube_downloader --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e youtube_downloader_options__audio_options__cookiefile=/telegram_youtube_downloader/cookies/cookies.txt \
-e youtube_downloader_options__video_options__cookiefile=/telegram_youtube_downloader/cookies/cookies.txt \
-v <YOUR_COOKIES_PATH>/cookies:/telegram_youtube_downloader/cookies \
cccaaannn/telegram_youtube_downloader:latest
```
</details>

<details>
<summary>🏠 Example with default command</summary>

You can set a [default command](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md#default_command) to run a download command on bare messages.

```shell
docker run -d --name telegram_youtube_downloader --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e telegram_bot_options__default_command=video \
cccaaannn/telegram_youtube_downloader:latest
```
</details>

<details>
<summary>🔑 Example with authorization</summary>

You can set authorization rules per user [see authorization config](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md#authorization_options).
If you have many users you can map the configs directory to a local directory and edit the config file.

```shell
docker run -d --name telegram_youtube_downloader --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e telegram_bot_options__authorization_options__mode=ALLOW_SELECTED \
-e telegram_bot_options__authorization_options__users__0__claims=all \
-e telegram_bot_options__authorization_options__users__0__id=<TELEGRAM_USER_ID_1> \
-e telegram_bot_options__authorization_options__users__1__claims=audio,help \
-e telegram_bot_options__authorization_options__users__1__id=<TELEGRAM_USER_ID_2> \
cccaaannn/telegram_youtube_downloader:latest
```
</details>

<details>
<summary>💾 Example with mapped volumes</summary>

1. You can map logs to a local directory. [See logger options](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md#logger_options).
2. You can also map the configs directory to a local directory if you have too many custom configurations.

```shell
docker run -d --name telegram_youtube_downloader --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-v <YOUR_LOGS_PATH>/logs:/telegram_youtube_downloader/logs \
-v <YOUR_CONFIGS_PATH>/configs:/telegram_youtube_downloader/telegram_youtube_downloader/configs \
cccaaannn/telegram_youtube_downloader:latest
```
</details>

<details>
<summary>🔎 Example with search</summary>

You can use search command to search videos on YouTube. [See search feature](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md#search-command).

```shell
docker run -d --name telegram_youtube_downloader --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e YOUTUBE_API_KEY=<YOUTUBE_API_KEY> \
cccaaannn/telegram_youtube_downloader:latest
```
</details>

## Daily build
This project depends on [yt-dlp](https://github.com/yt-dlp/yt-dlp) and it is constantly updated, a [daily Docker build](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader/tags) pipeline added to keep the project up to date with external dependencies. It is not tested so might not be stable but if you are getting download errors on the latest version you can use daily until latest is fixed.
```shell
docker run -d --name telegram_youtube_downloader --restart unless-stopped -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> cccaaannn/telegram_youtube_downloader:daily
```

## Docs
- [Setup](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/SETUP.md) for more ways to run the bot.
- [Configurations](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md) for all configurable options.
- [Hardware Acceleration](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/HARDWARE_ACCELERATION.md) for using ffmpeg with hardware acceleration.
- [Api Server](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/API_SERVER.md) for using with custom telegram api server with increased download limits.
