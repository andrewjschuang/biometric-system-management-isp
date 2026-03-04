FROM andrewjsc/bmsisp-base:py3.12-dlib19.24.8

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED=1
ENV OPENCV_FFMPEG_CAPTURE_OPTIONS="rtsp_transport;tcp|stimeout;10000000"
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# dlib and face_recognition already installed in base image venv.
# Poetry detects them via pip metadata and skips recompilation.
RUN /app/.venv/bin/poetry install --no-root

COPY . /app

CMD ["poetry", "run", "python", "-m", "server"]
