import os
import json
import requests

link = 'https://graph.facebook.com/v3.0/'
user = '10156528375839031'
token = '?access_token=EAAMlIAK5ZAZAwBAJfNE2IZB0TuD1i5ZCHWORWdeSJkAiZBXOhQafwKpbsWtoM7YKhNNDxtMFJCpAeMTqPSiNiXZAjyo4WU0ZCOZBzlClNpmmrZB7NFtwRRHgx1CiIKbZAVaYnHiANnGnwomyY6IiWD6ZAyixZBOqAHTwkTD4m2KbdkecudjinQrATSkCD9zavFaZC3llCdr8yZC406JwZDZD'
project_root = os.path.abspath(os.path.dirname(__file__))
max_photos = 100

# Output goes to:  ./photos_for_$user_name
user_name = json.loads(requests.get(link+user+token).content)['name'].replace(' ', '_')
maindir = os.path.join(project_root, "photos_for_%s" % user_name)
if not (os.path.exists(maindir) and os.path.isdir(maindir)):
    os.makedirs(maindir)

def main():
    # get_album_photos()
    get_tagged_photos()

def get_album_photos():
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
            thisdir = os.path.join(maindir, "%s - %s" % (album['id'], album['name']))
            if not (os.path.exists(thisdir) and os.path.isdir(thisdir)):
                os.makedirs(thisdir)

            # gets request for photos in album
            photos = json.loads(requests.get(link+album['id']+'/photos'+token).content)['data']

            print("%d photos" % len(photos))
            total_photos += len(photos)

            # Actually download the photos in this album.
            for photo in photos:
                photo_u = requests.get(link+photo['id']+'/picture'+token)
                photo_file = open(os.path.join(thisdir, "%d.jpg" % int(photo['id'])), "wb")
                photo_file.write(photo_u.content)
                photo_file.close()

        print("\n%d total albums" % total_albums)
        print("%d total photos" % total_photos)


def get_tagged_photos():
    downloaded_photos = 0
    next_page = link+user+'/photos'+token

    thisdir = os.path.join(maindir, "Tagged Photos")
    if not (os.path.exists(thisdir) and os.path.isdir(thisdir)):
        os.makedirs(thisdir)

    # gets request for albums from user
    while downloaded_photos < max_photos and next_page:
        r = requests.get(next_page)
        if r.status_code == 200:
            content = json.loads(r.content)
            photos = content['data']
            try:
                next_page = content['paging']['next']
            except KeyError:
                next_page = ''

            # Actually download the photos in this album.
            for photo in photos:
                if downloaded_photos == max_photos:
                    break
                if downloaded_photos % 10 == 0:
                    print('%s photos downloaded' % downloaded_photos)
                photo_u = requests.get(link+photo['id']+'/picture'+token)
                photo_file = open(os.path.join(thisdir, "%d.jpg" % int(photo['id'])), "wb")
                photo_file.write(photo_u.content)
                photo_file.close()
                downloaded_photos += 1
        else:
            break

    print('%s photos downloaded' % downloaded_photos)

if __name__ == '__main__':
    main()
