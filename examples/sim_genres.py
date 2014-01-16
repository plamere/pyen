import pyen
import sys

en = pyen.Pyen()

if len(sys.argv) > 1:
    genre = ' '.join(sys.argv[1:])
    response = en.get('genre/similar', name=genre)
    for genre in response['genres']:
        print genre['name']
else:
    print "usage: python sim_genres.py genre name"
