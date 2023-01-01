# Setup

--- 

## Table of contents
- [Preliminary steps](#Preliminary-steps)
- [Running](#Running)
    1. [Docker](#Docker)
    2. [Ubuntu](#Ubuntu)
    3. [Windows](#Windows)
- [Search command](#Search-command)
- [Alternative ways to pass keys](#Alternative-ways-to-pass-keys)

<br>

## **Preliminary steps**
1. Get a telegram bot key.
2. (optional) Get a youtube api key. [See search command](#Search-command)

---

## **Running**

## 1. Docker
1. Install Docker. [docker docs](https://docs.docker.com/engine/install/ubuntu/)
```shell
sudo apt update
sudo apt install docker.io -y
```
2. Run the container with your bot key. [telegram_youtube_downloader docker image](https://hub.docker.com/r/cccaaannn/telegram_youtube_downloader)
```shell
sudo docker run -d --name telegram_youtube_downloader --restart unless-stopped -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> cccaaannn/telegram_youtube_downloader:latest
```

**Optional flags**

- To run bot with search feature
```shell
-e YOUTUBE_API_KEY=<YOUTUBE_API_KEY>
```
- Mapping config folder to a volume for setting custom configurations.
```shell
-v /home/can/configs:/telegram_youtube_downloader/telegram_youtube_downloader/configs
```
- Mapping logs to a volume.
```shell
-v /home/can/logs:/telegram_youtube_downloader/logs
```
- **Example with all flags**
```shell
sudo docker run -d --name telegram_youtube_downloader --restart unless-stopped \
-e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> \
-e YOUTUBE_API_KEY=<YOUTUBE_API_KEY> \
-v <YOUR_CONFIGS_PATH>/configs:/telegram_youtube_downloader/telegram_youtube_downloader/configs \
-v <YOUR_LOGS_PATH>/logs:/telegram_youtube_downloader/logs \
cccaaannn/telegram_youtube_downloader:latest
```

---

## 2. Ubuntu
1. Install ffmpeg
```shell
sudo apt update
sudo apt upgrade -y
sudo apt install ffmpeg -y
```
2. Install python and virtualenv
```shell
sudo apt install python3 -y
sudo apt install python3-pip -y

sudo apt install python3-virtualenv -y
```
3. Add your bot key to environment. Also check the [alternative ways to pass keys](#Alternative-ways-to-pass-keys).
```shell
export TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY>
source ~/.bashrc
```
- (optional) To run bot with search feature
```shell
export YOUTUBE_API_KEY=<YOUTUBE_API_KEY>
source ~/.bashrc
```
4. Install the repository and run the bot 
```shell
# Install repository
git clone https://github.com/cccaaannn/telegram_youtube_downloader.git
cd telegram_youtube_downloader

# Create virtualenv
virtualenv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run
python telegram_youtube_downloader
```

---

## 3. Windows
1. Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/).
    - Add `ffmpeg` to path, or add the binary path to `telegram_youtube_downloader\configs\config.yaml`. [See configurations](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md).
2. Install latest python from [python.org](https://www.python.org/downloads/).
3. Install requirements.
```shell
pip install -r requirements.txt
```
4. Run on cmd/terminal. Also check [Alternative ways to pass keys](#Alternative-ways-to-pass-keys).

```shell
python telegram_youtube_downloader -k <TELEGRAM_BOT_KEY>
```
- (optional) To run bot with search feature
```shell
python telegram_youtube_downloader -k <TELEGRAM_BOT_KEY>,<YOUTUBE_API_KEY>
```

---

<br>

## **Search command**
- `/search` is an optional feature, and requires a youtube api key.
- With search enabled you can make youtube searches and download from search results that listed as a button menu. 
- **You can get the key from [console.developers.google.com](https://console.developers.google.com/)**

<br/>

## **Alternative ways to pass keys**
1. With environment (Default)
    - `TELEGRAM_BOT_KEY` key must be present on environment variables.
    - To use `/search`, `YOUTUBE_API_KEY` key must be present on environment variables.
```shell
python telegram_youtube_downloader
```
2. With file
    - First line has to be <TELEGRAM_BOT_KEY>.
    - To use `/search`, <YOUTUBE_API_KEY> should be on the second line.
```shell
python telegram_youtube_downloader -f <FILE_PATH_FOR_KEYS>
```
3. Directly
```shell
python telegram_youtube_downloader -k <TELEGRAM_BOT_KEY>
```
```shell
python telegram_youtube_downloader -k <TELEGRAM_BOT_KEY>,<YOUTUBE_API_KEY>
```