from PIL import Image, ImageDraw
import threading
import argparse
import datetime
import signal
import time
import base64

import face_recognition
import numpy as np
import cv2

import config
from database.EncodingsCollection import EncodingsCollection
from database.EventsCollection import EventsCollection
from database.ImagesCollection import ImagesCollection
from database.MembersCollection import MembersCollection
from entities.Event import Event
from entities.Day import Day
from entities.Photo import Photo
from entities.PhotoCategory import PhotoCategory
from entities.PhotoMode import PhotoMode
from entities.Presence import Presence


class Recognition:
    _instance = None
    _is_initialized = False

    # singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Recognition, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    # constructor using configuration file
    def __init__(self):
        if not self._is_initialized:
            self.encodings_db = EncodingsCollection()
            self.events_db = EventsCollection()
            self.images_db = ImagesCollection()
            self.members_db = MembersCollection()
            self.video_source = config.video_source
            self.display_image = config.display_image
            self.tolerance = config.tolerance
            self.video_capture = cv2.VideoCapture(self.video_source)
            self.known_face_encodings = []
            self.get_known_encodings()
            self.run = False
            self._is_initialized = True

    def inject_socket(self, socketio):
        self.socketio = socketio

    # updates attributes
    def configure(self, video_source=None, display_image=None, tolerance=None):
        if tolerance:
            try:
                tolerance = float(tolerance)
            except Exception as e:
                error = 'Error: tolerance not a floating number'
                print(error)
                return error
            if tolerance < 0 or tolerance > 1:
                error = 'Error: tolerance not between 0 and 1'
                print(error)
                return error
            self.tolerance = tolerance

        if video_source:
            try:
                video_source = int(video_source)
            except:
                pass
            self.video_source = video_source
            self.video_capture.release()
            self.video_capture = cv2.VideoCapture(self.video_source)

        if display_image and (display_image.lower() == 'true' or display_image == '1'):
            self.display_image = True
        elif display_image and (display_image.lower() == 'false' or display_image == '0'):
            self.display_image = False

        return None

    # gets database of registered faces from mongo
    def get_known_encodings(self):
        self.known_face_encodings = self.encodings_db.get_all_encodings()

        if len(self.known_face_encodings) == 0:
            print('no face encodings found in database %s' % self.encodings_db.db_name)
            return
        print('got %s encodings from database' %
              len(self.known_face_encodings))

    # saves frame to database with detected info
    def save_event(self, event, coordinates):
        # switches back to original color
        frame = event.photo
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # draws rectangle around face
        top, right, bottom, left = coordinates
        pil_image = Image.fromarray(frame)
        ImageDraw.Draw(pil_image).rectangle(
            ((left, top), (right, bottom)), outline=(0, 0, 255))

        event.photo = Photo(PhotoCategory.EVENT, PhotoMode.RGB,
                            pil_image.tobytes(), pil_image.size)
        ids = self.events_db.insert_event(event)
        print('saved event to database')
        # to retrieve the saved photo
        # Image.frombytes(event['foto']['mode'], pil_image['foto']['size'], pil_image['foto']['data']).show()

    # starts face recognition
    def start(self, capture_interval=0.5):
        if not self.video_capture.isOpened():
            print('error opening capture device %s' % self.video_source)
            return

        print('connected to capture device')

        # captures indefinitely
        while self.run:
            frame = self.capture()
            _, buffer = cv2.imencode('.jpg', frame)
            encoded_frame = base64.b64encode(buffer.tobytes()).decode('utf-8')
            self.socketio.emit('frame', {'frame': encoded_frame})

            if frame is not None:
                threading.Thread(target=self.recognize, args=(frame,)).start()
                print('started recognition thread')
                time.sleep(capture_interval)

            # displays raw captured frame
            if self.display_image and frame is not None:
                cv2.imshow('Biometric System Management', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.signal_handler()
                    print('quitting display')
                    break

        print('run stopped')

        # releases everything
        self.signal_handler()
        cv2.destroyAllWindows()

    # captures frames and starts face recognition in new thread
    def capture(self):
        ret, frame = self.video_capture.read()
        if ret:
            print('got new frame')
            return frame
        print('error in getting frame')
        return None

    # identifies faces in frame and persists it
    def recognize(self, frame, model='hog', day=None, presence=None):
        if len(self.known_face_encodings) == 0:
            print('no face encodings found in database %s' % self.encodings_db.db_name)
            return

        face_locations, face_encodings = self.get_faces_from_picture(
            frame, model=model)
        results = self.identify(frame, face_locations, face_encodings)
        names = []

        # conf that defines if should update person's presence or not
        if day is not None and day != '':
            for result in results:
                member = self.members_db.get_member_by_id(result.member_id)
                if member.calendar.mark_presence(Day.from_str(day), Presence[presence]):
                    self.members_db.update_member_calendar(member)
                names.append(result.name)
        else:
            names = [x.name for x in results]

        print("found in frame: %s" % names)
        return results

    # detects faces in frame
    def get_faces_from_picture(self, frame, model='hog'):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(frame, model=model)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        return face_locations, face_encodings

    # identifies faces and info
    def identify(self, frame, face_locations, face_encodings):
        results = []

        # iterates through each face
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Draw a box around the face
            cv2.rectangle(frame, (left*4, top*4),
                          (right*4, bottom*4), (0, 0, 255), 2)

            face_distances = face_recognition.face_distance(
                [x.data for x in self.known_face_encodings], face_encoding)

            min_face_distance = np.min(face_distances)
            min_face_distance_index = np.argmin(face_distances)

            # detected and found face in database
            if min_face_distance <= self.tolerance:
                name = self.known_face_encodings[min_face_distance_index].name
                member_id = self.known_face_encodings[min_face_distance_index].member_id

                # don't repeat for already found faces
                # if name in found:
                #     print('%s already in cache. skipping..' % name)
                #     continue

                # create event document and save it to mongodb
                event = Event(member_id, name, Day.today(), min_face_distance,
                              self.known_face_encodings[min_face_distance_index], frame)
                self.save_event(event, coordinates=(top, right, bottom, left))

                _, buffer = cv2.imencode('.jpg', frame)
                encoded_frame = base64.b64encode(buffer.tobytes()).decode('utf-8')

                photo_id = self.members_db.get_member_by_id(member_id).photos['FRONT']
                match = self.images_db.get_image(photo_id)
                encoded_match = base64.b64encode(match).decode('utf-8')

                self.socketio.emit('match', {
                    'image': {
                        'src': encoded_frame,
                    },
                    'match': {
                        'src': encoded_match,
                        'id': str(member_id),
                        'name': str(name)
                    }
                })

                results.append(event)

        return results

    # handles start / stop capturing
    def signal_handler(self, run=False):
        self.run = run


# stand alone execution
if __name__ == '__main__':
    # starts face recognition
    recognition = Recognition()

    # initiates signal handler
    signal.signal(signal.SIGINT, recognition.signal_handler)
    recognition.signal_handler(run=True)
    recognition.start()
