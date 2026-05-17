FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Install system dependencies
RUN apk add ffmpeg --no-cache

# Install python dependencies
WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./
ENV UV_NO_DEV=1

# Install dependencies only, always upgrade yt-dlp to latest
RUN uv sync --no-install-project --upgrade-package yt-dlp

# Add volumes for performance with io intensive operations
VOLUME /app/logs
VOLUME /app/temp

# Copy app
COPY telegram_youtube_downloader /app/telegram_youtube_downloader

# Install the project itself as package
RUN uv sync

# Run
CMD ["uv", "run", "tyd"]
