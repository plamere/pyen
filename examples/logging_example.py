import pyen
import random
import logging

logging.basicConfig()

en = pyen.Pyen()

logging.getLogger('pyen').setLevel(logging.DEBUG)

artist_name = 'The Beatles'

for i in xrange(500):
    response = en.get('artist/similar', name=artist_name)

    print artist_name
    for artist in response['artists']:
        print '   --> ', artist['name']

    artist_name = random.choice(response['artists'])['name']
