import pyen
import pprint
from datetime import datetime

# shows the age of the newest news article
# for each of the top 100 artists

en = pyen.Pyen()

response = en.get('artist/top_hottt', results=100, bucket=['news', 'reviews', 'blogs']) 

def get_most_recent_date(artist, doc):
    if len(artist[doc]) > 0:
        date =  artist[doc][0]['date_found']
        return get_age_delta(date)
    else:
        return 1000


def get_age_delta(date):
    # 2013-11-17T00:00:00
    today = datetime.today()
    day = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    delta = today - day;
    return delta.days


for artist in response['artists']:
    news_delta =  get_most_recent_date(artist, 'news')
    reviews_delta =  get_most_recent_date(artist, 'reviews')
    blogs_delta =  get_most_recent_date(artist, 'blogs')
    print "%4d %4d %4d %s" % (news_delta, reviews_delta, blogs_delta, artist['name'])


