import pyen
import sys


en = pyen.Pyen(api_key=None,)

if len(sys.argv) > 1:
    artist = ' '.join(sys.argv[1:])
    response = en.get('artist/news', name=artist, high_relevance=True)
    for news in response['news']:
        print news['name']
else:
    print "usage: python news.py artist name"
