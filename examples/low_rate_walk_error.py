
import pyen
import random

# this API key has a very low rate limit
# we will try to call it with 120 times
# per minute, which should generate an error


en = pyen.Pyen(api_key='YDLX4ITBBQHH3PHU0', config={'rate_limit': 120} )

artist_name = 'The Beatles'

for i in xrange(10):
    response = en.get('artist/similar', {'name': artist_name} )

    print artist_name
    for artist in response['artists']:
        print '   --> ', artist['name']

    artist_name = random.choice(response['artists'])['name']
