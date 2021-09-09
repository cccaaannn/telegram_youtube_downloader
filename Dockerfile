FROM ubuntu

# install system dependencies
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

# copy app
COPY . /home/telegram_youtube_downloader

# install python dependencies
WORKDIR /home/telegram_youtube_downloader
RUN pip3 install -r requirements.txt

# run
WORKDIR /home/telegram_youtube_downloader/src
CMD ["python3", "run.py", "-e"]
