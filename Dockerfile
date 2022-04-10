FROM ubuntu

# Install system dependencies
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

# Copy app
COPY . /telegram_youtube_downloader

# Install python dependencies
WORKDIR /telegram_youtube_downloader
RUN pip3 install -r requirements.txt

# Run
CMD ["python3", "src/telegram_youtube_downloader.py"]