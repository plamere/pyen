import pyen
import sys
import os


en = pyen.Pyen()


def play(id):
    print 'playing', id
    os.system("osascript -e 'tell app \"Rdio\" to play source \"%s\"'" % (id,))


if len(sys.argv) > 1:
    artist = ' '.join(sys.argv[1:])
    params = {
        'type':'artist', 
        'artist':artist, 
        'results': 1,
        'bucket' : ['id:rdio-US', 'tracks'],
        'limit' : True
    }
    response = en.get('playlist/static', **params)
    songs = response['songs']
    if len(songs) > 0:
        song = songs[0]
        track = song['tracks'][0]
        rdio_track_id = track['foreign_id'].split(':')[2]
        print 'playing', song['title'], 'by', song['artist_name']
        play(rdio_track_id)
    else:
        print "Can't find any songs for", artist

else:
    print "usage: python rdio_play.py artist name"


