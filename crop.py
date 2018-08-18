import argparse
import face_recognition
from PIL import Image

def main():
    args = createArgsParser()

    # loads image
    image = face_recognition.load_image_file(args.filename)
    # gets coordinates for each face in picturel=
    face_locations = face_recognition.face_locations(image, model='hog')

    # counter for number of cropped faces
    count = 1
    # crops face image and saves it
    for face_location in face_locations:
        top, right, bottom, left = face_location

        expansion = 1.05
        top = int(top/expansion)
        left = int(left/expansion)
        bottom = int(bottom + abs(top*(expansion-1)))
        right = int(right + abs(left*(expansion-1)))

        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        if args.notlocal:
            out = saveOriginalDirectory(args.filename, count)
        else:
            out = saveLocally(args.filename, count)
        pil_image.save(out)
        count += 1
    print('%s faces cropped' % (count-1))

# parses arguments from command line
def createArgsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='filename of picture to crop')
    parser.add_argument('-nl', '--notlocal', help='save cropped images in original directory', action='store_true')
    return parser.parse_args()

# returns original directory path
def saveOriginalDirectory(fp, count):
    fp, extension = fp.split('.')
    return fp + "-cropped-" + str(count) + '.' + extension

# returns current working directory path
def saveLocally(fp, count):
    fp = fp.split('/')[-1]
    fp, extension = fp.split('.')
    return fp + "-cropped-" + str(count) + '.' + extension

if __name__ == '__main__':
    main()
