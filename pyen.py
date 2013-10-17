import requests
import os
import time

''' A simple and thin python library for the Echo Nest API
'''

class Pyen:

    default_config = {
        'rate_limit': 0,  # calls per minute
        'prefix': 'http://developer.echonest.com/api/v4/'
    }

    def __init__(self, api_key=None, config=None):
        """ Creates a new Pyen

        Args:
            api_key: the Echo Nest API key. If not set, look
                     for one in the ECHO_NEST_API_KEY environment variable

            config: optional dictionary of configuration parameters. Current parameters include::

                   rate_limit - the default rate limit. If not set, then the rate limit
                                is automatically detected
        """

        if api_key == None:
            if 'ECHO_NEST_API_KEY' in os.environ:
                api_key = os.environ['ECHO_NEST_API_KEY']
            else:
                raise Exception("Pyen:Can't find your API key anywhere")

        self.api_key = api_key
        self.config = self.default_config
        self.last_command_time = 0
        self.time_per_call = 0
        self.trace = False
        self.trace_header = False


        if (config):
            for key, val in config.items():
                if key in self.config:
                    self.config[key] = val
                else:
                    print >> sys.stderr, "Unknown configuration item", key

        if self.config['rate_limit'] > 0:
            self.time_per_call = 60. / self.config['rate_limit']

    def post(self, method, params = None, files = None):
        """ Makes a post request.

            Args:
                method (str): the name of the API method (such as 'artist/profile')
                params (dict): API parameters
                files: (dict): optional - files to be uploaded with the post

            Returns:
                the Echo Nest Response as a dictionary

            Raises:
                Exception - on a transport or Echo Nest error
        """
        return self.get(method, params, True, files)


    def get(self, method, params = None, use_post=False, files=None):
        """ Makes a get request

            Args:
                method (str): the name of the API method (such as 'artist/profile')
                params (dict): (optional) API parameters

            Returns:
                the Echo Nest Response as a dictionary

            Raises:
                Exception - on a transport or Echo Nest error
        """
        self.throttle()
        url = self.config['prefix'] + method

        full_params = {
            'api_key' : self.api_key
        }

        if params:
            full_params.update(params)
            self.normalize(full_params)

        if use_post:
            #url = 'http://requestb.in/1drkod21'
            if files:
                r = requests.post(url, data=full_params, files=files)
            else:
                r = requests.post(url, data=full_params)
            if self.trace:
                print 'send', r.url, full_params
        else:
            r = requests.get(url, params=full_params)
            if self.trace:
                print 'send', r.url



        if self.trace and r.status_code >= 400 and r.status_code < 500:
            print 'error', r.status_code, r.url

        r.raise_for_status()

        if self.trace_header:
            print 'header', r.headers 

        if self.time_per_call == 0:
            if 'x-ratelimit-limit' in r.headers:
                rate_limit = int(r.headers['x-ratelimit-limit'])
                if rate_limit > 0:
                    self.config['rate_limit'] = rate_limit
                    self.time_per_call = 60. / rate_limit
                    # print 'auto set of rate limit to', rate_limit, 'TPC is', self.time_per_call
            

        if self.trace:
            print 'resp:', r.text

        results =  r.json()

        response = results['response']
        if response['status']['code'] <> 0:
            raise Exception('(' + str(response['status']['code']) + ') - ' + response['status']['message'])

        return response

    def normalize(self, params):
        for key, value in params.items():
            if type(value) == bool:
                params[key] = 'true' if value else 'false'

    def get_rate_limit():
        return self.config['rate_limit']

    def throttle(self):
        delta = time.time() - self.last_command_time
        delay = self.time_per_call - delta
        if delay > 0:
            time.sleep(delay)
        self.last_command_time = time.time()
        
