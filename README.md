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
   - or Explicitly call the Pyen constructor with your API key 
   
Get the API key from your ECHO_NEST_API_KEY environment variable:
   
    en = pyen.Pyen()

Explicitly set the API key:

    en = pyen.Pyen("YOUR_API_KEY")
    
Call the Pyen.get or the Pyen.post method to make API requests. Here's an example:

    en = pyen.Pyen()  # create the EN api
    response = en.get('artist/similar', name='weezer')

Extract the output data from the response:

    for artist in response['artists']:
        print artist['id'], artist['name']
        
Refer to the [Echo Nest API documentation](http://developer.echonest.com/docs/v4) for details on the methods and parameters.
Note that most API calls require a 'get' request but certain API method calls require a 'post'. Use the ```Pyen.get``` and
the ```Pyen.post``` where appropriate.  The Echo Nest API documentation indicates whether a `get` or a `post` is required.
   
## Quick Examples

Create a playlist with a seed artist of Weezer:

    import pyen
    en = pyen.Pyen()
    
    response = en.get('playlist/static', artist = 'Weezer', type = 'artist-radio')
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



Create a taste profile (note the 'post' call):

    import pyen

    en = pyen.Pyen()

    response = en.post('catalog/create', name='test-catalog', type='general')
    print response['id']
  
## More Examples
A full set of examples can be found in the [Pyen examples directory](https://github.com/plamere/pyen/tree/master/examples)  



## Configuration
You can configure pyen by setting attributes. For example, to enable tracing of method calls and responses:
    
    en = pyen.Pyen()

Current configuration parameters are:

- **api_key** - your Echo Nest API key.
- **auto_throttle** - (default True) - if True, pyen will throttle your API calls to match your rate limit.
- **max_retries** - (default 5) - maximum number of retries when hitting the rate limit

## Logging
*(note, this logging behavior is temporarily disabled)*

You can turn tracing of requests and responses on and off by setting the `pyen` logger:

        import logging
        logging.getLogger('pyen').setLevel(logging.DEBUG)

## Notes
`pyen` will automatically detect your rate limit (by examining the response headers) and automatically throttle your API call rate to match that rate limit. If you turn off this behavior (by setting auto_throttle to False), pyen will throw an exception if you exceed the rate limit.

When an error is detected(via the http response or via the Echo Nest return status code) a python exception is raised.

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/plamere/pyen/issues) or contact me
at [paul@echonest.com](mailto:paul@echonest.com).

## Version
- 2.3 - 11/22/2013 - Added more examples
- 2.2 - 11/15/2013 - Removed logging to avoid unicode error
- 2.1 - 10/22/2013 - New configuration style
- 2.0 - 10/21/2013 - New, more pythonic call style
- 1.1 - 10/19/2013 - Better approach to auto throttling
- 1.0 - 10/18/2013 - Initial release

