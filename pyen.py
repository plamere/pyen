import requests
import os
import time
import json
import logging

''' A simple and thin python library for the Echo Nest API
'''

logger = logging.getLogger('pyen')

class PyenConfigurationException(Exception): pass

class Pyen(object):

    default_config = {
        'rate_limit': 0,  # calls per minute
        'prefix': 'api/v4',
        'transport': 'http',
        'host': 'developer.echonest.com',
        'api_key': None,
    }

    def __init__(self, **kwargs):
        """ Creates a new Pyen

        Args:
            api_key: the Echo Nest API key. If not set, look
                     for one in the ECHO_NEST_API_KEY environment variable

            config: optional dictionary of configuration parameters. Current parameters include::

                   rate_limit - the default rate limit. If not set, then the rate limit
                                is automatically detected
        """

        for k,v in kwargs.items():
            if k not in self.default_config:
                raise PyenConfigurationException("Unknown configuration item {0}".format(k))

        self.config = {}
        self.config.update(self.default_config)
        self.config.update(kwargs)

        if not self.config['api_key']:
            self.config['api_key'] = os.environ.get('ECHO_NEST_API_KEY')

        if not self.config['api_key']:
            raise PyenConfigurationException("Can't find your API key anywhere")

        self.api_key = self.config['api_key']
        self.last_command_time = 0
        self.time_per_call = 0
        self.trace = False
        self.trace_header = False

        if self.config['rate_limit'] > 0:
            self.time_per_call = 60. / self.config['rate_limit']

    def _internal_call(self, verb, method, params):

        clean_params = dict(api_key = self.config['api_key'])
        files = {}

        for k,v in params.items():
            if isinstance(v, bool):
                v = 'true' if v else 'false'
            elif hasattr(v, 'read') and hasattr(v, 'close'):
                files[k] = v
                continue
            elif (method== 'catalog/update' and k == 'data'
                    and not isinstance(v, str)):
                v = json.dumps(v)
            clean_params[k] = v

        if verb == 'GET':
            args = dict(params=clean_params)
        else:
            args = dict(data=clean_params)
            if files:
                args['files'] = files

        url = '{0}://{1}/{2}/{3}'.format(self.config['transport'],
                                            self.config['host'],
                                            self.config['prefix'], method)
        logger.debug('URL: {0}'.format(url))
        logger.debug('ARGS: {0}'.format(repr(params)))

        r = requests.request(verb, url, **args)

        if r.status_code >= 400 and r.status_code < 500:
            logger.error('ERROR {0} {1}'.format(r.status_code, r.url))

        r.raise_for_status()

        logger.debug('HEADERS {0}'.format(repr(r.headers)))

        if self.time_per_call == 0:
            if 'x-ratelimit-limit' in r.headers:
                rate_limit = int(r.headers['x-ratelimit-limit'])
                if rate_limit > 0:
                    self.config['rate_limit'] = rate_limit
                    self.time_per_call = 60. / rate_limit
                    # print 'auto set of rate limit to', rate_limit, 'TPC is', self.time_per_call
            
        logger.debug('RESP: {0}'.format(r.text))

        results =  r.json()

        response = results['response']
        if response['status']['code'] != 0:
            raise Exception('(' + str(response['status']['code']) + ') - ' + response['status']['message'])

        return response


    def post(self, method, args = None, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call('POST', method, kwargs)

    def get(self, method, args = None, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call('GET', method, kwargs)

    def get_rate_limit(self):
        return self.config['rate_limit']

    def throttle(self):
        delta = time.time() - self.last_command_time
        delay = self.time_per_call - delta
        if delay > 0:
            time.sleep(delay)
        self.last_command_time = time.time()
        
