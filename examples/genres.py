
import pyen
import sys

en = pyen.Pyen()

if len(sys.argv) > 1:
    artist = ' '.join(sys.argv[1:])
    response = en.get('artist/profile', name=artist, bucket=['genre'])
    print response['artist']
    for g in response['artist']['genres']:
        print g['name']
else:
    print "usage: python genres.py artist name"
