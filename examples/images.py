# example showing how to get images for an artist
#

import pyen
from pprint import pprint

en = pyen.Pyen()

response = en.get('artist/profile', name='deadmau5', bucket=['images'])
print "<html>"
print "  <body>"

for images in response['artist']['images']:
    print '<img src="' +images['url'] + '">'

print "  </body>"
print "</html>"

