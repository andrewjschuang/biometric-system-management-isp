import argparse
import face_recognition

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file1', help='picture 1 to compare')
    parser.add_argument('file2', help='picture 2 to compare')
    args = parser.parse_args()

    pic1 = face_recognition.load_image_file(args.file1)
    pic1_encoding = face_recognition.face_encodings(pic1)[0]

    pic2 = face_recognition.load_image_file(args.file2)
    pic2_encoding = face_recognition.face_encodings(pic2)[0]

    face_distances = face_recognition.face_distance([pic1_encoding], pic2_encoding)
    print(face_distances)

    results = face_recognition.compare_faces([pic1_encoding], pic2_encoding)
    print(results)

if __name__ == '__main__':
    main()
