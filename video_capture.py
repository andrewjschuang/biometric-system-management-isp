import os
import signal
import argparse
import datetime
from PIL import Image, ImageDraw
from pathlib import Path

import numpy as np
import cv2
import imutils
import face_recognition
import fr_encodings

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# global variable to run (loop) or not
run = True

# ends process when Ctrl+C is hit
def signal_handler(signal, frame):
    global run
    run = False

# run face recognition in video source
def main(video_source=None, display_image=None, output=None, encodings=None, tolerance=None):
    # default values
    video_source = 0 if video_source is None else video_source
    display_image = False if display_image is None else display_image
    output = './found/temp' if output is None else output
    encodings = './encodings' if encodings is None else encodings
    tolerance = 0.4 if tolerance is None else tolerance

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(video_source)

    # gets all saved encodings
    known_face_encodings = []
    known_face_paths = []
    known_face_names = []
    pathlist = Path(encodings).glob('**/*.pk')
    for path in pathlist:
        path_in_str = str(path)
        known_face_encodings.append(fr_encodings.load(path_in_str)['encoding'])
        known_face_paths.append(path_in_str)
        known_face_names.append(fr_encodings.load(path_in_str)['name'])

    # must have at least one encoding
    if len(known_face_encodings) == 0:
        raise Exception('no face encodings found in directory %s' % encodings)
        exit(1)

    # creates directory if it doesn't exist
    try:
        os.makedirs(output, exist_ok=True)
    except:
        raise Exception('not able to create output directory %s' % output)
        exit(1)

    # Initialize some variables
    found = []
    face_locations = []
    face_encodings = []
    process_this_frame = True

    # run forever until Ctrl+C
    while run:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if not ret:
            return os.path.abspath(output)

        # Resize frame of video to 1/4 size for faster face recognition processing
        # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # process every other frame
        process_this_frame = not process_this_frame

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)

            # only this takes long
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # checks for all faces
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Draw a box around the face
                cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)

                # Gets the face distance for each known faces
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                # Minimum face distance and its index
                min_face_distance = np.min(face_distances)
                min_face_distance_index = np.argmin(face_distances)

                # Gets match
                if min_face_distance <= tolerance:
                    name = known_face_names[min_face_distance_index]
                    face_path = known_face_paths[min_face_distance_index]

                    # don't repeat for found faces
                    # if name in found:
                    #     continue
                    # found.append(name)
                # else:
                #     name = 'unknown'
                #     face_path = 'unknown'

                    # save information
                    timestamp = datetime.datetime.now().strftime("%c")
                    filename = timestamp + '- ' + name + '.png'

                    # save picture file
                    pil_image = Image.fromarray(frame)
                    draw = ImageDraw.Draw(pil_image)
                    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
                    del draw
                    pil_image.save(os.path.join(output, filename))

                    # save output text file
                    out = str({'name': name, 'ts': timestamp, 'image': filename, 'encoding': face_path, 'face distance': min_face_distance}) + '\n'
                    with open(os.path.join(output, 'out.txt'), 'a') as f:
                        f.write(out)

                    # print output
                    # if display_image:
                    print(out, end="")

        # option to display image
        if display_image:
             # Display the resulting image
            cv2.imshow('Biometric System Management', frame)

             # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    # returns output path
    return os.path.abspath(output)

# python argument parser
def createArgsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help="video input source. may be a video file")
    parser.add_argument('-d', '--display', help='whether to display the source video')
    parser.add_argument('-o', '--output', help='folder to save output files')
    parser.add_argument('-e', '--encodings', help='folder of encoding files')
    parser.add_argument('-t', '--tolerance', type=float, help='tolerance for face distance')
    return parser.parse_args()

if __name__ == '__main__':
    # argument parser
    args = createArgsParser()

    # source may be an integer that represents a device or a string that represents a video file
    try:
        args.source = int(args.source)
    except:
        pass

    # display must be a boolean value
    if args.display and args.display.lower() == 'true':
        args.display = True
    else:
        args.display = False

    # encodings must be an existing path
    if args.encodings and not os.path.isdir(args.encodings):
        raise NotADirectoryError('encodings directory not found')
        exit(1)

    # tolerance must be in range [0,1]
    if args.tolerance and (args.tolerance < 0 or args.tolerance > 1):
        raise Exception('tolerance not in range [0,1]')
        exit(1)

    # Ctrl+C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # run face recognition
    output = main(video_source=args.source, display_image=args.display, output=args.output, encodings=args.encodings, tolerance=args.tolerance)

    # print output information
    print('saved information in %s' % output)
