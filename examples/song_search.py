# Displays the 100 top hotttest songs according to the Echo Nest
#
#   python top_songs.py
#

import sys
import pyen
import pprint

en = pyen.Pyen()

artist = sys.argv[1]
title = sys.argv[2]

response = en.get('song/search', artist=artist, title=title, bucket=['audio_summary'], results=1)
for song in response['songs']:
    pprint.pprint(song)
