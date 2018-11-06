import cv2
import threading
import time
import sys

url = 'rtsp://admin:CPqd123$$@10.50.11.111/LiveMedia/ch1/Media1'

def main():
    video_capture = cv2.VideoCapture(url)
    if not video_capture.isOpened():
        print('error opening capture device')
        return

    while True:
        ret, frame = video_capture.read()
        if ret:
            # print('frame captured')
            t = threading.Thread(target=save, args=(frame,))
            t.start()
        time.sleep(1)

def save(frame):
    filename = 'frames/' + str(time.asctime()) + '.jpg'
    cv2.imwrite(filename, frame)
    print('saved frame ' + filename)

if __name__ == '__main__':
    main()
