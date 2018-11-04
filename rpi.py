import cv2
import requests
import datetime
import time
import sys
from PIL import Image

video_capture = cv2.VideoCapture(0)

if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    url = 'http://192.168.2.116'

while True:
    ret, frame = video_capture.read()
    if ret:
        filename = datetime.datetime.now().isoformat() + '.jpg'
        cv2.imwrite(filename, frame)
        with open(filename, 'rb') as f:
            requests.post(url, files={ 'file' : f })
    time.sleep(1)
