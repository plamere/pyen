import requests
import os
import time
import datetime
import json
import logging

''' A simple and thin python library for the Echo Nest API
'''

logger = logging.getLogger('pyen')

class PyenConfigurationException(Exception): pass

class Pyen(object):

    def __init__(self, api_key = None):
        """ Creates a new Pyen

        Args:
            api_key: the Echo Nest API key. If not set, look
                     for one in the ECHO_NEST_API_KEY environment variable

        """

        if not api_key:
            api_key = os.environ.get('ECHO_NEST_API_KEY')

        # These are things we can config
        self.api_key = api_key
        self.auto_throttle = True
        self.prefix = 'http://developer.echonest.com/api/v4/'
        self.max_retries = 5

        if not self.api_key:
            raise PyenConfigurationException("Can't find your API key anywhere")


    def _internal_call(self, verb, method, params):

        clean_params = dict(api_key = self.api_key)
        files = {}

        for k,v in params.items():
            if isinstance(v, bool):
                v = 'true' if v else 'false'
            elif hasattr(v, 'read') and hasattr(v, 'close'):
                files[k] = v
                continue
            elif (method == 'catalog/update' and k == 'data'
                    and not isinstance(v, str)):
                v = json.dumps(v)
            clean_params[k] = v

        if verb == 'GET':
            args = dict(params=clean_params)
        else:
            args = dict(data=clean_params)
            if files:
                args['files'] = files

        url = self.prefix + method

        logger.debug('URL: {0}'.format(url))
        logger.debug('ARGS: {0}'.format(repr(params)))

        max_tries = self.max_retries
        while max_tries > 0:
            r = requests.request(verb, url, **args)

            if self.auto_throttle:
                self.throttle(r)
            if r.status_code == 429 and self.auto_throttle:
                max_tries -= 1
                logger.debug('RATE LIMITED, retrying ...:')
            else:
                break

        if r.status_code >= 400 and r.status_code < 500:
            logger.error('ERROR {0} {1}'.format(r.status_code, r.url))

        logger.debug('HEADERS {0}'.format(repr(r.headers)))
        logger.debug('RESP: {0}'.format(r.text))

        r.raise_for_status()
        results =  r.json()
        response = results['response']
        if response['status']['code'] != 0:
            raise Exception('(' + str(response['status']['code']) + ') - ' + response['status']['message'])
        return response

    def throttle(self, r):
        remaining = int(r.headers['x-ratelimit-remaining'])
        if remaining == 0:
            date_string = r.headers['date']
            date = self.parse_date(date_string)
            delay_time = 60 - date.second
            if delay_time > 0:
                logger.debug('RATE LIMITED, delaying for {0}'.format(delay_time))
                time.sleep(delay_time)

    def parse_date(self, date_string):
        # Mon, 21 Oct 2013 18:06:50 GMT
        # TODO:
        # need to be careful about locale here, the locale
        # will be Echo Nest locale, not local locale. So
        # this code will break in france
        #
        fmt = "%a, %d %b %Y %H:%M:%S %Z"
        date = datetime.datetime.strptime(date_string, fmt)
        return date

    def post(self, method, args = None, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call('POST', method, kwargs)

    def get(self, method, args = None, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call('GET', method, kwargs)

