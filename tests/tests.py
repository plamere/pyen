import pyen
import time
import unittest
import random
import os.path


class TestPyEn(unittest.TestCase):

    def setUp(self):
        self.en = pyen.Pyen()


    def test_top_hot(self):
        response = self.en.get('artist/top_hottt')
        self.assertTrue("artists" in response)
        self.assertTrue(len(response['artists']) >= 15)

    def test_artist_sims(self):
        response = self.en.get('artist/similar', params={'name': 'weezer'})
        self.assertTrue("artists" in response)
        self.assertTrue(len(response['artists']) >= 15)

    def test_cat_create_delete(self):
        try:
            response = self.en.get('catalog/profile', params={'name': 'my-test-catalog-name'})
            if 'catalog' in response:
                cat_id = response['catalog']['id']
                response = self.en.post('catalog/delete', params={'id': cat_id})
                self.assertTrue(response['status']['code'] == 0)
        except:
            pass

        response = self.en.post('catalog/create', params={'name': 'my-test-catalog-name'})
        self.assertTrue("id" in response)
        cat_id = response['id']
        response = self.en.post('catalog/delete', params={'id': cat_id})
        self.assertTrue(response['status']['code'] == 0)


    def test_track_upload(self):
        params = { 'filetype': 'ogg' }
        f_path = os.path.join(os.path.dirname(__file__), '../audio/test.ogg')
        f = open(f_path, 'rb')
        response = self.en.post('track/upload', params, files={'track': f} )
        trid = response['track']['id']
        while True:
            response = self.en.get('track/profile', {'id' : trid, 'bucket' :['audio_summary']} )
            if response['track']['status'] != 'pending':
                break
            time.sleep(1)
        self.assertTrue(response['track']['status'] == 'complete')


    def test_random_walk(self):
        artist_name = 'The Beatles'
        for i in range(10):
            response = self.en.get('artist/similar', {'name': artist_name, 'results': 15} )
            print(artist_name)
            self.assertTrue(len(response['artists']) == 15)
            for artist in response['artists']:
                print("   --> {0}".format(artist['name']))
            artist_name = random.choice(response['artists'])['name']

    def test_slow_random_walk(self):
        en = pyen.Pyen(api_key='YDLX4ITBBQHH3PHU0') # the low rate limit key
        artist_name = 'The Beatles'
        for i in range(3):
            response = en.get('artist/similar', {'name': artist_name, 'results': 15} )
            print(artist_name)
            self.assertTrue(len(response['artists']) == 15)
            for artist in response['artists']:
                print('   --> {0}'.format(artist['name']))
            artist_name = random.choice(response['artists'])['name']
        

if __name__ == '__main__':
    unittest.main()
