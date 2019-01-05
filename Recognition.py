import os
import time
import signal
import argparse
import datetime
import threading
from pathlib import Path
from PIL import Image, ImageDraw

import numpy as np
import cv2
import imutils
import face_recognition
import fr_encodings
import config

# global variable to run (loop) or not
run = True

# ends process when Ctrl+C is hit
def signal_handler(signal, frame):
    global run
    run = False

class Recognition:
    # constructor using configuration file
    def __init__(self):
        self.video_source = config.video_source
        self.display_image = config.display_image
        self.output = config.output
        self.encodings = config.encodings
        self.tolerance = config.tolerance
        self.known_face_encodings = []
        self.known_face_paths = []
        self.known_face_names = []
        self.get_known_encodings(self.encodings)

    # updates attributes
    def update(self, video_source=None, display_image=None, output=None, encodings=None, tolerance=None):
        self.video_source = video_source if video_source else self.video_source
        self.display_image = display_image if display_image else self.display_image
        self.output = output if output else self.output
        self.tolerance = tolerance if tolerance else self.tolerance

        # udpates database
        if encodings != self.encodings:
            self.encodings = encodings
            self.get_known_encodings(self.encodings)

    # starts face recognition
    def start(self):
        self.connect()

    # identifies faces and info
    def identify(self, frame, face_locations, face_encodings):
        found = []
        results = []

        # iterates through each face
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Draw a box around the face
            cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            min_face_distance = np.min(face_distances)
            min_face_distance_index = np.argmin(face_distances)

            # detected and found face in database
            if min_face_distance <= self.tolerance:
                name = self.known_face_names[min_face_distance_index]
                print('%s found' % name)

                # don't repeat for already found faces
                if name in found:
                    print('%s already in cache. skipping..' % name)
                    continue

                found.append(name)
                face_path = self.known_face_paths[min_face_distance_index]
                timestamp = datetime.datetime.now().strftime("%c")
                filename = timestamp + '- ' + name + '.png'
                out = { 'name': name, 'ts': timestamp, 'image': filename, 'encoding': face_path, \
                        'face distance': min_face_distance, 'coordinates': (top, right, bottom, left)}
                results.append(out)

        return results

    # connects to capture device
    def connect(self):
        video_capture = cv2.VideoCapture(self.video_source)

        if not video_capture.isOpened():
            print('error opening capture device %s' % self.video_source)
            exit(1)

        print('connected to capture device')

        # captures indefinitely
        while run:
            frame = self.capture(video_capture, sleep=0.5)

            # displays raw captured frame
            if self.display_image and frame:
                cv2.imshow('Biometric System Management', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print('quitting display')
                    break

        # releases everything
        video_capture.release()
        cv2.destroyAllWindows()

    # captures frames and starts face recognition in new thread
    def capture(self, video_capture, sleep=0):
        ret, frame = video_capture.read()
        if ret:
            print('got new frame')
            threading.Thread(target=self.recognize, args=(frame,)).start()
            print('started recognition thread')
            time.sleep(sleep)
            return frame
        print('error in getting frame')
        return None

    # identifies faces in frame and persists it
    def recognize(self, frame):
        face_locations, face_encodings = self.get_faces_from_picture(frame, model='hog')
        results = self.identify(frame, face_locations, face_encodings)

        # save_cache(result)
        # print('saved new person %s to cache' % result.name)

        names = [x['name'] for x in results]

        if len(names) > 0:
            threading.Thread(target=self.save_picture, args=(frame, results)).start()
            print('saving frame in a new thread: %s' % names)

        return names

    # gets database of resgistered faces
    def get_known_encodings(self, encodings):
        pathlist = Path(encodings).glob('**/*.pk')
        for path in pathlist:
            path_in_str = str(path)
            encoding = fr_encodings.load(path_in_str)['encoding']
            if len(encoding) > 0:
                self.known_face_encodings.append(encoding)
                self.known_face_paths.append(path_in_str)
                self.known_face_names.append(fr_encodings.load(path_in_str)['name'])

        if len(self.known_face_encodings) == 0:
            print('no face encodings found in directory %s' % encodings)
            exit(1)

    # detects faces in frame
    def get_faces_from_picture(self, frame, model='hog'):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(frame, model=model)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        return face_locations, face_encodings

    # saves frame to database with detected info
    def save_picture(self, frame, results):
        # switches back to original color
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        for result in results:
            top, right, bottom, left = result['coordinates']
            pil_image = Image.fromarray(frame)

            # draws rectangle around face
            draw = ImageDraw.Draw(pil_image)
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
            del draw
            
            # creates directory if nonexistent
            try:
                os.makedirs(self.output, exist_ok=True)
            except:
                return False

            # saves image to database
            pil_image.save(os.path.join(self.output, result['image']))

            # writes log to disk
            with open(os.path.join(self.output, 'out.txt'), 'a') as f:
                f.write(str(result))

if __name__ == '__main__':
    # initiates signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # starts face recognition
    recognition = Recognition()
    recognition.start()
