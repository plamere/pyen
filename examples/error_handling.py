import pyen
import random


en = pyen.Pyen()

# this throws an exception

try:
    response = en.get('artist/bad_method', name='argument')
except Exception as e:
    print 'trouble - ', e

try:
    response = en.get('artist/profile', bad_argument='argument')
except Exception as e:
    print 'trouble - ', e
