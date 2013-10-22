import pyen
import sys

en = pyen.Pyen()

if len(sys.argv) < 2:
    print 'Usage: python playlist.py seed artist name'
else:
    artist_name = ' '.join(sys.argv[1:])
    response = en.get('playlist/static', artist=artist_name, type='artist-radio' )

    for i, song in enumerate(response['songs']):
        print "%d %-32.32s %s" % (i, song['artist_name'], song['title'])
