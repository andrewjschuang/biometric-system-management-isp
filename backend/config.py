import os

# default config, db values will take precedence
video_source = 0
tolerance = 0.2
active_rate = 0.5
delay = 0.1
display_image = False
enable_match_confirmation = False
show_only_sundays = True

mongodb = {
    'host': os.environ.get('MONGO_HOST') or 'localhost',
    'port': int(os.environ.get('MONGO_PORT')) if os.environ.get('MONGO_PORT') else 27017,
    'db_name': os.environ.get('MONGO_DB_NAME') or 'bmsisp'
}
