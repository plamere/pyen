# -*- coding: latin-1 -*-
import pyen
import time
import unittest
import random
import os.path
import locale

import logging

logging.basicConfig(level=logging.CRITICAL)


class TestPyEn(unittest.TestCase):

    def setUp(self):
        self.en = pyen.Pyen()


    def test_top_hot(self):
        response = self.en.get('artist/top_hottt')
        self.assertTrue("artists" in response)
        self.assertTrue(len(response['artists']) >= 15)

    def test_artist_sims(self):
        response = self.en.get('artist/similar', name = 'weezer')
        self.assertTrue("artists" in response)
        self.assertTrue(len(response['artists']) >= 15)

    def test_cat_create_delete(self):

        # first cleanup any old catalogs with this name
        try:
            response = self.en.get('catalog/profile', name="my-test-catalog-name")
            if 'catalog' in response:
                cat_id = response['catalog']['id']
                response = self.en.post('catalog/delete', id=cat_id)
                self.assertTrue(response['status']['code'] == 0)
        except:
            pass

        response = self.en.post('catalog/create', name='my-test-catalog-name')
        self.assertTrue("id" in response)
        cat_id = response['id']
        response = self.en.post('catalog/delete', id=cat_id)
        self.assertTrue(response['status']['code'] == 0)

    def test_cat_create_update_delete(self):
        # first cleanup any old catalogs with this name

        try:
            response = self.en.get('catalog/profile', name="my-update-test-catalog")
            if 'catalog' in response:
                cat_id = response['catalog']['id']
                response = self.en.post('catalog/delete', id=cat_id)
                self.assertTrue(response['status']['code'] == 0)
        except:
            pass

        # create the catalog

        response = self.en.post('catalog/create', name='my-update-test-catalog')
        self.assertTrue("id" in response)
        cat_id = response['id']

        # update the catalog

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

        response = self.en.post('catalog/update', id=cat_id, data=items)
        ticket = response['ticket']

        max_tries = 10
        while max_tries > 0:
            response = self.en.get('catalog/status', ticket = ticket)
            if response['ticket_status'] != 'pending':
                break
            time.sleep(1)
            max_tries -= 1

        self.assertTrue(response['ticket_status'] == 'complete')



    #@unittest.skip("skip temporarily")
    def test_track_upload(self):
        f_path = os.path.join(os.path.dirname(__file__), '../audio/test.ogg')
        f = open(f_path, 'rb')
        response = self.en.post('track/upload', filetype='ogg', track=f )
        trid = response['track']['id']
        while True:
            response = self.en.get('track/profile', id=trid, 
                                                    bucket=['audio_summary'])
            if response['track']['status'] != 'pending':
                break
            time.sleep(1)
        self.assertTrue(response['track']['status'] == 'complete')


    def test_random_walk(self):
        artist_name = 'The Beatles'
        for i in range(5):
            response = self.en.get('artist/similar', name=artist_name,
                                        results=15 )
            self.assertTrue(len(response['artists']) == 15)
            artist_name = random.choice(response['artists'])['name']

    def test_slow_random_walk(self):
        en = pyen.Pyen(api_key='YDLX4ITBBQHH3PHU0') # the low rate limit key
        en.auto_throttle = False
        artist_name = 'The Beatles'
        try:
            for i in range(3):
                response = en.get('artist/similar', name=artist_name, results=15 )
        except pyen.PyenException as e:
            self.assertTrue(e.http_status == 429)


    def test_bad_api_key(self):
        en = pyen.Pyen(api_key='BAD_API_KEY') 
        try:
            response = en.get('artist/profile', name='weezer')
            self.assertTrue(False, "Should never get here")
        except pyen.PyenException as e:
            self.assertTrue(True, "exception raised properly")
            self.assertTrue(e.code == 1)

    def test_bad_method(self):
        try:
            response = self.en.get('artist/bad_method', name='weezer')
            self.assertTrue(False, "Should never get here")
        except pyen.PyenException as e:
            self.assertTrue(True, "exception raised properly")
            self.assertTrue(e.code == -1)
            self.assertTrue(e.http_status == 404)

    def test_multiple_ids(self):
        response = self.en.get('song/profile', id=['SOSXTLA12AB017DAC6', 
            'SOIFQXL135C32569FE', 'SOLIUSN13731ED3105'] )
        self.assertTrue(True, len(response['songs']) == 3)

    def test_param_types(self):
        min_tempo = 123.4
        max_tempo = 130
        response = self.en.get('song/search', 
            min_tempo=min_tempo,
            max_tempo=max_tempo,
            artist = 'weezer',
            bucket=['audio_summary', 'artist_location', 'artist_familiarity'],
            results=3)

        self.assertTrue(True, len(response['songs']) == 3)

        for song in response['songs']:
            tempo = song['audio_summary']['tempo']
            self.assertTrue(True, tempo >= min_tempo and tempo <= max_tempo)
            self.assertTrue('los angeles' in song['artist_location']['location'].lower())

    def test_encodings(self):
        def name_check(name):
            response = self.en.get('artist/profile', name=name)
            self.assertTrue(name == response['artist']['name'], 'name check for ' + name)

        name_check(u'Weezer')
        name_check(u'M\xf6tley Cr\xfce')
        name_check(u'Bj\xf6rk')
        name_check(u'!!!')
        name_check(u'Hall & Oates')
        name_check(u'Beyonc\xe9')

    def test_top_hot_from_france(self):
        old_locale = locale.getlocale(locale.LC_ALL)
        locale.setlocale(locale.LC_ALL, 'fr_FR')
        response = self.en.get('artist/top_hottt')
        self.assertTrue("artists" in response)
        self.assertTrue(len(response['artists']) >= 15)
        locale.setlocale(locale.LC_ALL, old_locale)

    def test_artist_sims_over_ssl(self):
        en = pyen.Pyen()
        en.prefix = 'https://developer.echonest.com/api/v4/'
        response = en.get('artist/similar', name = 'weezer')
        self.assertTrue("artists" in response)
        self.assertTrue(len(response['artists']) >= 15)
        

if __name__ == '__main__':
    unittest.main()
