import sys, argparse
import face_recognition
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='filename of picture to crop')
    parser.add_argument('-nl', '--notlocal', help='save cropped images in original directory', action='store_true')
    args = parser.parse_args()

    image = face_recognition.load_image_file(args.filename)
    face_locations = face_recognition.face_locations(image)

    count = 1
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        if args.notlocal:
            out = saveOriginalDirectory(args.filename, count)
        else:
            out = saveLocally(args.filename, count)
        pil_image.save(out)
        count += 1

def saveOriginalDirectory(fp, count):
    fp, extension = fp.split('.')
    return fp + "-cropped-" + str(count) + '.' + extension

def saveLocally(fp, count):
    fp = fp.split('/')[-1]
    fp, extension = fp.split('.')
    return fp + "-cropped-" + str(count) + '.' + extension

if __name__ == '__main__':
    main()
