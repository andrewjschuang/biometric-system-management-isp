import pickle
import argparse
import os
import face_recognition

def main():
    args = createArgsParser()
    pic = face_recognition.load_image_file(args.picture)
    pic_encoding = face_recognition.face_encodings(pic)[0]
    if args.filename:
        result = save(pic_encoding, args.name, args.filename)
    else:
        result = save(pic_encoding, args.name, getNextFilenameInt())
    print(result)

def save(encoding, name, fp):
    if fp.lower().endswith('.jpg') or fp.lower().endswith('.png'):
        fp = fp[:-4] + '.pk'
    try:
        with open(fp, 'wb') as f:
            pickle.dump({'name': name, 'encoding': encoding}, f)
        return True
    except:
        return False

def persist(image, name):
    # pic = face_recognition.load_image_file(image)
    encoding = face_recognition.face_encodings(image)[0]

    filename = getNextFilenameInt()

    if filename.lower().endswith('.jpg') or filename.lower().endswith('.png'):
        filename = filename[:-4] + '.pk'
    try:
        with open(filename, 'wb') as f:
            pickle.dump({'name': name, 'encoding': encoding}, f)
        return True
    except:
        return False

def load(fp):
    with open(fp, 'rb') as f:
        return pickle.load(f)

def createArgsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('picture', help='picture to encode')
    parser.add_argument('name', help='name of person')
    parser.add_argument('--filename', help='filename to save')
    return parser.parse_args()

def getNextFilenameInt():
    i = 1
    while os.path.exists("encodings/encoding-%s.pk" % i):
        i += 1
    return ("encodings/encoding-%s.pk" % i)

if __name__ == '__main__':
    main()
