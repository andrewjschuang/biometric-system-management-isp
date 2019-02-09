# import os
import time
import signal
import argparse
import datetime
import threading
from PIL import Image, ImageDraw
# from pathlib import Path

from Mongodb import Mongodb
import numpy as np
import cv2
# import imutils
import face_recognition
# import fr_encodings
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
        self.db = Mongodb(config.mongodb['host'], config.mongodb['port'], config.mongodb['db'])
        self.video_source = config.video_source
        self.display_image = config.display_image
        # self.output = config.output
        # self.encodings = config.encodings
        self.tolerance = config.tolerance
        self.known_face_encodings = []
        self.known_face_encodings_list = []
        # self.known_face_paths = []
        # self.known_face_names = []
        self.get_known_encodings()
        # self.get_known_encodings_from_path(self.encodings)

    # updates attributes
    def update(self, video_source=None, display_image=None, output=None, encodings=None, tolerance=None):
        if video_source:
            try:
                self.video_source = int(video_source)
            except:
                self.video_source = video_source
        if display_image and display_image.lower() == 'true':
            self.display_image = True
        if tolerance:
            try:
                self.tolerance = float(tolerance)
            except:
                error = 'ERROR: input tolerance not a floating number'
                print(error)
                return error
        # self.output = output if output else self.output

    #     # udpates database
    #     if encodings != self.encodings:
    #         self.encodings = encodings
    #         self.get_known_encodings(self.encodings)
        return None

    # starts face recognition
    def start(self):
        self.connect()

    # identifies faces and info
    def identify(self, frame, face_locations, face_encodings):
        # found = []
        results = []

        # iterates through each face
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Draw a box around the face
            cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)

            # face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings_list, face_encoding)

            min_face_distance = np.min(face_distances)
            min_face_distance_index = np.argmin(face_distances)

            # detected and found face in database
            if min_face_distance <= self.tolerance:
                # name = self.known_face_names[min_face_distance_index]
                name = self.known_face_encodings[min_face_distance_index]['nome']
                print('%s found' % name)

                # don't repeat for already found faces
                # if name in found:
                #     print('%s already in cache. skipping..' % name)
                #     continue

                self.db.increment('encodings', self.known_face_encodings[min_face_distance_index]['_id'])
                # found.append(name)
                # face_path = self.known_face_paths[min_face_distance_index]
                timestamp = datetime.datetime.now().isoformat()
                # filename = timestamp + '- ' + name + '.png'
                # out = { 'name': name, 'ts': timestamp, 'image': filename, 'encoding': face_path, \
                # out = { 'name': name, 'ts': timestamp, 'image': filename, \
                #         'encoding': self.known_face_encodings[min_face_distance_index]['_id'], \
                #         'face distance': min_face_distance, 'coordinates': (top, right, bottom, left)}
                # results.append(out)

                results.append(name)

                # create event document and save in mongodb
                event = {
                    'nome': name,
                    'membro': None,
                    'data': timestamp,
                    'foto': frame,
                    'encoding': self.known_face_encodings[min_face_distance_index]['_id'],
                    'face_distance': min_face_distance
                }

                self.save_event('events', event, coordinates=(top, right, bottom, left))

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
            frame = self.capture(video_capture)
            if frame is not None:
                threading.Thread(target=self.recognize, args=(frame,)).start()
                print('started recognition thread')

            # displays raw captured frame
            if self.display_image and frame is not None:
                cv2.imshow('Biometric System Management', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print('quitting display')
                    break

        # releases everything
        video_capture.release()
        cv2.destroyAllWindows()

    # captures frames and starts face recognition in new thread
    def capture(self, video_capture, sleep=0.5):
        ret, frame = video_capture.read()
        time.sleep(sleep)
        if ret:
            print('got new frame')
            # threading.Thread(target=self.recognize, args=(frame,)).start()
            # print('started recognition thread')
            return frame
        print('error in getting frame')
        return None

    # identifies faces in frame and persists it
    def recognize(self, frame, model='hog'):
        face_locations, face_encodings = self.get_faces_from_picture(frame, model=model)
        results = self.identify(frame, face_locations, face_encodings)

        # save_cache(result)
        # print('saved new person %s to cache' % result.name)

        # names = [x['name'] for x in results]

        # if len(names) > 0:
        #     threading.Thread(target=self.save_picture, args=(frame, results)).start()
        #     print('saving frame in a new thread: %s' % names)

        print("found in frame: %s" % results)
        return results

    # DEPRECATED
    # gets database of resgistered faces from system path
    # def get_known_encodings_from_path(self, encodings):
    #     pathlist = Path(encodings).glob('**/*.pk')
    #     for path in pathlist:
    #         path_in_str = str(path)
    #         encoding = fr_encodings.load(path_in_str)['encoding']
    #         if len(encoding) > 0:
    #             self.known_face_encodings.append(encoding)
    #             self.known_face_paths.append(path_in_str)
    #             self.known_face_names.append(fr_encodings.load(path_in_str)['name'])
    #         else:
    #             print('warning. found empty encoding: %s' % path_in_str)

    #     if len(self.known_face_encodings) == 0:
    #         print('no face encodings found in directory %s' % encodings)
    #         exit(1)

    #     print(self.known_face_encodings[0])
    #     exit(1)

    # gets database of registered faces from mongo
    def get_known_encodings(self):
        cursor = self.db.find('encodings', {})
        self.known_face_encodings = list(cursor)
        for encoding in self.known_face_encodings:
            self.known_face_encodings_list.append(np.array(encoding.pop('foto')))

        if len(self.known_face_encodings) == 0:
            print('no face encodings found in database %s' % self.db.db)
            exit(1)

        print('got %s encodings from database' % len(self.known_face_encodings))

    # detects faces in frame
    def get_faces_from_picture(self, frame, model='hog'):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(frame, model=model)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        return face_locations, face_encodings

    # saves frame to database with detected info
    def save_event(self, collection, document, coordinates):
        # switches back to original color
        frame = document['foto']
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # for result in results:
        # draws rectangle around face
        top, right, bottom, left = coordinates
        pil_image = Image.fromarray(frame)
        ImageDraw.Draw(pil_image).rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        # del draw

        # pil_image.show()
        document['foto'] = {
            'mode': pil_image.mode,
            'size': pil_image.size,
            'data': pil_image.tobytes()
        }

        ids = self.db.insert(collection, document)
        print('saved event to database')
        # to retrieve the saved photo
        # Image.frombytes(document['foto']['mode'], pil_image['foto']['size'], pil_image['foto']['data']).show()

        # # creates directory if nonexistent
        # try:
        #     os.makedirs(self.output, exist_ok=True)
        # except:
        #     return False

        # # saves image to database
        # pil_image.save(os.path.join(self.output, result['image']))

        # # writes log to disk
        # with open(os.path.join(self.output, 'out.txt'), 'a') as f:
        #     f.write(str(result))

if __name__ == '__main__':
    # initiates signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # starts face recognition
    recognition = Recognition()
    recognition.start()
