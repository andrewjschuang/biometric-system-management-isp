# Biometric System Management using Face Recognition

## Current branch in development

`git checkout 0.1.2`

## How to use

Clone repository

`git clone git@github.com:andrewjschuang/biometric-system-management-isp.git`

Switch to latest branch - check above for latest branch

`git checkout x.x.x`

Create virtual environment

`cd biometric-system-management-isp/`

`python3 -m venv ve`

Activate virtual environment

`source ve/bin/activate`

Install requirements

`pip install -r requirements.txt`

Add some pictures

`python fr_encodings.py path/to/picture.jpg "name of person" --filename=path/to/save/file`

Fire up webcam to begin using Face Recognition

`python video_capture.py --display=true --encodings=path/to/encoding/files --tolerance=0.4`

## How to use

Clone repository

`git clone git@github.com:andrewjschuang/biometric-system-management-isp.git`

Create virtual environment

`cd biometric-system-management-isp/`

`python3 -m venv ve`

Activate virtual environment

`source ve/bin/activate`

Install requirements

`pip install -r requirements.txt`

Add some pictures

`python fr_encodings.py path/to/picture.jpg "name of person" --filename=path/to/save/file`

Fire up webcam to begin using Face Recognition

`python video_capture.py --display=true --encodings=path/to/encoding/files --tolerance=0.4`

## Docker Compose
You may use Docker to run the application
`docker-compose up -d`

Before executing the command above, add a volume in docker-compose.yml to copy your encodings folder to inside the container
`volumes:`
`  - /local/path/to/encodings:/app/encodings`


## Special thanks to:
https://github.com/ageitgey/face_recognition
