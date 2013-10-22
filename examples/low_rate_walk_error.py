
import pyen
import random

# this API key has a very low rate limit
# with auto_throttle disabled we will generate
# a 429 error when we reach the rate limit

en = pyen.Pyen(api_key='YDLX4ITBBQHH3PHU0')
en.auto_throttle=False

artist_name = 'The Beatles'

for i in xrange(10):
    response = en.get('artist/similar', name=artist_name )

    print artist_name
    for artist in response['artists']:
        print '   --> ', artist['name']

    artist_name = random.choice(response['artists'])['name']
