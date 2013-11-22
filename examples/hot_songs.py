# Displays the 100 top hotttest songs according to the Echo Nest
#
#   python top_songs.py
#

import pyen
en = pyen.Pyen()

start = 0
i = 1
last_artist = None
last_hotttnesss = 0

while i <= 100:
    response = en.get('song/search', start=start, results=100, bucket='song_hotttnesss', sort='song_hotttnesss-desc')
    for song in response['songs']:
        if song['artist_name'] == last_artist and song['song_hotttnesss'] == last_hotttnesss:
            continue
        else:
            print i, song['title'], ' --- ', song['artist_name']
            last_artist = song['artist_name']
            last_hotttnesss = song['song_hotttnesss']
            i += 1
            if i > 100:
                break
    start += 100
