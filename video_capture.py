import os
import datetime
from PIL import Image, ImageDraw
from pathlib import Path

import face_recognition
import cv2
import fr_encodings

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# gets all saved encodings
known_face_encodings = []
known_face_names = []
pathlist = Path('./encodings/').glob('**/*.pk')
for path in pathlist:
    path_in_str = str(path)
    known_face_encodings.append(fr_encodings.load(path_in_str)['encoding'])
    known_face_names.append(fr_encodings.load(path_in_str)['name'])

# Initialize some variables
found = []
face_locations = []
face_encodings = []
process_this_frame = True

# creates directory if it doesn't exist
directory = './found'
os.makedirs(directory, exist_ok=True)

# run forever until Ctrl+C
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)

        # only this takes long
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # checks for all faces
        # for face_encoding in face_encodings:
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # don't repeat for found faces
                if name in found:
                    continue
                found.append(name)

                # save info
                timestamp = datetime.datetime.now().strftime("%c")
                filename = name + ' - ' + timestamp + '.png'

                pil_image = Image.fromarray(rgb_small_frame)
                draw = ImageDraw.Draw(pil_image)
                draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
                del draw
                pil_image.save(os.path.join(directory, filename))

                with open(os.path.join(directory, 'out.txt'), 'a') as f:
                    f.write(str({'name': name, 'ts': timestamp, 'image': filename}) + '\n')

    # process every other frame
    process_this_frame = not process_this_frame
