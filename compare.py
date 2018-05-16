import argparse
import face_recognition

def main():
    args = createArgsParser()

    # encodes first image
    pic1 = face_recognition.load_image_file(args.file1)
    pic1_encoding = face_recognition.face_encodings(pic1)[0]

    # encodes second image
    pic2 = face_recognition.load_image_file(args.file2)
    pic2_encoding = face_recognition.face_encodings(pic2)[0]

    # gets face distance from comparing the images
    # closer to 0 is more similar (less distant)
    face_distances = face_recognition.face_distance([pic1_encoding], pic2_encoding)
    print(face_distances)

    # original threshold: faces are from the same person if face distance < 0.6
    results = face_recognition.compare_faces([pic1_encoding], pic2_encoding)
    print(results)

# parses arguments from command line
def createArgsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file1', help='picture 1 to compare')
    parser.add_argument('file2', help='picture 2 to compare')
    return parser.parse_args()

if __name__ == '__main__':
    main()
