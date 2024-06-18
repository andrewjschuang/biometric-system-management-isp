FROM python:3.6-slim-stretch

RUN apt-get -y update

RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=0
ENV OPENCV_FFMPEG_CAPTURE_OPTIONS=null

CMD ["python", "-m", "server"]
