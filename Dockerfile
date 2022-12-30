FROM ubuntu

# Install system dependencies
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

# Install python dependencies
WORKDIR /telegram_youtube_downloader
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Copy app
COPY . /telegram_youtube_downloader

# Run
CMD ["python3", "telegram_youtube_downloader"]