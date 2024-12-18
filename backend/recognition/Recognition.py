from PIL import Image, ImageDraw
import threading
import signal
import time
import base64

import face_recognition
import numpy as np
import cv2
import io

from database.ConfigCollection import ConfigCollection
from database.EncodingsCollection import EncodingsCollection
from database.EventsCollection import EventsCollection
from database.ImagesCollection import ImagesCollection
from database.MembersCollection import MembersCollection
from entities.Event import Event
from utils.logger import logger


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
            self.config_db = ConfigCollection()
            self.encodings_db = EncodingsCollection()
            self.events_db = EventsCollection()
            self.images_db = ImagesCollection()
            self.members_db = MembersCollection()
            self.known_face_encodings = []
            self.get_known_encodings()
            self.video_capture = cv2.VideoCapture(self.config_db.get_video_source())
            self.run = False
            self._is_initialized = True

    def inject_socket(self, socketio):
        self.socketio = socketio

    # updates attributes
    def update_video_source(self, video_source):
        self.video_capture.release()
        self.video_capture = cv2.VideoCapture(video_source)
        if self.video_capture.isOpened():
            logger.info('successfully updated video source')
        else:
            logger.error(f'error updating video source {video_source}')

    # gets database of registered faces from mongo
    def get_known_encodings(self):
        self.known_face_encodings = self.encodings_db.get_all_encodings()

        n = len(self.known_face_encodings)
        if n == 0:
            logger.info('zero encodings found in database')
        else:
            logger.info(f'loaded {n} encodings from database')

    # saves frame to database with detected info
    def save_event(self, event, coordinates):
        # switches back to original color
        frame = cv2.cvtColor(event.photo, cv2.COLOR_RGB2BGR)

        # draws rectangle around face
        top, right, bottom, left = coordinates
        pil_image = Image.fromarray(frame)
        ImageDraw.Draw(pil_image).rectangle(
            ((left, top), (right, bottom)), outline=(0, 0, 255))

        imgByteArr = io.BytesIO()
        pil_image.save(imgByteArr, format='JPEG')
        imgByteArr.seek(0)
        image_id = self.images_db.insert_image(imgByteArr.getvalue())
        logger.debug('saved event image to database')

        event.photo = image_id
        self.events_db.insert_event(event)
        logger.debug('saved event to database')

        return image_id

    # starts face recognition
    def start(self):
        if not self.video_capture.isOpened():
            logger.error(f'error opening capture device {self.config_db.get_video_source()}')
            return

        logger.debug('connected to capture device')

        # captures indefinitely
        while self.run:
            frame = self.capture()
            _, buffer = cv2.imencode('.jpg', frame)
            encoded_frame = base64.b64encode(buffer.tobytes()).decode('utf-8')
            self.socketio.emit('frame', {'frame': encoded_frame})

            if frame is not None:
                threading.Thread(target=self.recognize, args=(frame,)).start()
                logger.debug('started recognition thread')
                time.sleep(self.config_db.get_delay())

            # displays raw captured frame
            if self.config_db.get_display_image() and frame is not None:
                cv2.imshow('Biometric System Management', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.signal_handler()
                    logger.debug('quitting display')
                    break

        logger.debug('run stopped')

        # releases everything
        self.signal_handler()
        cv2.destroyAllWindows()

    # captures frames and starts face recognition in new thread
    def capture(self):
        ret, frame = self.video_capture.read()
        if ret:
            logger.debug('new frame')
            return frame
        logger.debug('failed to capture frame')

    # identifies faces in frame and persists it
    def recognize(self, frame, model='hog', dry_run=False):
        if len(self.known_face_encodings) == 0:
            logger.warning('zero encodings found in database')
            return

        face_locations, face_encodings = self.get_faces_from_picture(
            frame, model=model)

        return self.identify(frame, face_locations, face_encodings, dry_run)

    # detects faces in frame
    def get_faces_from_picture(self, frame, model='hog'):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(frame, model=model)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        return face_locations, face_encodings

    # identifies faces and info
    def identify(self, frame, face_locations, face_encodings, dry_run=False):
        matches = {}

        # TODO: change to confirmed=True
        for event in self.events_db.get_events_by_date(confirmed=None):
            matches[event.member_id] = event.name

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
            if min_face_distance <= self.config_db.get_tolerance():
                name = self.known_face_encodings[min_face_distance_index].name
                member_id = self.known_face_encodings[min_face_distance_index].member_id

                if dry_run:
                    matches[member_id] = name
                    logger.debug(f"matched {name}: {min_face_distance}")
                    continue

                # don't repeat for already found faces
                if member_id in matches:
                    logger.debug(f'already matched with {name}')
                    continue

                matches[member_id] = name
                logger.debug(f"matched {name}: {min_face_distance}")

                # create event document and save it to mongodb
                event = Event(member_id, name, int(time.time()), min_face_distance, frame,
                              self.known_face_encodings[min_face_distance_index], confirmed=True)
                event_photo_id = self.save_event(
                    event, coordinates=(top, right, bottom, left))

                # TODO: should be transaction / atomic
                member = self.members_db.get_member_by_id(member_id)
                member.calendar.mark_presence(event_photo_id)
                self.members_db.replace_member(member_id, member)

                _, buffer = cv2.imencode('.jpg', frame)
                encoded_frame = base64.b64encode(
                    buffer.tobytes()).decode('utf-8')

                match = self.images_db.get_image(
                    self.members_db.get_member_by_id(member_id).photos['FRONT'])
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

        return list(matches.values())

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
