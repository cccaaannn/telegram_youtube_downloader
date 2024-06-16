FROM ubuntu:24.04

# Install system dependencies
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-venv -y

# Create a virtual environment and activate it
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install python dependencies
WORKDIR /telegram_youtube_downloader
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Copy app
COPY . /telegram_youtube_downloader

# Run
CMD ["python3", "telegram_youtube_downloader"]