import os
import argparse
import json
import face_recognition
import fr_encodings
import numpy as np
import matplotlib.pyplot as plt

def main():
    args = createArgsParser()

    # needs to compare with another picture or a folder of pictures
    if not args.filename and not args.folder:
        print('please indicate picture or folder to compare')
        return

    # load a pickled encoding
    encoding = fr_encodings.load(args.encoding)
    # tolerance for comparing
    tolerance = 0.6

    # compares with all pictures inside folder
    if args.folder:
        distances = []
        results = {'true':0, 'false':0}
        # f = open(args.folder+'/summary-'+args.encoding[10:-3]+'.txt', 'w')
        f = open(args.folder+'/'+args.encoding[10:-3]+'.txt', 'w')
        files, filenames = list_of_files(args.folder)

        # iterates through all picture files
        for file in files:
            image = face_recognition.load_image_file(file)
            pic_encoding = face_recognition.face_encodings(image)

            min_distance = 1
            for pic in pic_encoding:
                face_distance = face_recognition.face_distance([encoding['encoding']], pic)
                if face_distance < min_distance:
                    min_distance = face_distance

            if min_distance == 1:
                print('%s - %s' % (file, [np.nan]))
                f.write('%s - %s\n' % (file, [np.nan]))
                distances.append(np.nan)
            else:
                print('%s - %s' % (file, min_distance))
                f.write('%s - %s\n' % (file, min_distance))
                distances.append(min_distance)

            # original threshold: faces are from the same person if face distance < 0.6
            # result = face_recognition.compare_faces([encoding['encoding']], pic_encoding, tolerance=tolerance)
            if min_distance < tolerance:
                results['true'] += 1
            elif min_distance != 1:
                results['false'] += 1

        fd = np.array(distances)

        # prints results
        print(results)
        print('average: %s' % np.nanmean(fd))
        print(args.encoding)

        # writes results to file
        f.write(json.dumps(results) + '\n')
        f.write('average: %s\n' % np.nanmean(fd))
        f.write(args.encoding)
        f.close()

        # plots face distances graph
        plt.plot(filenames, fd, 'bo')
        plt.title(args.folder)
        plt.ylabel('face distance')
        plt.xlabel('filename')
        plt.xticks(rotation=90)
        plt.axhline(y=tolerance, color='r', linestyle='-')
        plt.gcf().subplots_adjust(bottom=0.4)
        plt.savefig(args.folder+'/face_distances-'+args.encoding[10:-3]+'.png')
        # plt.show()

    # compares with only one picture
    elif args.filename:
        image = face_recognition.load_image_file(args.filename)
        pic_encoding = face_recognition.face_fr_encodings(image)

        min_distance = 1
        for pic in pic_encoding:
            face_distance = face_recognition.face_distance([encoding['encoding']], pic)
            if face_distance < min_distance:
                min_distance = face_distance

        print(min_distance)

        # original threshold: faces are from the same person if face distance < 0.6
        # results = face_recognition.compare_faces([encoding['encoding']], pic_encoding, tolerance=tolerance)
        print(True if min_distance < tolerance else False)

# iterates through folder to get list of filenames
def list_of_files(path):
    # filenames with path
    files = []
    # filenames to label at graph
    fnames = []

    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith('.jpg') or filename.lower().endswith('.png'):
                files.append(os.sep.join([dirpath, filename]))
                fnames.append(filename)

    # cuts .jpg from filename
    fnames = [x[:-4] for x in fnames]

    # sorts as ubuntu directory sorts
    return zip(*sorted(zip(files, fnames), key=lambda x: (len(x[0]), x)))

# parses arguments from command line
def createArgsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoding', help="someone's encoding")
    parser.add_argument('--filename', help='filename of picture to compare')
    parser.add_argument('--folder', help='folder of pictures to compare')
    return parser.parse_args()

if __name__ == '__main__':
    main()
