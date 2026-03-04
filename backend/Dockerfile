FROM python:3.12-slim

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=1
ENV OPENCV_FFMPEG_CAPTURE_OPTIONS="rtsp_transport;tcp|stimeout;10000000"
ENV PATH="/app/.venv/bin:$PATH"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get -y update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    libgraphicsmagick1-dev \
    libopenblas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    libopencv-dev \
    pkg-config \
    python3-dev \
    zip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN python -m venv /app/.venv && \
    /app/.venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel && \
    /app/.venv/bin/pip install --no-cache-dir poetry && \
    /app/.venv/bin/poetry install --no-root && \
    /app/.venv/bin/pip install --force-reinstall git+https://github.com/ageitgey/face_recognition_models

COPY . /app

CMD ["poetry", "run", "python", "-m", "server"]
