import pyen
import sys

en = pyen.Pyen()

if len(sys.argv) < 2:
    print 'Usage: python genre_playlist.py seed genre name'
else:
    genre = ' '.join(sys.argv[1:])
    response = en.get('playlist/static', type='genre-radio', genre_preset='core-best', genre=genre)

    for i, song in enumerate(response['songs']):
        print "%d %s by %s" % ((i +1), song['title'], song['artist_name'])
