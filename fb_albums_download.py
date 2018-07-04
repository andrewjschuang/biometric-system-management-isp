import os
import json
import requests

link = 'https://graph.facebook.com/v3.0/'
user = '10156528375839031'
token = '?access_token=EAAMlIAK5ZAZAwBAP9dpCcV2qefkbkWpDs3Pepf97RJCtJquh92A2pchPg8j1tHdPdMIYnABhys3czAfnle286gZBWSGvf5m8nZBSpPpJEGlCbwR4UBfvU97bEEOp2wBbEVgyj4eLCRyrKGZCdLxHaX1TpIOyzbamVBXkCsAtK5ao4ivo7TV1cUHTAINbH7PwZD'
project_root = os.path.abspath(os.path.dirname(__file__))
user_name = json.loads(requests.get(link+user+token).content)['name'].replace(' ', '_')

# Output goes to:  ./photos_for_$user_name
maindir = os.path.join(project_root, "photos_for_%s" % user_name)
if not (os.path.exists(maindir) and os.path.isdir(maindir)):
    os.makedirs(maindir)

# gets request for albums from user
r = requests.get(link+user+'/albums'+token)
if r.status_code == 200:
    albums = json.loads(r.content)['data']

    print("Downloading %d albums..." % len(albums))

    total_albums = len(albums)
    total_photos = 0

    for album in albums:
        print("\nAlbum: %s" % album['id'])

        # Make subdirectory for this album
        THISDIR = os.path.join(MAINDIR, "%s - %s" % (album['id'], album['name']))
        if not (os.path.exists(THISDIR) and os.path.isdir(THISDIR)):
            os.makedirs(THISDIR)

        # gets request for photos in album
        photos = json.loads(requests.get(link+album['id']+'/photos'+token).content)['data']

        print("%d photos" % len(photos))
        total_photos += len(photos)

        # Actually download the photos in this album.
        for photo in photos:
            photo_u = requests.get(link+photo['id']+'/picture'+token)
            photo_file = open(os.path.join(THISDIR, "%d.jpg" % int(photo['id'])), "wb")
            photo_file.write(photo_u.content)
            photo_file.close()

    print("\n%d total albums" % total_albums)
    print("%d total photos" % total_photos)
