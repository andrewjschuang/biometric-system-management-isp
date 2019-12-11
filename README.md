# Biometric System Management using Face Recognition

## Dependencies - Debian (Ubuntu)

Compile and install dlib from source
https://github.com/davisking/dlib.git

Install and run MongoDB
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

python3, python3-pip and virtual environment
https://docs.python.org/3/library/venv.html

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

Start the server and have fun!

`./start_server.sh`

## Docker Compose
You may use Docker to run the application

`docker-compose up -d`

## Special thanks to:
https://github.com/ageitgey/face_recognition
