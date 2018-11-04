import os
import signal
import argparse
import datetime
from pathlib import Path
from PIL import Image, ImageDraw

import numpy as np
import cv2
import imutils
import face_recognition
import fr_encodings
import config

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

def get_known_encodings(encodings):
    known_face_encodings = []
    known_face_paths = []
    known_face_names = []

    pathlist = Path(encodings).glob('**/*.pk')
    for path in pathlist:
        path_in_str = str(path)
        known_face_encodings.append(fr_encodings.load(path_in_str)['encoding'])
        known_face_paths.append(path_in_str)
        known_face_names.append(fr_encodings.load(path_in_str)['name'])

    if len(known_face_encodings) == 0:
        raise Exception('no face encodings found in directory %s' % pathlist)
        exit(1)

    return known_face_encodings, known_face_paths, known_face_names

def get_faces_from_picture(frame, model='hog'):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame, model=model)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    return face_locations, face_encodings

def identify(frame, face_locations, face_encodings, known_face_encodings, known_face_paths, known_face_names, tolerance, output, save=False):
    found = []
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
            found.append(name)
        
        # unknown person
        # else:
        #     name = 'unknown'
            # face_path = 'unknown'

            timestamp = datetime.datetime.now().strftime("%c")
            filename = timestamp + '- ' + name + '.png'
            out = {'name': name, 'ts': timestamp, 'image': filename, 'encoding': face_path, 'face distance': min_face_distance}
            if save:
                picture = save_picture(frame, output, filename, str(out), (top, right, bottom, left))

            # print output
            # if display_image:
            # print(str(out))

    if len(found) == 0:
        return 'Unknown'
    return found

def save_picture(frame, output, filename, out, coordinates):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    top, right, bottom, left = coordinates
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    del draw
    pil_image.save(os.path.join(output, filename))

    with open(os.path.join(output, 'out.txt'), 'a') as f:
        f.write(out)
    
    return pil_image

def identify_people(frame):
    known_face_encodings, known_face_paths, known_face_names = get_known_encodings(config.encodings)
    face_locations, face_encodings = get_faces_from_picture(frame, model='hog')
    return identify(frame, face_locations, face_encodings, known_face_encodings, known_face_paths, known_face_names, config.tolerance, config.output, save=True)

# run face recognition in video source
def main(video_source, display_image, output, encodings, tolerance, save=False):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(video_source)

    # creates directory if it doesn't exist
    try:
        os.makedirs(output, exist_ok=True)
    except:
        raise Exception('not able to create output directory %s' % output)
        exit(1)

    process_this_frame = True
    known_face_encodings, known_face_paths, known_face_names = get_known_encodings(encodings)

    # run forever until Ctrl+C
    while run:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if not ret:
            return os.path.abspath(output)

        # Only process every other frame of video to save time
        if process_this_frame:
            face_locations, face_encodings = get_faces_from_picture(frame, model='hog')
            found = identify(frame, face_locations, face_encodings, known_face_encodings, known_face_paths, known_face_names, tolerance, output, save=save)

        # option to display image
        if display_image:
             # Display the resulting image
            cv2.imshow('Biometric System Management', frame)

             # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # process every other frame
        process_this_frame = not process_this_frame

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

    # default values
    video_source = config.video_source if args.source is None else args.source
    display_image = config.display_image if args.display is None else args.display
    output = config.output if args.output is None else args.output
    encodings = config.encodings if args.encodings is None else args.encodings
    tolerance = config.tolerance if args.tolerance is None else args.tolerance

    # run face recognition
    output = main(video_source, display_image, output, encodings, tolerance, save=True)

    # print output information
    print('saved information in %s' % output)
