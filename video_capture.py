import cv2
import threading
import requests
import time
import json
from PIL import Image

video_source = 0
url = 'http://127.0.0.1:5000'

def capture():
    count = 0
    video_capture = cv2.VideoCapture(video_source)
    while True:
        ret, frame = video_capture.read()
        if ret:
            print('got new frame')
            filename = 'frame%s.jpg' % count
            pil_image = Image.fromarray(frame)
            pil_image.save(filename)
            threading.Thread(target=send, args=(filename,)).start()
            print('sending frame')
            time.sleep(0.5)
            count += 1

def send(filename):
    r = requests.post(url, files={'file': open(filename, 'rb')})
    # print('frame sent. status code: %s. response: %s' % (r.status_code, r.text), end='')
    return

if __name__ == '__main__':
    capture()