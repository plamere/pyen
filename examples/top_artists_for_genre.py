import pyen
import sys

en = pyen.Pyen()

if len(sys.argv) > 1:
    genre = ' '.join(sys.argv[1:])
    response = en.get('genre/artists', name=genre)
    for artist in response['artists']:
        print artist['name']
else:
    print "usage: python top_artists_for_genre.py genre name"
