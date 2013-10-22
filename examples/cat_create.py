import pyen
import sys
import os


en = pyen.Pyen()

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
    response = en.post('catalog/create', name=name, type='general')
    print response['name']
    print response['id']
    print response['type']
else:
    print "usage: python cat_create.py catalog name"

