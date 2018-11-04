import cv2
import requests
import datetime
import time
from PIL import Image

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if ret:
        filename = datetime.datetime.now().isoformat() + '.jpg'
        cv2.imwrite(filename, frame)
        with open(filename, 'rb') as f:
            requests.post('http://localhost:5000', files={ 'file' : f })
    time.sleep(1)
