# Api server

---

### Running with custom api server has some advantages [using-a-local-bot-api-server](https://core.telegram.org/bots/api#using-a-local-bot-api-server) like uploading files up to 2000 MB

## Table of contents
- [Preliminary steps](#preliminary-steps)
- [Update config](#update-config)
- [Docker compose](#docker-compose)

## Preliminary steps
1. Create a application from [https://core.telegram.org/api/obtaining_api_id](https://core.telegram.org/api/obtaining_api_id).
2. Get `api_id` and `api_hash`.

## Update config
1. Copy default config file and update this line with your api server url, this example uses custom docker bridge network.
```yaml
telegram_bot_options:
  base_url: http://telegram-bot-api:8081/bot
```
2. (optional) Also increase default download timeouts and download duration limits.
```yaml
telegram_bot_options:
  video_timeout_seconds: 300
  audio_timeout_seconds: 300

youtube_downloader_options:
  max_video_duration_seconds: 1200
  max_audio_duration_seconds: 3000
```
3. (optional) If you don't have a fast machine file conversions might take too long on longer videos, you can remove `postprocessors` section to make it faster but you will get mkv files.
```yaml
youtube_downloader_options:
  video_options:
    # postprocessors: 
    #   - key: "FFmpegVideoConvertor"
    #     preferedformat: "mp4"
    format: "bestvideo+bestaudio"
    noplaylist: true
```

## Docker compose
- This example uses [aiogram/telegram-bot-api](https://hub.docker.com/r/aiogram/telegram-bot-api) image for api server, you can also install natively.
1. Update required fields with your credentials and save paths. 
2. Put your updated config file in to correct location on the host machine.
3. Run with `docker compose up -d`
```yaml
services:
  telegram-bot-api:
    image: aiogram/telegram-bot-api:latest
    container_name: telegram-bot-api
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G
    networks:
      - telegram_bot_internal
    ports:
      - 8081
    environment:
      TELEGRAM_API_ID: <API_ID>
      TELEGRAM_API_HASH: <API_HASH>
    volumes:
      - <YOUR_BASE_PATH>/telegram_bot_api:/var/lib/telegram-bot-api

  telegram-youtube-downloader:
    image: cccaaannn/telegram_youtube_downloader:latest
    container_name: telegram-youtube-downloader
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G
    networks:
      - telegram_bot_internal
    environment:
      TELEGRAM_BOT_KEY: <TELEGRAM_BOT_KEY>
    #   YOUTUBE_API_KEY: <YOUTUBE_API_KEY>
    volumes:
      - <YOUR_BASE_PATH>/telegram_youtube_downloader/configs:/telegram_youtube_downloader/telegram_youtube_downloader/configs
    #   - <YOUR_BASE_PATH>/telegram_youtube_downloader/logs:/telegram_youtube_downloader/logs
    depends_on:
      - telegram-bot-api

networks:
  telegram_bot_internal:
    name: telegram_bot_internal
```
