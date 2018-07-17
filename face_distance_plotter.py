import os
import argparse
import json
import face_recognition
import fr_encodings
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def main():
    args = createArgsParser()

    # needs to compare with another picture or a folder of pictures
    if not args.filename and not args.folder:
        print('please indicate picture or folder to compare')
        return

    # load a pickled encoding
    encoding = fr_encodings.load(args.encoding)

    # compares with all pictures inside folder
    if args.folder:
        # gets all image files
        files = list_of_files(args.folder)

        # option to draw box around face
        if args.draw:
            # iterates through all picture files
            for file_path in files:
                print(file_path)
                # don't box boxed file again
                if not 'boxed' in file_path and not 'encoding' in file_path:
                    # searches for the minimum face distance
                    face, min_distance, dimensions = min_face_distance(encoding, file_path)
                    # draws box only if face was found (i.e. dimensions is not null)
                    if dimensions:
                        draw_box(file_path, encoding['name'], min_distance, dimensions)

        # option to compare with pictures inside specified folder
        else:
            # initializes variables
            distances = []
            file_paths = []
            results = {'true':0, 'false':0}
            os.makedirs(os.path.join(args.folder, os.path.basename(os.path.dirname(args.encoding))), exist_ok=True)
            f = open(args.folder+args.encoding[10:-3]+'.txt', 'w')
            # iterates through all picture files
            for file_path in files:

                # searches for the minimum face distance
                face, min_distance, dimensions = min_face_distance(encoding, file_path)

                # saves distance to file if face was found or nan if no face was found
                if face:
                    # writes result for each picture comparison to file
                    print('%s - %s' % (file_path, min_distance))
                    f.write('%s - %s\n' % (file_path, min_distance))
                    distances.append(min_distance)
                    file_paths.append(file_path)

                # original threshold: faces are from the same person if face distance < 0.6
                if min_distance < args.tolerance:
                    results['true'] += 1
                elif min_distance != 1:
                    results['false'] += 1

            # creates np.array for efficient calculations
            fd = np.array(distances)

            # prints results to stdout
            print(results)
            print('average: %s' % np.nanmean(fd))
            print(args.encoding)

            # writes final results to file
            f.write(json.dumps(results) + '\n')
            f.write('average: %s\n' % np.nanmean(fd))
            f.write(args.encoding)
            f.close()

            # plots face distances graph
            plt.plot(file_paths, fd, 'bo')
            plt.title(args.folder)
            plt.ylabel('face distance')
            plt.xlabel('filename')
            plt.xticks(rotation=90)
            plt.axhline(y=args.tolerance, color='r', linestyle='-')
            plt.gcf().subplots_adjust(bottom=0.4)
            plt.savefig(args.folder+args.encoding[10:-3]+'.png')
            # plt.show()

    # option to compare with only one picture
    elif args.filename:
        # searches for the minimum face distance
        face, min_distance, dimensions = min_face_distance(encoding, args.filename)
        print('face distance: %s' % min_distance)

        # original threshold: faces are from the same person if face distance < 0.6
        print(True if min_distance < args.tolerance else False)

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.
def draw_box(image_path, name, face_distance, dimensions):
    filename = os.path.dirname(image_path) + '/boxed-' + os.path.basename(image_path)
    top, right, bottom, left = dimensions

    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(image_path)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Draw a box around the face using the Pillow module
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # Draw a label with a name below the face
    name_dist = name + ": " + str(round(face_distance,2))
    text_width, text_height = draw.textsize(name_dist)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height - 5), name_dist, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    # pil_image.show()

    # You can also save a copy of the new image to disk if you want by uncommenting this line
    pil_image.save(filename)

# gets face with minimum face distance
def min_face_distance(encoding, unknown_image_path):
    # variables initialization
    min_distance = 1
    face = None
    dimensions = None

    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(unknown_image_path)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        face_distance = face_recognition.face_distance([encoding['encoding']], face_encoding)
        # gets minimum face distance (closest result)
        if face_distance < min_distance:
            min_distance = face_distance[0]
            face = encoding
            dimensions = (top, right, bottom, left)

    return face, min_distance, dimensions

# iterates through folder to get list of filenames
def list_of_files(path):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            # gets only jpg or png files
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.png'):
                files.append(os.path.join(dirpath, filename))
    return files

# parses arguments from command line
def createArgsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoding', help="someone's encoded picture")
    parser.add_argument('--filename', help='filename of picture to compare')
    parser.add_argument('--folder', help='folder of pictures to compare')
    parser.add_argument('--tolerance', type=float, default=0.6, help='tolerance for face distance')
    parser.add_argument('--draw', type=bool, default=False, help='draw box around face')
    return parser.parse_args()

if __name__ == '__main__':
    main()
