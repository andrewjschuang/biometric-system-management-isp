import os

video_source = 0
tolerance = 0.4
display_image = False

mongodb = {
    'host': os.environ.get('MONGO_HOST') or 'localhost',
    'port': int(os.environ.get('MONGO_PORT')) if os.environ.get('MONGO_PORT') else 27017,
    'db': os.environ.get('MONGO_DB') or 'bmsisp'
}
