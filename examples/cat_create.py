import pyen
import sys
import os


en = pyen.Pyen()

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
    params = {
        'name': name,
        'type': 'general'
    }
    response = en.post('catalog/create', params)
    print response['name']
    print response['id']
    print response['type']
else:
    print "usage: python cat_create.py catalog name"

