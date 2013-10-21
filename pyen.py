import requests
import os
import time
import datetime

''' A simple and thin python library for the Echo Nest API
'''

class PyenConfigurationException(Exception): pass

class Pyen(object):

    def __init__(self, api_key=None):
        """ Creates a new Pyen

        Args:
            api_key: the Echo Nest API key. If not set, look
                     for one in the ECHO_NEST_API_KEY environment variable

        """

        if api_key == None:
            if 'ECHO_NEST_API_KEY' in os.environ:
                api_key = os.environ['ECHO_NEST_API_KEY']
            else:
                raise PyenConfigurationException("Can't find your API key anywhere")

        # These are things we can config

        self.api_key = api_key
        self.auto_throttle = True
        self.prefix = 'http://developer.echonest.com/api/v4/'
        self.trace = False
        self.trace_header = False
        self.max_retries = 5

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

        url = self.prefix + method

        full_params = {
            'api_key' : self.api_key
        }

        if params:
            full_params.update(params)
            self.normalize(full_params)

        max_tries = self.max_retries
        while max_tries > 0:
            if use_post:
                if files:
                    r = requests.post(url, data=full_params, files=files)
                else:
                    r = requests.post(url, data=full_params)
                if self.trace:
                    print('send {0} {1}'.format(r.url, full_params))
            else:
                r = requests.get(url, params=full_params)
                if self.trace:
                    print('send {0}'.format(r.url))

            if self.auto_throttle:
                self.throttle(r)
            if r.status_code == 429 and self.auto_throttle:
                max_tries -= 1
                if self.trace:
                    print('rate limit hit hard, retry needed')
            else:
                break

        if self.trace and r.status_code >= 400 and r.status_code < 500:
            print('error {0} {1}'.format(r.status_code, r.url))


        if self.trace_header:
            print('header {0}'.format(repr(r.headers)))

        if self.trace:
            print('resp: {0}'.format(r.text))

        r.raise_for_status()
        results =  r.json()
        response = results['response']
        if response['status']['code'] != 0:
            raise Exception('(' + str(response['status']['code']) + ') - ' + response['status']['message'])
        return response

    def normalize(self, params):
        for key, value in params.items():
            if type(value) == bool:
                params[key] = 'true' if value else 'false'

    def throttle(self, r):
        remaining = int(r.headers['x-ratelimit-remaining'])
        if remaining == 0:
            date_string = r.headers['date']
            date = self.parse_date(date_string)
            delay_time = 60 - date.second
            if delay_time > 0:
                if self.trace:
                    print('rate limit hit, throttling for {0} seconds.'.format(delay_time))
                time.sleep(delay_time)

    def parse_date(self, date_string):
        # Mon, 21 Oct 2013 18:06:50 GMT
        # need to be careful about locale here, the locale
        # will be Echo Nest locale, not local locale
        fmt = "%a, %d %b %Y %H:%M:%S %Z"
        date = datetime.datetime.strptime(date_string, fmt)
        return date
