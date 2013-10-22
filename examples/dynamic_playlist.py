
import pyen
import sys

en = pyen.Pyen()

if len(sys.argv) > 1:
    seed = ' '.join(sys.argv[1:])
else:
    seed = 'Weezer'

response = en.get('playlist/dynamic/create', artist=seed, type='artist-radio')
session_id = response['session_id']

for song_count in xrange(20):
    response = en.get('playlist/dynamic/next', session_id=session_id)
    for i, s in enumerate(response['songs']):
        print "%d %s by %s" % (song_count, s['title'], s['artist_name'])

