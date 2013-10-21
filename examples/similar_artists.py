
import pyen

en = pyen.Pyen()

response = en.get('artist/similar', name='weezer')
for artist in response['artists']:
    print artist['id'], artist['name']
