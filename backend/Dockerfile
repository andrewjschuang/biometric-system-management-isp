# Contains Python 3.12
FROM ubuntu:24.04

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=0
ENV OPENCV_FFMPEG_CAPTURE_OPTIONS=null

RUN apt-get -y update && apt-get install -y --no-install-recommends \
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
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    libopencv-dev \
    pkg-config \
    python3-pip \
    python3.12-venv \
    python3-dev \
    python3-numpy \
    python3-opencv \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# # Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry install

CMD ["poetry", "run", "python", "-m", "server"]
