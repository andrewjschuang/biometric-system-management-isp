from pprint import pprint
from PIL import Image
from bson.objectid import ObjectId

from Mongodb import Mongodb

db = Mongodb(db='bmsisp')

def show_picture(document):
    image = document['foto']
    Image.frombytes(image['mode'], image['size'], image['data']).show()

def print_info(document, log=False):
    info = {
        'nome': document['nome'],
        # 'encoding': document['encoding'],
        # 'foto': document['foto'],
        'face_distance': document['face_distance']
    }

    if log:
        print('{ %s' % info['nome'], end=', ')
        print('%s }' % info['face_distance'])
    return info

if __name__ == '__main__':
    cursor = db.find('events')

    for document in cursor:
        print_info(document, log=True)
        show_picture(document)
        input()
