# Outputs HMTL that shows images of the top 100 artists.
#
# Typical usage:
#   python top_hottt.py > hottt.html
#   open hottt.html
#

import pyen
en = pyen.Pyen()

response = en.get('artist/top_hottt', results=100, bucket=['images'])

print "<html>"
print "  <body>"
for artist in response['artists']:
    print '    <img src="' + artist['images'][0]['url'] + '">'
print "  </body>"
print "</html>"

