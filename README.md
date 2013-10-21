# Pyen - a Python client for The Echo Nest API

## Description

Pyen is a thin, un-opinionated client library for The Echo Nest. It allows you to easily call Echo Nest methods. It manages API keys, rate limits and error responses in a sane fashion. 

Pyen is a thin client. It doesn't try to represent Echo Nest items such as artists, songs and tracks as objects. Instead, it just lets you call the API method and gives you back a dictionary representation of the Echo Nest response.  If you prefer a fatter client that represents items as objects, and performs intelligent caching consider using [pyechonest](http://github.com/echonest/pyechonest) instead.

## Installation
If you already have [Python](http://www.python.org/) and [pip](http://www.pip-installer.org/) on your system you can install
the library simply by running:

    pip install pyen
    
Or you can download the distribution, unpack it and install in the usual fashion:

    python setup.py install


## Dependencies

- [Requests](https://github.com/kennethreitz/requests) - pyen requires the requests package to be installed


## Quick Start
To get started:

- Install pyen
- **Get an API key** - to use the Echo Nest API you need an Echo Nest API key.  You can get one for free at [developer.echonest.com](http://developer.echonest.com).
- **Set the API** key - you can do this one of two ways:
   - Set an environment variable named `ECHO_NEST_API_KEY` to your API key
   - or Explicitly call the Pyen constructor with your API key like so:
   
    ```en = pyen.Pyen("YOUR_API_KEY")```
    
Call the Pyen.get or the Pyen.post method to make API requests. Here's an example:

    en = pyen.Pyen()  # create the EN api
    response = en.get('artist/similar', {'name': artist_name} )

Extract the output data from the response:

    for artist in response['artists']:
        print artist['id'], artist['name']
        
Refer to the [Echo Nest API documentation](http://developer.echonest.com/docs/v4) for details on the methods and parameters.
Note that most API calls require a 'get' request but certain API method calls require a 'post'. Use the ```Pyen.get``` and
the ```Pyen.post``` where appropriate.  The Echo Nest API documentation indicates whether a `get` or a `post` is required.
   
## Quick Examples

Create a playlist with a seed artist of Weezer:

    import pyen

    # Construct pyen as so:
    #
    # en = pyen.Pyen()
    #
    # this will get your API key from the environment
    # variable ECHO_NEST_API_KEY
    # 
    # alternatively you can call the constructor with the API key
    # like so:
    #
    #  en = pyen.Pyen("YOUR_API_KEY")

    en = pyen.Pyen()
    response = en.get('playlist/static', artist = 'Weezer',
                        type = 'artist-radio')
    for i, song in enumerate(response['songs']):
        print "%d %-32.32s %s" % (i, song['artist_name'], song['title'])


Random walk through similar artists:

    import pyen
    import random

    en = pyen.Pyen()
    artist_name = 'The Beatles'
    for i in xrange(500):
        response = en.get('artist/similar', name =  artist_name)
        print artist_name
        for artist in response['artists']:
            print '   --> ', artist['name']
        artist_name = random.choice(response['artists'])['name']

Create a taste profile:

    import pyen

    en = pyen.Pyen()
    params = {
        'name': 'test-catalog,
        'type': 'general'
    }
    response = en.post('catalog/create', **params)
    print response['id']
    

Update a taste profile:

    import pyen
    import sys
    import os
    import time

    en = pyen.Pyen()
    en.trace = False

    def wait_for_ticket(ticket):
        while True:
            response = en.get('catalog/status', {'ticket':ticket})
            if response['ticket_status'] <> 'pending':
                break
            time.sleep(1)

        print 'status  ', response['ticket_status'] 
        print 'items   ', response['total_items'] 
        print 'updated ', response['items_updated'] 
        print 'complete', response['percent_complete'] 


    if len(sys.argv) > 1:
        cat_id = sys.argv[1]
        items = [
            {
                "action": "update",
                "item" : {
                    "item_id" : "1",
                    "song_name" : "el scorcho",
                    "artist_name" : "weezer",
                }
            },
            {
                "action": "update",
                "item" : {
                    "item_id" : "2",
                    "song_name" : "boyfriend",
                    "artist_name" : "justin bieber",
                    "banned" : True
                }
            },
            {
                "action": "update",
                "item" : {
                    "item_id" : "3",
                    "song_name" : "call me maybe",
                    "artist_name" : "carly rae jepsen",
                    "play_count": 20,
                }
            }
        ]

        params = {
            'id': cat_id,
            'data' : items,
        }
        response = en.post('catalog/update', **params)
        ticket = response['ticket']
        wait_for_ticket(ticket)
    else:
        print "usage: python cat_update.py cat_id"


Upload and analyze a track:

    import pyen
    import sys
    import os
    import time
    import pprint

    en = pyen.Pyen()
    en.trace = False

    def wait_for_analysis(id):
        while True:
            response = en.get('track/profile', id = id,
                                bucket = ['audio_summary'])
            if response['track']['status'] <> 'pending':
                break
            time.sleep(1)

        for k,v in response['track']['audio_summary'].items():
            print "%32.32s %s" % (k, str(v))

    if len(sys.argv) > 2:
        mp3 = sys.argv[1]
        type = sys.argv[2]

        params = {
            'filetype': type,
        }

        f = open(mp3, 'rb')
        
        # note that this is done via a post, with params in the params
        # dictionary, and the file in a files dictionary.
        
        response = en.post('track/upload', filetype = type, tracks = f)
        trid = response['track']['id']
        print 'track id is', trid
        wait_for_analysis(trid)
    else:
        print "usage: python track_upload.py path-audio audio-type"

There are a number of other [examples](http://github.com/plamere/pyen/examples) on github.

## Configuration
You can configure pyen by passing a configuration dictionary
into the constructor like so:

    en = pyen.Pyen(YOUR_API_KEY, rate_limit = 120)

Current configuration parameters are:

- rate_limit - the number of calls per minute that your API key is allowed to make. Note that you should rarely need to set this configuration value since the rate_limit is automatically detected.

You can turn tracing of requests and responses on and off by setting the `pyen` logger:

        import logging
        logging.getLogger('pyen').setLevel(logging.DEBUG)

## Notes
`pyen` will automatically detect your rate limit (by examining the response headers) and automatically throttle your API call rate to match that rate limit.

When an error is detected(via the http response or via the Echo Nest return status code) a python exception is raised.

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/plamere/pyen/issues) or contact me
at [paul@echonest.com](mailto:paul@echonest.com).

