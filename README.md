# Telegram YouTube downloader
---
Telegram bot that downloads YouTube videos.

![GitHub top language](https://img.shields.io/github/languages/top/cccaaannn/telegram_youtube_downloader?style=flat-square) ![](https://img.shields.io/github/repo-size/cccaaannn/telegram_youtube_downloader?style=flat-square) [![GitHub license](https://img.shields.io/github/license/cccaaannn/telegram_youtube_downloader?style=flat-square)](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/LICENSE)


## **Table of contents**
- [Bot commands](#Bot-commands)
- [Setting it up](#Setting-it-up)
    - [Docker](#Docker)
    - [Ubuntu](#Ubuntu)
    - [Windows](#Windows)
- [Alternative ways to pass the bot key](#Alternative-ways-to-pass-the-bot-key)
- [Configurations](#Configurations)

</br>

## Bot commands
- /help
    - Shows help text.
- /formats
    - Shows supported formats.
- /audio "youtube link"
    - Converts video from the link to audio and sends it. 
- /video "youtube link" or /video 480p "youtube link"
    - Sends the video with selected resolution.

<br/>

## Setting it up
### Docker
1. Get a telegram bot key.
2. Install Docker. [docker docs](https://docs.docker.com/engine/install/ubuntu/)
```shell
sudo apt update
sudo apt install docker.io -y
```
3. Run the container with your bot key. [docker image](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader)
```shell
sudo docker run -d --name telegram_youtube_downloader -e TELEGRAM_BOT_KEY=<YOUR_BOT_KEY> cccaaannn/telegram_youtube_downloader
```

#### Or build from source for docker
```shell
git clone https://github.com/cccaaannn/telegram_youtube_downloader.git
cd telegram_youtube_downloader
docker build -t telegram_youtube_downloader .
sudo docker run -d --name telegram_youtube_downloader -e TELEGRAM_BOT_KEY=<YOUR_BOT_KEY> telegram_youtube_downloader
```

<br>

### Ubuntu
1. Get a telegram bot key.

2. Install ffmpeg
```shell
sudo apt update
sudo apt upgrade -y
sudo apt install ffmpeg -y
```

3. Install python and virtualenv
```shell
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.7 -y

sudo apt install python3-virtualenv -y
```

4. Add your bot key to environment. Also check the [alternative ways to pass the bot key](#Alternative-ways-to-pass-the-bot-key).
```shell
export TELEGRAM_BOT_KEY=<YOUR_BOT_KEY>
source /etc/environment
```

5. Install the repository and run the bot 
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
cd src
python run.py -e
```

5. Alternatively, you can run the bot on a terminal screen session.
```shell
# Install screen and create session
sudo apt install screen -y
screen -S telegram_ytd_bot

# Install repository
git clone https://github.com/cccaaannn/telegram_youtube_downloader.git
cd telegram_youtube_downloader

# Create virtualenv
virtualenv -p /usr/bin/python3.7 venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run
cd src
python run.py -e

# ctrl+a+d to detach from screen session
```

<br/>

### Windows

1. Get a telegram bot key.
2. Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/).
3. Put these ffmpeg files "`ffmpeg.exe`, `ffprobe.exe`, `ffplay.exe`" in the **src folder** or specify a folder path for ffmpeg from the `src/cfg/options.cfg`. [configurations](#Configurations).
4. Install python from [python.org](https://www.python.org/downloads/).
5. Install requirements.
```shell
pip install -r requirements.txt
```
7. Run the `src/run.py` script from terminal/cmd. Also check [Alternative ways to pass the bot key](#Alternative-ways-to-pass-the-bot-key).

```shell
python run.py -k <YOUR_BOT_KEY>
```

<br/>

## Alternative ways to pass the bot key
```shell
# With environment
export TELEGRAM_BOT_KEY=<YOUR_BOT_KEY>
source /etc/environment
python run.py --use_env

# With file
python run.py --use_file <FILE_PATH_FOR_KEY>

# Directly
python run.py --use_key <YOUR_BOT_KEY>
```

<br/>

## Configurations
Configuration file `src/cfg/options.cfg` contains several options.
- **ffmpeg path**. Ex: `"ffmpeg_location": "ffmpeg/"`
    - If you are using a package manager to download ffmpeg leave this empty.

- Maximum allowed video duration in seconds. Ex: `"max_video_duration": 1200`

- Audio and video sending timeout intervals in milliseconds.  Ex: `"timeout_video": 300000`
    - If you are running this on a slow internet, increase those.

- Preferred video format and audio codec. Ex: `"preferred_video_format": "mp4"`
    - It is not guaranteed that this format will be downloaded since it may not exists. Check  [youtube_dl](https://youtube-dl.org/).

- Video formats and their command names. 
    - For more video formats youtube_dl documentations [youtube_dl](https://youtube-dl.org/).

- Bad chars and their replacements. (mostly for windows)

- Logger name, file path, log level.

