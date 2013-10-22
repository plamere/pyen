import pyen
import sys
import time


en = pyen.Pyen()
en.trace = False


def wait_for_ticket(ticket):
    while True:
        response = en.get('catalog/status', ticket=ticket)
        if response['ticket_status'] <> 'pending':
            break
        time.sleep(1)

    print 'status  ', response['ticket_status'] 
    print 'items   ', response['total_items'] 
    print 'updated ', response['items_updated'] 
    print 'complete', response['percent_complete'] 


if len(sys.argv) > 1:
    cat_id = sys.argv[1]
    items = [
        {
            "action": "update",
            "item" : {
                "item_id" : "1",
                "song_name" : "el scorcho",
                "artist_name" : "weezer",
            }
        },
        {
            "action": "update",
            "item" : {
                "item_id" : "2",
                "song_name" : "boyfriend",
                "artist_name" : "justin bieber",
                "banned" : True
            }
        },
        {
            "action": "update",
            "item" : {
                "item_id" : "3",
                "song_name" : "call me maybe",
                "artist_name" : "carly rae jepsen",
                "play_count": 20,
            }
        }
    ]
    response = en.post('catalog/update', id=cat_id, data=items)
    ticket = response['ticket']
    wait_for_ticket(ticket)
else:
    print "usage: python cat_update.py cat_id"


