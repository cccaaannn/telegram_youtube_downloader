FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Install system dependencies
RUN apk add ffmpeg --no-cache

# Install python dependencies
WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./
ENV UV_NO_DEV=1

# Upgrade unpinned dependencies
RUN uv sync --upgrade 

# Add volumes for performance with io intensive operations
VOLUME /app/logs
VOLUME /app/temp

# Copy app
COPY telegram_youtube_downloader /app/telegram_youtube_downloader

# Run
CMD ["uv", "run", "telegram_youtube_downloader"]