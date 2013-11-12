import pyen

en = pyen.Pyen()

queue = []
done = set()
queue.append('ARH6W4X1187B99274F')

while len(queue) > 0:
    cid = queue.pop(0)
    if cid not in done:
        response = en.get('artist/similar', id=cid, bucket='artist_location', artist_location="United States")
        done.add(cid)

        for artist in response['artists']:
            if not artist['id'] in done and not artist['id'] in queue:
                if 'artist_location' in artist:
                    location = artist['artist_location']['location']
                    print artist['id'], artist['name'], location
                    queue.append(artist['id'])
