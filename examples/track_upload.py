import pyen
import sys
import os
import simplejson as json
import time
import pprint


en = pyen.Pyen()
en.trace = False

def wait_for_analysis(id):
    while True:
        response = en.get('track/profile', {'id' : id, 'bucket' :['audio_summary']} )
        if response['track']['status'] <> 'pending':
            break
        time.sleep(1)

    for k,v in response['track']['audio_summary'].items():
        print "%32.32s %s" % (k, str(v))


if len(sys.argv) > 2:
    mp3 = sys.argv[1]
    type = sys.argv[2]

    params = {
        'filetype': type,
    }

    f = open(mp3, 'rb')
    response = en.post('track/upload', params, files={'track': f} )
    trid = response['track']['id']
    print 'track id is', trid
    wait_for_analysis(trid)
else:
    print "usage: python track_upload.py path-audio audio-type"


