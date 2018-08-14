# Biometric System Management using Face Recognition

## Current branch in development

`git checkout 0.1.1`

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

## Files and scripts

Crops faces in a set of pictures

`python crop.py filename_to_save`

Compares faces in pictures

`python compare.py picture1 picture2`

Saves face encodings from pictures

`python fr_encodings.py path/to/picture.jpg "name of person" --filename=path/to/save/file`

Detects and recognizes faces in camera

`python video_capture.py --display=true --encodings=path/to/encoding/files --tolerance=0.4`

## Special thanks to:

https://github.com/ageitgey/face_recognition