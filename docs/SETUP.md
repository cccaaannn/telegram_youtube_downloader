# Setup

---

## Table of contents
- [Preliminary steps](#preliminary-steps)
- [Running](#running)
    1. [Docker](#1-docker)
    2. [Docker compose](#2-docker-compose)
    3. [Terraform](#3-terraform)
    4. [Ubuntu (with python)](#4-ubuntu)
    5. [Windows (with python)](#5-windows)
- [Search command](#search-command)
- [Alternative ways to pass keys](#alternative-ways-to-pass-keys)

<br>

## Preliminary steps
1. Get a telegram bot key.
2. (optional) Get a youtube api key. [See search command](#Search-command)

---

## Running

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

- You can set any config value with environment variables using `__` convention. [See configurations](https://github.com/cccaaannn/telegram_youtube_downloader/blob/master/docs/CONFIGURATIONS.md#set-config-via-env)
    ```shell
    -e telegram_bot_options__default_command=video
    -e telegram_bot_options__authorization_options__users__0__id=123
    -e telegram_bot_options__authorization_options__users__0__claims=audio,help
    ```
- To run bot with search feature
    ```shell
    -e YOUTUBE_API_KEY=<YOUTUBE_API_KEY>
    ```
- Mapping config folder to a volume for setting custom configurations.
    ```shell
    -v <YOUR_BASE_PATH>/configs:/app/telegram_youtube_downloader/configs
    ```
- Mapping logs to a volume.
    ```shell
    -v <YOUR_BASE_PATH>/logs:/app/logs
    ```

---

## 2. Docker compose
1. Copy `compose/.env.template` to `compose/.env`, add your `TELEGRAM_BOT_KEY`
2. Run with `docker compose -f compose/default.yaml up -d`
3. (optional) You can add more custom configuration in your `.env` or directly update compose files.

- Container data is saved under `compose/tyd_data` by default, you can configure it from composes.

- There are multiple prebuilt compose examples under `/compose`
    - Use with DockerHub build `docker compose -f compose/default.yaml up -d`
    - Use with local build `docker compose -f compose/local.yaml up -d`
    - Use with api server `docker compose -f compose/apisv.yaml up -d`

---

## 3. Terraform

1. Prepare cli tools
    1. Install [terraform cli](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
    2. Install [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
    3. Configure aws cli with your credentials.
        ```shell
        aws configure
        ```
2. Clone the repository and switch to `terraform/aws` directory
    ```shell
    git clone https://github.com/cccaaannn/telegram_youtube_downloader.git
    cd telegram_youtube_downloader/terraform/aws
    ```
3. Initialize terraform
    ```shell
    terraform init
    ```
4. Plan the deployment (optional)
    ```shell
    terraform plan
    ```
5. Apply the deployment
    ```shell
    terraform apply
    ```
- To delete the deployment (You can leave prompted parameters empty while destroying)
    ```shell
    terraform destroy
    ```

### Operating terraform deployment
- Deployment creates a pem file named `aws-tyd-key.pem` in the terraform directory. You can use this file to ssh to the ec2 instance.
    ```shell
    ssh -i aws-tyd-key.pem ec2-user@<ec2-ip>
    ```
- Update your cookies file on ec2, if provided
    - You might need to `chmod 700 aws-tyd-key.pem` on linux.
    ```shell
    scp -i aws-tyd-key.pem <cookiefile-path>/cookies.txt ec2-user@<ec2-ip>:/telegram_youtube_downloader/cookies/cookies.txt
    ```

---

## 4. Ubuntu
- Tested with `Ubuntu 24` - `Python 3.12`
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

## 5. Windows
- Tested with `Windows 10` - `Python 3.12`
1. Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/).
    - Add `ffmpeg` to path.
2. Install python from [python.org](https://www.python.org/downloads/).
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

## Search command
- `/search` is an optional feature, and requires a youtube api key.
- With search enabled you can make youtube searches and download from search results that listed as a button menu. 
- **You can get the key from [console.developers.google.com](https://console.developers.google.com/)**

## Alternative ways to pass keys
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
